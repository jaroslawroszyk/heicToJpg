# HEIC to JPG Batch Converter

High-performance command-line tool for batch converting **HEIC/HEIF** images to **JPEG**.  
Designed for **stability, low memory usage, and smooth operation inside WSL** and other virtualized environments.

---

## ✨ Features

- **Batch Conversion** – Convert entire folders of `.heic` files at once  
- **Multi-threaded Processing** – Uses `ThreadPoolExecutor` for fast concurrent conversions  
- **WSL-Optimized** – Prevents memory exhaustion common with multiprocessing  
- **Configurable JPEG Quality** – Control output compression level  
- **Progress Tracking** – Real-time progress bar with `tqdm`  
- **Simple CLI Interface** – Easy and script-friendly

---

## ⚙️ Why Threads Instead of Processes?

HEIC decoding is memory-intensive.  
Many converters use multiprocessing, which spawns multiple heavy processes.  
In **WSL or low-RAM systems**, this often leads to:

- Sudden system slowdowns  
- WebSocket disconnects (Error 1006)  
- Full WSL crashes

This tool uses **ThreadPoolExecutor** with conservative defaults, ensuring:

- Lower memory overhead  
- Stable long batch runs  
- No system freezes

---

## 🧰 Requirements

- Python **3.8+**
- Linux, macOS, or **WSL on Windows**
- `pip` installed

---

## 📦 Installation

Clone repository:

```bash
git clone https://github.com/yourusername/heic-to-jpg-converter.git
cd heic-to-jpg-converter
```

---

## 🚀 Usage

### Basic conversion

(Outputs to `converted/` inside input directory)

```bash
python converter.py -i "/path/to/heic/files"
```

### Custom output directory & quality

```bash
python converter.py -i "./input" -o "./output" -q 90
```

### Limit worker threads (maximum stability)

```bash
python converter.py -i "./input" -w 2
```

---

## 🧾 CLI Arguments

| Flag | Long Flag | Description | Default |
|------|-----------|-------------|---------|
| `-i` | `--input` | Input directory containing .heic files | Required |
| `-o` | `--output` | Output directory | `./input/converted` |
| `-q` | `--quality` | JPEG quality (1–100) | `85` |
| `-w` | `--workers` | Number of concurrent threads | `4` |

---

## 📊 Example

```bash
python converter.py \
  --input "/mnt/c/Users/Jaroslaw/Pictures/HEIC" \
  --output "/mnt/c/Users/Jaroslaw/Pictures/JPG" \
  --quality 92 \
  --workers 3
```

---

## 🛡️ Stability Tips for WSL

- Keep `--workers` between 2–4
- Avoid running other heavy apps during conversion
- If converting thousands of images, process in smaller batches

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details.