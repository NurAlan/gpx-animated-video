import gpxpy
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import numpy as np
import os
import cv2
from tqdm import tqdm
import argparse
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description="Generate cinematic GPX overlay video.")
    parser.add_argument('--gpx', type=str, required=True, help='Path to input GPX file')
    parser.add_argument('--output', type=str, default='gpx_cinematic_overlay.mp4', help='Output video file name')
    parser.add_argument('--sample', type=int, default=3, help='Sample every Nth point')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for output video')
    parser.add_argument('--windowsize', type=int, default=1000, help='Map window size in meters')
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        help='Video resolution (e.g., 1920x1080 for landscape, 1080x1920 for portrait)')
    return parser.parse_args()


def main():
    args = parse_args()

    # === CONFIGURATION ===
    GPX_FILE = args.gpx
    OUTPUT_VIDEO = args.output
    SAMPLE_EVERY = args.sample
    FPS = args.fps
    WINDOW_SIZE = args.windowsize  # meter
    FRAME_DIR = "frames"
    FONT = cv2.FONT_HERSHEY_SIMPLEX

    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
    except ValueError:
        print("\U0000274C Format resolusi tidak valid. Gunakan format 'widthxheight' (misal: 1920x1080).")
        return

    print(f"\U0001F5B9 Membaca file GPX: {GPX_FILE}")
    with open(GPX_FILE, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coords = [(p.longitude, p.latitude, p.time)
              for track in gpx.tracks
              for segment in track.segments
              for p in segment.points]

    coords = coords[::SAMPLE_EVERY]

    points = gpd.GeoDataFrame(
        geometry=[Point(lon, lat) for lon, lat, _ in coords],
        crs="EPSG:4326"
    ).to_crs(epsg=3857)

    x_vals = points.geometry.x.values
    y_vals = points.geometry.y.values
    times = [t.timestamp() if t else None for _, _, t in coords]

    os.makedirs(FRAME_DIR, exist_ok=True)
    for f in os.listdir(FRAME_DIR):
        os.remove(os.path.join(FRAME_DIR, f))

    print("\U0001F4D0 Menghitung metrik...")
    total_distance = 0
    cumulative_distance = [0]
    for i in range(1, len(x_vals)):
        dx = x_vals[i] - x_vals[i - 1]
        dy = y_vals[i] - y_vals[i - 1]
        dist = np.sqrt(dx ** 2 + dy ** 2)
        total_distance += dist
        cumulative_distance.append(total_distance)

    print("\U0001F4F8 Membuat frame dengan overlay...")

    # Matplotlib figure size untuk resolusi Full HD (1920x1080)
    fig_width = width / 100
    fig_height = height / 100

    for i in tqdm(range(1, len(x_vals)), desc="Processing frames"):
        cx, cy = x_vals[i], y_vals[i]

        dx = x_vals[i] - x_vals[i - 1]
        dy = y_vals[i] - y_vals[i - 1]
        angle = 0  # Optional: rotate based on direction

        dt = times[i] - times[i - 1] if times[i] and times[i - 1] else 1
        speed_mps = np.sqrt(dx ** 2 + dy ** 2) / dt if dt > 0 else 0
        speed_kph = speed_mps * 3.6

        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
        ax.set_xlim(cx - WINDOW_SIZE, cx + WINDOW_SIZE)
        ax.set_ylim(cy - WINDOW_SIZE, cy + WINDOW_SIZE)

        try:
            ctx.add_basemap(ax,
                            crs=points.crs.to_string(),
                            source=ctx.providers.Esri.WorldImagery,
                            zoom=17)
        except Exception as e:
            print(f"Error loading basemap: {e}")

        ax.plot(x_vals[:i], y_vals[:i], color="red", linewidth=2)
        ax.plot([cx], [cy], "bo", markersize=4)
        ax.axis("off")
        fig.tight_layout(pad=0)

        frame_path = f"{FRAME_DIR}/frame_{i:04d}.png"
        fig.savefig(frame_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        img = cv2.imread(frame_path)
        h, w = img.shape[:2]
        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR)

        distance_km = cumulative_distance[i] / 1000
        time_elapsed = times[i] - times[0] if times[i] and times[0] else 0
        minutes = int(time_elapsed // 60)
        seconds = int(time_elapsed % 60)

        cv2.putText(rotated, f"Distance: {distance_km:.2f} km", (20, 30), FONT, 0.6, (255, 255, 255), 2)
        cv2.putText(rotated, f"Speed: {speed_kph:.1f} km/h", (20, 60), FONT, 0.6, (255, 255, 255), 2)
        cv2.putText(rotated, f"Time: {minutes:02d}:{seconds:02d}", (20, 90), FONT, 0.6, (255, 255, 255), 2)

        cv2.imwrite(frame_path, rotated)

    print("\U0001F3AC Menggabungkan frame menjadi video...")
    frame_example = cv2.imread(f"{FRAME_DIR}/frame_0001.png")
    height, width, _ = frame_example.shape

    out = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS,
        (width, height)
    )

    for i in range(1, len(x_vals)):
        frame_path = f"{FRAME_DIR}/frame_{i:04d}.png"
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    print(f"\u2705 Video berhasil disimpan: {OUTPUT_VIDEO}")

    print("\U0001F5D1 Membersihkan folder frame...")
    shutil.rmtree(FRAME_DIR)
    print("\u2705 Folder frame telah dihapus.")

if __name__ == "__main__":
    main()