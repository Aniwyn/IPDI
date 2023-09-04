import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np

im = imageio.imread('imageio:chelsea.png')
im = np.clip(im / 255., 0., 1.)

imgR = im

imgR[:, :, 0] *= 5

plt.imshow(imgR[:,:,0], 'gray', vmin=0, vmax=1)
plt.show()

# plt.hist(im[:, :, :], bins=25)
# plt.show()
