import imageio.v2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import MeanShift as skMeanShift
import src.PixelArithmetic as k
import cv2 as cv

im = imageio.v2.imread('../../resource/S2.png')
im = np.clip(im, 0, 255)

t = np.copy(im)

print('T ', t.shape)
a = np.stack((t[:, :, 0], t[:, :, 1], t[:, :, 2]), axis=-1)
print('A', a.shape)
c = np.stack((t[:, :, 0], t[:, :, 1]), axis=-1)
print('C', c.shape)

u = k.RGBtoYIQ_array(t)
b = np.column_stack((u[:, :, 0].flatten(), u[:, :, 1].flatten()))
print('b ', b.shape, '   ', b[0])
# b = np.column_stack((a[:,:,0].flatten(),a[:,:,1].flatten(),a[:,:,2].flatten()))
# print('b ', b.shape, '   ', b[0])
print(b.shape)
print('entre')
otherlabel = skMeanShift(bandwidth=0.1, bin_seeding=True).fit(b)  # 0.05 5 clases queda bien 0408
# 29 con f2.png
# 15 con 0408.png
# 14 con 0408.png
# 14 con 0508Raiz.png
# 13 con 0508.png
print('Sali')
print(b.shape)
print('Cantidad de labels de sklearn: ', len(np.unique(otherlabel.labels_)))

labesDiferentes = np.unique(otherlabel.labels_)
print(labesDiferentes)

resutls = []
colorLabels = []

for j in range(len(labesDiferentes)):
    aux = np.copy(b)
    colorAux = []
    cantidad_iters = aux.shape[0]
    for i in range(cantidad_iters):
        if otherlabel.labels_[i] == j:
            colorAux.append(aux[i, 0])
    colorLabels.append(np.mean(colorAux))

print('Color originales: ', colorLabels)

for i in range(len(colorLabels)):
    if 0.1 < colorLabels[i] < 0.8:
        colorLabels[i] *= 1.5  # 1.2

imgFinal = np.copy(b)
cantidad_labels = len(labesDiferentes)
cantidad_iters = imgFinal.shape[0]
print('Color alterados: ', colorLabels)
print('Cantidad diferentes labels: ', len(labesDiferentes))
print('Cantidad de Iteraciones ', imgFinal.shape[0])

for j in range(cantidad_labels):
    for i in range(cantidad_iters):
        if otherlabel.labels_[i] == j:
            # if otherlabel.labels_[i] < 5:
            #    imgFinal[i, :] = 255
            # print('label ', otherlabel.labels_[i], '   valor de iter', j, '   valor de color: ', colorLabels[j])
            imgFinal[i, :] = colorLabels[j]

histFinal = plt.hist(imgFinal[:, 0], bins=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                     range=(0, 1), edgecolor='black', alpha=0.7, color='salmon')
imgFinal = imgFinal.reshape(c.shape)
print('Shape imgFinal: ', imgFinal.shape)
# aux = np.clip(aux*255,0.0,1.1)
plt.figure(0)
plt.imshow(imgFinal[:, :, 0], cmap='gray')
plt.show()

imgFinalA = cv.convertScaleAbs(imgFinal[:, :, 0])


# global thresholding
ret1, th1 = cv.threshold(imgFinalA, 127, 255, cv.THRESH_BINARY)
# Otsu's thresholding
ret2, th2 = cv.threshold(imgFinalA, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv.GaussianBlur(imgFinalA, (5, 5), 0)
ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

plt.imshow(th2, 'gray')
plt.show()

cv.destroyAllWindows()
cv.imshow("Original", th3)
kernelSize = (7, 7)
# loop over the kernels sizes
kernel = cv.getStructuringElement(cv.MORPH_RECT, kernelSize)
opening = cv.morphologyEx(th3, cv.MORPH_OPEN, kernel)
cv.imshow("Opening: ({}, {})".format(
    kernelSize[0], kernelSize[1]), opening)
cv.waitKey(0)


contours, hierarchy = cv.findContours(th2, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_L1)
print("Numero de contornos encontrados: " + str(len(contours)))

cv.drawContours(th2, contours, -1, (127, 127, 127), 5)
cv.imshow("Contours", th2);

for i in range(len(contours)):
    contorno_prueba = contours[i]
    area = cv.contourArea(contorno_prueba)
    perimeter = cv.arcLength(contorno_prueba, True)

    if area > 51:
        print('Index: ', i)
        print('Area: ', area)
        print('Perimetro: ', perimeter)

cv.waitKey(0)
