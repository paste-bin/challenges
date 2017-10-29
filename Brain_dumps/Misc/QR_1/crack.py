#!/usr/bin/python

from PIL import Image

background = Image.open("./QR3.png")
overlay = Image.open("./QR4.png")

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

new_img = Image.blend(background, overlay, 0.5)
new_img.save("new.png","PNG")
