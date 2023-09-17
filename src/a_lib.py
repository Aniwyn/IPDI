import imageio.v2 as imageio
from PIL import ImageTk, Image
import numpy as np
import os


def resize_image(image_path, size):
    old_image = open_image_abs(image_path)
    width, height = old_image.size
    if width > height:
        new_width = size
        new_height = int(height * (size / width))
    else:
        new_width = int(width * (size / height))
        new_height = size
    image = ImageTk.PhotoImage(Image.open(os.path.abspath(image_path)).resize((new_width, new_height)))
    return image


def resize_image_dir(image, size):
    width, height = image.size
    if width > height:
        new_width = size
        new_height = int(height * (size / width))
    else:
        new_width = int(width * (size / height))
        new_height = size
    new_image = ImageTk.PhotoImage(image.resize((new_width, new_height)))
    return new_image, image


def open_image_abs(image_path):
    image = Image.open(os.path.abspath(image_path))
    return image


def open_image(image_path):
    image = Image.open(image_path)
    return image


def save_image(image, file):
    image.save(file.name)
    file.close()


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


def rgb_to_float(image):
    return np.clip(image / 255., 0., 1.)


def rgb_to_int(image):
    return np.clip((image * 255).astype(int), 0, 255)


def rgb_operations_clamp(image_path_1, image_path_2, operation, size):
    image1 = imageio.imread(image_path_1)
    im1 = np.clip(image1 / 255., 0., 1.)
    image2 = imageio.imread(image_path_2)
    im2 = np.clip(image2 / 255., 0., 1.)
    if operation == '+':
        image = np.clip(((im1 + im2) * 255).astype(int), 0, 255).astype(np.uint8)
    elif operation == '-':
        image = np.clip(((im1 - im2) * 255).astype(int), 0, 255).astype(np.uint8)
    elif operation == '*':
        image = np.clip(((im1 * im2) * 255).astype(int), 0, 255).astype(np.uint8)
    elif operation == '/':
        image = np.clip(((im1 / (im2 + 0.00001)) * 255).astype(int), 0, 255).astype(np.uint8)
    elif operation == 'light':
        r, g, b = [np.maximum(image1[:, :, i], image2[:, :, i]) for i in range(3)]
        image = np.dstack((r, g, b))
    image_pil = Image.fromarray(image)
    return resize_image_dir(image_pil, size)


def rgb_operations_prom(image_path_1, image_path_2, operation, size):
    image1 = imageio.imread(image_path_1)
    im1 = np.clip(image1 / 255., 0., 1.)
    image2 = imageio.imread(image_path_2)
    im2 = np.clip(image2 / 255., 0., 1.)
    if operation == '+':
        image = np.clip(((im1 + im2) * 127.5).astype(int), 0, 255).astype(np.uint8)
    elif operation == '-':
        image = np.clip(((im1 - im2) * 127.5).astype(int), 0, 255).astype(np.uint8)
    elif operation == '*':
        image = np.clip(((im1 * im2) * 127.5).astype(int), 0, 255).astype(np.uint8)
    else:
        image = np.clip(((im1 / (im2 + 0.00001)) * 127.5).astype(int), 0, 255).astype(np.uint8)
    image_pil = Image.fromarray(image)
    return resize_image_dir(image_pil, size)


def interpolate(y1, y2, i1, i2, q1, q2):
    i3 = (y1 * i1 + y2 * i2) / (y1 + y2)
    q3 = (y1 * q1 + y2 * q2) / (y1 + y2)
    return i3, q3


def yiq_operations_clamp(image_path_1, image_path_2, operation, size):
    image1 = imageio.imread(image_path_1)
    image1 = np.clip(image1 / 255., 0., 1.)
    image1 = to_yiq(image1)
    image2 = imageio.imread(image_path_2)
    image2 = np.clip(image2 / 255., 0., 1.)
    image2 = to_yiq(image2)

    y1, i1, q1 = [image1[:, :, i] for i in range(3)]
    y2, i2, q2 = [image2[:, :, i] for i in range(3)]
    i_new, q_new = interpolate(y1, y2, i1, i2, q1, q2)
    if operation == '+':
        y_new = y1 + y2
    elif operation == '-':
        y_new = y1 - y2
    elif operation == '*':
        y_new = y1 * y2
    elif operation == '/':
        y_new = y1 / (y2 + 0.00001)
    elif operation == 'light':
        y_new = np.where(y1 > y2, y1, y2)
    else:
        y_new = np.where(y1 < y2, y1, y2)
    image = np.dstack((y_new, i_new, q_new))
    image = to_rgb(image)
    image_pil = Image.fromarray(image.astype(np.uint8))
    return resize_image_dir(image_pil, size)


def yiq_operations_prom(image_path_1, image_path_2, operation, size):
    image1 = imageio.imread(image_path_1)
    image1 = np.clip(image1 / 255., 0., 1.)
    image1 = to_yiq(image1)
    image2 = imageio.imread(image_path_2)
    image2 = np.clip(image2 / 255., 0., 1.)
    image2 = to_yiq(image2)

    y1, i1, q1 = [image1[:, :, i] for i in range(3)]
    y2, i2, q2 = [image2[:, :, i] for i in range(3)]
    i_new, q_new = interpolate(y1, y2, i1, i2, q1, q2)
    if operation == '+':
        y_new = (y1 + y2) / 2
    elif operation == '-':
        y_new = (y1 - y2) / 2
    elif operation == '*':
        y_new = (y1 * y2) / 2
    else:
        y_new = (y1 / (y2 + 0.00001)) / 2
    image = np.dstack((y_new, i_new, q_new))
    image = to_rgb(image)
    image_pil = Image.fromarray(image.astype(np.uint8))
    return resize_image_dir(image_pil, size)
