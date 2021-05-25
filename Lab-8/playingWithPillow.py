print("Image displayed with Pillow:")
# ======================================================================

from PIL import Image 
image = Image.open("dennis-ritchie.jpg")
print("Image format: {}".format(image.format))
print("Image mode: {}".format(image.mode))
print("Image size: {}".format(image.size))
image.show()

# ======================================================================

print("Image converted to a numpy array:")
# ======================================================================
from matplotlib import image
from matplotlib import pyplot 

data = image.imread("dennis-ritchie.jpg")

print(data.dtype)
print(data.shape)

pyplot.imshow(data)
pyplot.show()

# ======================================================================

image = Image.open("dennis-ritchie.jpg")
print(image.size)

image.thumbnail((100, 100))
print("Thumbnail size: {}".format(image.size))
