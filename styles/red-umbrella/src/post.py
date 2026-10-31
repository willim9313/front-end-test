"""Grain the rendered scene and make the fogged version that keeps the red umbrella."""
from PIL import Image, ImageChops, ImageFilter

scene = Image.open("scene-raw.png").convert("RGB")
W, H = scene.size
grain = Image.effect_noise((W, H), 14).convert("RGB")
scene = ImageChops.add(ImageChops.subtract(scene, Image.new("RGB", (W, H), (7, 7, 7))), grain, scale=1, offset=-120)
scene = Image.blend(Image.open("scene-raw.png").convert("RGB"), scene, 0.35)
scene.save("../assets/scene.jpg", quality=86, optimize=True, progressive=True)

# fog: heavy blur lifted towards white, then put the red back through a soft mask
r, g, b = scene.split()
red = ImageChops.subtract(r, g).point(lambda v: 255 if v > 70 else 0).filter(ImageFilter.GaussianBlur(10))
red = red.point(lambda v: min(255, v * 3))
blurred = scene.filter(ImageFilter.GaussianBlur(16))
fog = Image.blend(blurred, Image.new("RGB", (W, H), (226, 228, 230)), 0.62)
umbrella = Image.blend(scene.filter(ImageFilter.GaussianBlur(5)), fog, 0.25)
fog = Image.composite(umbrella, fog, red)
fog.save("../assets/fog.jpg", quality=84, optimize=True, progressive=True)
print("ok", W, H)
