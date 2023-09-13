import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np

# im = imageio.imread('imageio:chelsea.png')
im = imageio.imread('../../resource/Charly.bmp')
im = np.clip(im / 255., 0., 1.)


def to_yiq(im_rgb):
    new_yiq = np.zeros(im_rgb.shape)
    new_yiq[:, :, 0] = np.clip(
        0.229 * im_rgb[:, :, 0] + 0.587 * im_rgb[:, :, 1] + 0.114 * im_rgb[:, :, 2],
        a_min=0,
        a_max=1
    )
    new_yiq[:, :, 1] = np.clip(
        0.595716 * im_rgb[:, :, 0] + -0.274453 * im_rgb[:, :, 1] + -0.321263 * im_rgb[:, :, 2],
        a_min=-0.5957,
        a_max=0.5957
    )
    new_yiq[:, :, 2] = np.clip(
        0.211456 * im_rgb[:, :, 0] + -0.522591 * im_rgb[:, :, 1] + 0.311135 * im_rgb[:, :, 2],
        a_min=-0.5226,
        a_max=0.5226
    )
    return new_yiq


def to_rgb(im_yiq):
    new_rgb = np.zeros(im_yiq.shape)
    new_rgb[:, :, 0] = im_yiq[:, :, 0] + 0.9663 * im_yiq[:, :, 1] + 0.6210 * im_yiq[:, :, 2]
    new_rgb[:, :, 1] = im_yiq[:, :, 0] + -0.2721 * im_yiq[:, :, 1] + -0.6474 * im_yiq[:, :, 2]
    new_rgb[:, :, 2] = im_yiq[:, :, 0] + -1.1070 * im_yiq[:, :, 1] + 1.7046 * im_yiq[:, :, 2]
    new_rgb = (new_rgb * 255).astype(int)
    return np.clip(new_rgb, 0, 255)


def apply_params(img, param_a, param_b):
    new_image = np.zeros(img.shape)
    new_image[:, :, 0] = img[:, :, 0] * param_a
    new_image[:, :, 1] = img[:, :, 1] * param_b
    new_image[:, :, 2] = img[:, :, 2] * param_b
    return new_image


yiq = to_yiq(im)

a = 1
b = 1
convert = apply_params(yiq, a, b)

rgb = to_rgb(convert)

plt.imshow(rgb)
plt.show()
