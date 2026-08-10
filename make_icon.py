"""One-off, run-by-hand script: generates shutdowntimer.ico for the .exe's
file icon. Not imported by the app itself. Run with: python make_icon.py
"""
from PIL import Image, ImageDraw


def make_icon_image(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = size * 0.06
    draw.ellipse((margin, margin, size - margin, size - margin), fill=(30, 144, 255, 255))
    width = max(2, size // 16)
    center = size / 2
    draw.line((center, center, center, size * 0.22), fill="white", width=width)
    draw.line((center, center, size * 0.72, center), fill="white", width=width)
    return img


if __name__ == "__main__":
    base = make_icon_image(256)
    base.save("shutdowntimer.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    print("Saved shutdowntimer.ico")
