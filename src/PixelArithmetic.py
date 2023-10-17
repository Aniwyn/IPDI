# ------------------------Libraries----------------------------------
import numpy as np
import imageio.v2 as imageio
from PIL import ImageTk


# ------------------------Img Manager----------------------
def uploadImgNormalize(path):
    return np.clip(imageio.imread(path) / 255., 0, 1)


def saveImg(img, path):
    return imageio.imwrite(path, img.astpype(np.uint8))

def saveImgTk(img, file):
    imgPil = ImageTk.getimage(img)
    imgPil.save(file.name)

def resize_image_dir(image, size):
    width, height = image.size
    if width > height:
        new_width = size
        new_height = int(height * (size / width))
    else:
        new_width = int(width * (size / height))
        new_height = size
    new_image = ImageTk.PhotoImage(image.resize((new_width, new_height)))
    return new_image


# ------------------------Across Space Chromatic----------------------
def RGBtoYIQ(img):
    img = np.clip(imageio.imread(img) / 255., 0.,1.)
    yiq = np.zeros(img.shape)
    yiq[:, :, 0] = np.clip(0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.144 * img[:, :, 2], None, 1)
    yiq[:, :, 1] = np.clip(0.595716 * img[:, :, 0] - 0.274453 * img[:, :, 1] - 0.321263 * img[:, :, 2], -0.5957, 0.5957)
    yiq[:, :, 2] = np.clip(0.211456 * img[:, :, 0] - 0.52591 * img[:, :, 1] + 0.311135 * img[:, :, 2], -0.5226, 0.5226)

    return yiq

def RGBtoYIQ_array(img):
    img = np.clip(img / 255., 0., 1.)
    yiq = np.zeros(img.shape)
    yiq[:, :, 0] = np.clip(0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.144 * img[:, :, 2], None, 1)
    yiq[:, :, 1] = np.clip(0.595716 * img[:, :, 0] - 0.274453 * img[:, :, 1] - 0.321263 * img[:, :, 2], -0.5957, 0.5957)
    yiq[:, :, 2] = np.clip(0.211456 * img[:, :, 0] - 0.52591 * img[:, :, 1] + 0.311135 * img[:, :, 2], -0.5226, 0.5226)

    return yiq


def YIQtoRGB(img):
    rgb = np.zeros(img.shape)
    rgb[:, :, 0] = img[:, :, 0] + 0.9663 * img[:, :, 1] + 0.6210 * img[:, :, 2]
    rgb[:, :, 1] = img[:, :, 0] - 0.2721 * img[:, :, 1] - 0.6474 * img[:, :, 2]
    rgb[:, :, 2] = img[:, :, 0] - 1.1070 * img[:, :, 1] + 1.7046 * img[:, :, 2]

    rgb = np.clip((rgb * 255).astype(int), 0, 255).astype(np.uint8)
    return rgb


def YIQtoRGB_mod(img):
    rgb = np.zeros(img.shape)
    rgb[:, :, 0] = img[:, :, 0] + 0.9663 * img[:, :, 1] + 0.6210 * img[:, :, 2]
    rgb[:, :, 1] = img[:, :, 0] - 0.2721 * img[:, :, 1] - 0.6474 * img[:, :, 2]
    rgb[:, :, 2] = img[:, :, 0] - 1.1070 * img[:, :, 1] + 1.7046 * img[:, :, 2]


    return np.mod((rgb * 255).astype(int), 255)


# ------------------------RBG Methods--------------------------------
def sumaClampRGB(A, B):
    return np.clip(((A + B) * 255).astype(int), 0, 255)


def sumaDiffRGB(A, B):
    return np.clip((((A + B) * 255) / 2).astype(int), 0, 255)


def restaClampRGB(A, B):
    return np.clip(((A - B) * 255).astype(int), 0, 255)


def restaDiffRGB(A, B):
    return np.clip((((A - B) * 255) / 2).astype(int), 0, 255)


def restaABSClampRGB(A, B):
    return np.clip((abs((A - B)) * 255).astype(int), 0, 255)


def restaABSDiffRGB(A, B):
    return np.clip(((abs((A - B)) * 255) / 2).astype(int), 0, 255)


def multRGB(A, B):
    return np.clip(((A * B) * 255).astype(int), 0, 255)


def multScalarRGB(A, N):
    return np.clip(((A * N) * 255).astype(int), 0, 255)


def divRGB(A, B):
    n = 0.000001
    return np.clip(((A / (B + n)) * 255).astype(int), 0, 255)


def ifLighterRGB(A, B):
    RC = np.maximum(A[:, :, 0], B[:, :, 0])
    GC = np.maximum(A[:, :, 1], B[:, :, 1])
    BC = np.maximum(A[:, :, 2], B[:, :, 2])
    return np.clip((np.dstack((RC, GC, BC)) * 255).astype(int), 0, 255)


def ifDarkerRGB(A, B):
    RC = np.minimum(A[:, :, 0], B[:, :, 0])
    GC = np.minimum(A[:, :, 1], B[:, :, 1])
    BC = np.minimum(A[:, :, 2], B[:, :, 2])
    return np.clip((np.dstack((RC, GC, BC)) * 255).astype(int), 0, 255)


# ------------------------YIQ Methods--------------------------------
def sumaClampYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = np.clip(YA + YB, None, 1)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(np.dstack((YC, IC, QC)))


def sumaDiffYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = (YA + YB) / 2
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(np.dstack((YC, IC, QC)))


def restaClampYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = np.clip(YA - YB, None, 1)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(np.dstack((YC, IC, QC)))


def restaDiffYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = (YA - YB) / 2
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(np.dstack((YC, IC, QC)))


def restaABSClampYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = np.clip(YA - YB, None, 1)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(abs(np.dstack((YC, IC, QC))))


def restaABSDiffYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = (YA - YB) / 2
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(abs(np.dstack((YC, IC, QC))))


def multYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = (YA * YB)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)

    return YIQtoRGB(np.dstack((YC, IC, QC)))


def multScalarYIQ(A, N):
    A = RGBtoYIQ(A)
    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YA = (YA * N)

    return YIQtoRGB(np.dstack((YA, IA, QA)))


def divYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)
    n = 0.000001

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = (YA / (YB + n))
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)
    return YIQtoRGB(np.dstack((YC, IC, QC)))


# ------------------------IF's Methods--------------------------------
def ifLighterYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = np.where(YA > YB, YA, YB)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)
    return YIQtoRGB(np.dstack((YC, IC, QC)))


def ifDarkerYIQ(A, B):
    A = RGBtoYIQ(A)
    B = RGBtoYIQ(B)

    YA, IA, QA = [A[:, :, i] for i in range(3)]
    YB, IB, QB = [B[:, :, i] for i in range(3)]

    YC = np.where(YA < YB, YA, YB)
    IC = (YA * IA + YB * IB) / (YA + YB)
    QC = (YA * QA + YB * QB) / (YA + YB)
    return YIQtoRGB(np.dstack((YC, IC, QC)))


# ------------------------Filters--------------------------------
def raizFilter(A):
    A = RGBtoYIQ(A)
    A[:, :, 0] = np.sqrt(A[:, :, 0])
    return YIQtoRGB(A)


def expFilter(A):
    A = RGBtoYIQ(A)
    A[:, :, 0] = np.square(A[:, :, 0])

    return YIQtoRGB(A)


def linearPartialFiler(A, min, max):
    A = RGBtoYIQ(A)
    min = float(min)
    max = float(max)

    A[:, :, 0] = np.where((A[:, :, 0] >= min) & (A[:, :, 0] <= max),
                          ((-1 / (min - max)) * (A[:, :, 0] - min)),
                          np.where(A[:, :, 0] > max, 1, 0))

    return YIQtoRGB(A)
