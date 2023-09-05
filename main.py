import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np

#im = imageio.imread('imageio:chelsea.png')
im = imageio.imread('resource/Charly.bmp')
im = np.clip(im / 255., 0., 1.)


def to_yiq(im_rgb):
    newYIQ = np.zeros(im_rgb.shape)
    newYIQ[:, :, 0] = 0.229 * im_rgb[:, :, 0] + 0.587 * im_rgb[:, :, 1] + 0.114 * im_rgb[:, :, 2]
    newYIQ[:, :, 1] = 0.595716 * im_rgb[:, :, 0] + -0.274453 * im_rgb[:, :, 1] + -0.321263 * im_rgb[:, :, 2]
    newYIQ[:, :, 2] = 0.211456 * im_rgb[:, :, 0] + -0.522591 * im_rgb[:, :, 1] + 0.311135 * im_rgb[:, :, 2]
    return newYIQ


def to_rgb(imYIQ):
    rgb = np.zeros(imYIQ.shape)
    rgb[:, :, 0] = 1 * imYIQ[:, :, 0] + 0.9663 * imYIQ[:, :, 1] + 0.6210 * imYIQ[:, :, 2]
    rgb[:, :, 1] = 1 * imYIQ[:, :, 0] + -0.2721 * imYIQ[:, :, 1] + -0.6474 * imYIQ[:, :, 2]
    rgb[:, :, 2] = 1 * imYIQ[:, :, 0] + -1.1070 * imYIQ[:, :, 1] + 1.7046 * imYIQ[:, :, 2]
    return rgb


def cal(img, a, b):
    newImage = np.zeros(img.shape)
    newImage[:, :, 0] = img[:, :, 0] * a
    newImage[:, :, 1] = img[:, :, 1] * b
    newImage[:, :, 2] = img[:, :, 2] * b
    return newImage


yiq = to_yiq(im)

a = 3
b = 5
convert = cal(yiq, a, b)

rgb = to_rgb(convert)

plt.imshow(rgb)
plt.show()
