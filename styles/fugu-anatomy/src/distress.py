import random
from PIL import Image, ImageFilter, ImageChops
W, H = 1120, 800
inks = {"teal": (0x22, 0x5A, 0x6E), "cyan": (0x18, 0x98, 0xB2), "coral": (0xE0, 0x68, 0x5A)}
comp = Image.new("RGB", (W, H), (255, 255, 255))
for i, (n, rgb) in enumerate(inks.items()):
    a = Image.open(f"raw-{n}.png").getchannel("A")
    rnd = random.Random(i)
    # screen wear: fine speckle + a few larger worn patches
    noise = Image.effect_noise((W // 3, H // 3), 90).resize((W, H), Image.BILINEAR)
    wear = noise.point(lambda v: 0 if v > 228 else 255)
    blot = Image.effect_noise((W // 24, H // 24), 70).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
    wear = ImageChops.multiply(wear, blot.point(lambda v: 0 if v > 222 else 255))
    a = ImageChops.multiply(a, wear).filter(ImageFilter.GaussianBlur(0.6))
    Image.merge("LA", (Image.new("L", (W, H), 0), a)).save(f"plate-{n}.png", optimize=True)
    layer = Image.new("RGB", (W, H), rgb)
    tinted = Image.composite(layer, Image.new("RGB", (W, H), (255, 255, 255)), a)
    comp = ImageChops.multiply(comp, tinted)
comp.save("preview.png")
