import imageio.v2 as imageio
from PIL import ImageTk, Image
import numpy as np
import math
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
        0.299 * im_rgb[:, :, 0] + 0.587 * im_rgb[:, :, 1] + 0.114 * im_rgb[:, :, 2],
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
    new_rgb[:, :, 0] = im_yiq[:, :, 0] + 0.9563 * im_yiq[:, :, 1] + 0.6210 * im_yiq[:, :, 2]
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
    else:
        r, g, b = [np.minimum(image1[:, :, i], image2[:, :, i]) for i in range(3)]
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


def convolve_operation(image_path, operation, size):
    image1 = imageio.imread(image_path)
    image1 = np.clip(image1 / 255., 0., 1.)
    image1 = to_yiq(image1)

    if operation == 'BoxBlur3':
        image = box_blur_filter(image1, 3)
    elif operation == 'BoxBlur5':
        image = box_blur_filter(image1, 5)
    elif operation == 'BoxBlur7':
        image = box_blur_filter(image1, 7)
    elif operation == 'GaussianBlur3':
        image = gaussian_blur_filter(image1, 3)
    elif operation == 'GaussianBlur5':
        image = gaussian_blur_filter(image1, 5)
    elif operation == 'GaussianBlur7':
        image = gaussian_blur_filter(image1, 7)
    elif operation == 'Bartlett3':
        image = bartlett_filter(image1, 3)
    elif operation == 'Bartlett5':
        image = bartlett_filter(image1, 5)
    elif operation == 'Bartlett7':
        image = bartlett_filter(image1, 7)
    elif operation == 'Laplace4':
        image = laplacian_filter(image1, 4)
    elif operation == 'Laplace8':
        image = bartlett_filter(image1, 8)
    elif operation == 'SobelN':
        image = sobel_filter(image1, 'N')
    elif operation == 'SobelNE':
        image = sobel_filter(image1, 'NE')
    elif operation == 'SobelE':
        image = sobel_filter(image1, 'E')
    elif operation == 'SobelSE':
        image = sobel_filter(image1, 'SE')
    elif operation == 'SobelS':
        image = sobel_filter(image1, 'S')
    elif operation == 'SobelSO':
        image = sobel_filter(image1, 'SO')
    elif operation == 'SobelO':
        image = sobel_filter(image1, 'O')
    elif operation == 'SobelNO':
        image = sobel_filter(image1, 'NO')

    image = to_rgb(image)
    image_pil = Image.fromarray(image.astype(np.uint8))
    return resize_image_dir(image_pil, size)

def box_blur_filter(image, size):
    kernel = np.ones((size, size)) / (size ** 2)
    return convolve(image, kernel)


def gaussian_blur_filter(image, size):
    pascal_row = []
    kernel = np.zeros((size, size))
    n = size - 1

    for k in range(size):
        coefficient = math.comb(n, k)
        pascal_row.append(coefficient)
    kernel[0, :] = pascal_row
    kernel[size - 1, :] = pascal_row
    kernel[:, 0] = pascal_row
    kernel[:, size - 1] = pascal_row

    for i in range(1, size - 1):
        for j in range(1, size - 1):
            kernel[i, j] = kernel[0, j] * kernel[i, 0]
    kernel = kernel / (16 ** (size // 2))

    return convolve(image, kernel)


def bartlett_filter(image, size):
    row = []
    kernel = np.zeros((size, size))

    for k in range(size // 2):
        row.append(k + 1)
    for k in range(size // 2, size):
        row.append(size - k)
    kernel[0, :] = row
    kernel[size - 1, :] = row
    kernel[:, 0] = row
    kernel[:, size - 1] = row

    sum = 0
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            kernel[i, j] = kernel[0, j] * kernel[i, 0]

    print(kernel)
    for a in range(size):
        for b in range(size):
            sum += kernel[a,b]
    print(sum)
    return convolve(image, kernel)


def laplacian_filter(image, version):
    kernel = []
    if version == 4:
        kernel = np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ])
    elif version == 8:
        kernel = np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])
    return convolve(image, kernel)


def sobel_filter(image, direction):
    kernel = []
    if direction == 'N':
        kernel = np.array([
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ])
    elif direction == 'S':
        kernel = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])
    elif direction == 'E':
        kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])
    elif direction == 'O':
        kernel = np.array([
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ])
    elif direction == 'NE':
        kernel = np.array([
            [0, 1, 2],
            [-1, 0, 1],
            [-2, -1, 0]
        ])
    elif direction == 'SE':
        kernel = np.array([
            [0, -1, -2],
            [1, 0, -1],
            [2, 1, 0]
        ])
    elif direction == 'NO':
        kernel = np.array([
            [2, 1, 0],
            [1, 0, -1],
            [0, -1, -2]
        ])
    elif direction == 'SO':
        kernel = np.array([
            [-2, -1, 0],
            [-1, 0, 1],
            [0, 1, 2]
        ])
    return convolve(image, kernel)


def convolve(image, kernel):
    min_dim = len(kernel[0, :]) // 2
    max_width = len(image[:, 0, 0]) - min_dim
    max_height = len(image[0, :, 0]) - min_dim
    result_y = np.zeros((len(image[:, 0, 0]) - len(kernel[0, :]) + 1, len(image[0, :, 0]) - len(kernel[:, 0]) + 1))

    for i in range(min_dim, max_width):
        for j in range(min_dim, max_height):
            sub_matriz = image[i - min_dim: i + len(kernel[0, :]) - min_dim,
                         j - min_dim: j + len(kernel[0, :]) - min_dim, 0]
            result_y[i - min_dim, j - min_dim] = np.sum(sub_matriz * kernel)
    result_i = image[min_dim:max_width, min_dim:max_height, 1]
    result_q = image[min_dim:max_width, min_dim:max_height, 2]

    return np.stack((result_y, result_i, result_q), axis=-1)
