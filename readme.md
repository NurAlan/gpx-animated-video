# 🎥 GPX Cinematic Tracker

A Python script to generate cinematic videos from GPX track files with real-time map overlay, distance, speed, and time display.

[![License](https://img.shields.io/github/license/nuralan/gpx-cinematic-tracker )](https://github.com/nuralan/gpx-cinematic-tracker/blob/main/LICENSE )
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg )](https://www.python.org/ )
[![Build](https://img.shields.io/github/actions/workflow/status/nuralan/gpx-cinematic-tracker/build.yml?branch=main)]( https://github.com/nuralan/gpx-cinematic-tracker/actions )

---

## 📌 Deskripsi

GPX Cinematic Tracker adalah tool berbasis CLI (Command Line Interface) yang memungkinkan Anda mengubah file GPX (misalnya dari Strava, Garmin, atau aplikasi pelacak GPS) menjadi video berkualitas tinggi dengan animasi peta, overlay kecepatan, jarak, dan waktu secara real-time.

Anda bisa:
- Mengatur resolusi video (landscape atau portrait)
- Menyesuaikan sampling titik
- Memilih frame rate
- Dan melihat visualisasi rute yang menarik

---

## 🖼️ Contoh Output

![Contoh Video Preview](example.gif)

> *Catatan: Ganti `example.gif` dengan preview video hasil render Anda.*

---

## 🛠️ Instalasi

Pastikan Python 3.9+ sudah terinstal di sistem Anda.

1. Clone repositori:

```bash
git clone https://github.com/username/gpx-cinematic-tracker.git 
cd gpx-cinematic-tracker
```

2. Install dependensi:

```bash
python gpx_cinematic.py --gpx <file.gpx> \
                        --output <video.mp4> \
                        --sample <N> \
                        --fps <FPS> \
                        --windowsize <meter> \
                        --resolution <widthxheight>
```

🔧 Argumen CLI:
| argumen | Deskripsi |
|-------------| --------|
|`--gpx` | Path ke file GPX Anda (wajib) |
|`--output`| Nama file video keluaran (default:`gpx_cinematic_overlay.mp4`)|
| `--sample` | Ambil 1 dari setiap N titik untuk performa (default: 3) |
| `--fps` | Frame per second dari video (default: 30)|
| `--windowsize` | Ukuran area peta dalam meter (default: 1000) |
| `--resolution` | Resolusi video (format: `<lebar>x<tigngi>` misal: `1920x1080, 1080x1920`) |

## 📱 Contoh: 
Untuk video landscape: 
```bash
python gpx_cinematic.py --gpx sample.gpx --output output.mp4 --resolution 1920x1080
```
## Untuk video portrait:
```bash
python gpx_cinematic.py --gpx sample.gpx --output output.mp4 --resolution 1080x1920
```

## 📦 Dependencies 

Install semua dependencies menggunakan: 
```bash
pip install -r requirements.txt
```
 
