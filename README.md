# PhotoWatermark

A simple command-line tool to add shooting date watermarks to images.  
The shooting date is extracted from **EXIF metadata** (if available), otherwise the **file modification time** is used as fallback.

---

## ✨ Features
- Reads shooting date (`YYYY-MM-DD`) from EXIF metadata.  
- Fallback: if no EXIF date exists (e.g. PNG, screenshots), uses file modification time.  
- Allows custom font size, color, and position.  
- Supports both single image file and entire folder as input.  
- Saves results to a new `_watermark` folder at the same level as the input folder.

---

## 📦 Installation

1. Clone this repository:

```bash
git clone https://github.com/<your-username>/PhotoWatermark.git
cd PhotoWatermark
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Add watermark to a folder

```bash
python photo_watermark.py ./images --font_size 40 --color blue --position center
```

Input folder structure:

```
project/
├── images/
│   ├── a.jpg
│   └── b.png
```

Output folder structure:

```
project/
├── images/
│   ├── a.jpg
│   └── b.png
├── images_watermark/
│   ├── a.jpg
│   └── b.png
```

### Add watermark to a single file

```bash
python photo_watermark.py ./images/a.jpg --font_size 50 --color red --position bottomright
```

Output file is saved to:

```
images_watermark/a.jpg
```

---

## ⚙️ Arguments

| Argument       | Type   | Default      | Description |
|----------------|--------|-------------|-------------|
| `input`        | str    | —           | Input file or folder path |
| `--font_size`  | int    | 32          | Font size of watermark text |
| `--color`      | str    | white       | Text color (e.g., `red`, `blue`, `#RRGGBB`) |
| `--position`   | str    | bottomright | Position of watermark: `topleft`, `bottomleft`, `bottomright`, `center` |

---

## 📋 Notes
- Supports `.jpg`, `.jpeg`, `.png`.  
- If EXIF shooting date is missing, the script uses the **file modification time**.  
- The output folder is always created next to the input folder with suffix `_watermark`.  

---

## 📝 Git Workflow (for assignment)

1. Initial commit:

```bash
git commit -am "feat: initial implementation of photo watermark tool"
```

2. Improvement commit (e.g., fallback handling, better folder naming):

```bash
git commit -am "fix: add fallback to file mtime when no EXIF date"
```

3. Tag the release:

```bash
git tag version-1.0
```

---

## 📜 License
MIT License
