import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ExifTags
from datetime import datetime


def get_exif_date(image_path):
    """获取 EXIF 中的拍摄日期（YYYY-MM-DD）。"""
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return None
        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
    except Exception:
        return None
    return None


def add_watermark(image_path, text, font_size, color, position):
    """给图片添加文字水印"""
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))

    # 字体
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(txt_layer)
    text_size = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_size[2] - text_size[0], text_size[3] - text_size[1]

    # 计算位置
    if position == "center":
        pos = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    elif position == "topleft":
        pos = (10, 10)
    elif position == "bottomright":
        pos = (img.width - text_width - 10, img.height - text_height - 10)
    else:
        pos = (10, img.height - text_height - 10)

    draw.text(pos, text, fill=color, font=font)

    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description="Add EXIF date watermark to photos")
    parser.add_argument("input", help="Input image path or folder")
    parser.add_argument("--font_size", type=int, default=32, help="Font size of watermark")
    parser.add_argument("--color", type=str, default="white", help="Font color (e.g., red, blue, #RRGGBB)")
    parser.add_argument(
        "--position", type=str, choices=["topleft", "center", "bottomright", "bottomleft"], default="bottomright"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.is_file():
        files = [input_path]
        # 输出目录在 input 文件所在目录的同级
        out_dir = input_path.parent.parent / f"{input_path.parent.name}_watermark"
    else:
        files = list(input_path.glob("*.*"))
        # 输出目录在 images 同级
        out_dir = input_path.parent / f"{input_path.name}_watermark"

    out_dir.mkdir(exist_ok=True)

    for file in files:
        if file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue
        date = get_exif_date(file)
        if not date:
            # fallback: 用文件修改时间
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            date = mtime.strftime("%Y-%m-%d")
            print(f"⚠ No EXIF date in {file}, using file mtime {date}")
        watermarked = add_watermark(file, date, args.font_size, args.color, args.position)
        save_path = out_dir / file.name
        watermarked.save(save_path)
        print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    main()
