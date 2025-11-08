# rounded.py
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def rounded_rect(w, h, r, fill="#ffffff", outline="#cccccc", width=1):
    """Devuelve una PhotoImage de rectángulo redondeado."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=r,
                           fill=fill, outline=outline, width=width)
    return ImageTk.PhotoImage(img)