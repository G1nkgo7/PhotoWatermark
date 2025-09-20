import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ExifTags
from datetime import datetime


def get_exif_date(img: Image.Image, file_path: Path) -> str:
    """
    获取照片的拍摄日期（优先 EXIF），否则用文件修改时间。
    返回 YYYY-MM-DD 格式字符串。
    """
    try:
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return value.split(" ")[0].replace(":", "-")
    except Exception:
        pass

    # fallback: 文件修改时间
    mtime = file_path.stat().st_mtime
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def add_watermark(input_path: Path, font_size: int, color: str, position: str):
    img = Image.open(input_path).convert("RGBA")
    watermark_text = get_exif_date(img, input_path)

    # 绘制层
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 字体（跨平台可以用 DejaVuSans 或 Windows 自带 Arial）
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # ✅ 兼容新旧 Pillow 版本
    try:
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        # Pillow < 10
        text_w, text_h = draw.textsize(watermark_text, font=font)

    # 位置计算
    if position == "left_top":
        pos = (10, 10)
    elif position == "center":
        pos = ((img.width - text_w) // 2, (img.height - text_h) // 2)
    elif position == "right_bottom":
        pos = (img.width - text_w - 10, img.height - text_h - 10)
    else:
        raise ValueError("位置参数错误: 仅支持 left_top, center, right_bottom")

    # 绘制
    draw.text(pos, watermark_text, font=font, fill=color)

    # 合成并保存
    output_img = Image.alpha_composite(img, txt_layer).convert("RGB")

    # 保存到新目录
    output_dir = input_path.parent / (input_path.parent.name + "_watermark")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / input_path.name
    output_img.save(output_file)
    print(f"✅ 已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="图片加拍摄日期水印工具")
    parser.add_argument("path", help="图片文件路径")
    parser.add_argument("--font_size", type=int, default=32, help="字体大小 (默认: 32)")
    parser.add_argument("--color", type=str, default="red", help="字体颜色 (默认: red)")
    parser.add_argument(
        "--position", type=str, default="right_bottom",
        choices=["left_top", "center", "right_bottom"],
        help="水印位置 (默认: right_bottom)"
    )

    args = parser.parse_args()
    input_path = Path(args.path)

    if not input_path.exists():
        print("❌ 文件不存在:", input_path)
        return

    add_watermark(input_path, args.font_size, args.color, args.position)


if __name__ == "__main__":
    main()


# python photo_watermark.py "./iamges/20250920_17371605.png" --font_size 40 --color blue --position center
