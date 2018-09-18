import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



imageFile = "demo-image.jpg"
im1 = Image.open(imageFile)


draw = ImageDraw.Draw(im1)
draw.text((0, 0), "description", (255, 0, 0))    
draw = ImageDraw.Draw(im1)                          


im1.save("demo-image.jpg")