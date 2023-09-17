import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
import PixelArithmetic as lib

# im = imageio.imread('imageio:chelsea.png')
im1 = imageio.imread('../resource/1024x600/1.png')
im1 = np.clip(im1 / 255., 0., 1.)

im2 = imageio.imread('../resource/1024x600/2.png')
im2 = np.clip(im2 / 255., 0., 1.)

asd = lib.ifLighterRGB(im1, im2)

plt.imshow(asd)
plt.show()
