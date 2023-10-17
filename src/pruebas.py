import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
from src import a_lib as lib

im1 = imageio.imread('../resource/Charly.bmp')
im1 = np.clip(im1 / 255., 0., 1.)

# im2 = imageio.imread('../resource/1024x600/2.png')
# im2 = np.clip(im2 / 255., 0., 1.)
image = lib.to_yiq(im1)
asd = lib.bartlett_filter(image, 9)
qq = lib.to_rgb(asd)

#plt.imshow(im1)
#plt.show()
#plt.imshow(qq)
#plt.show()
