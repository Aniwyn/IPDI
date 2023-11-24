import imageio.v2
import matplotlib.pyplot as plt
import numpy as np
import skimage.morphology
from sklearn.cluster import MeanShift as skMeanShift
from skimage.morphology import skeletonize
from skimage import measure
import src.PixelArithmetic as k

im = imageio.v2.imread('../../resource/S2.png')
im = np.clip(im,0,255)

t = np.copy(im)
print('T ', t.shape)

a = np.stack((t[:,:,0],t[:,:,1],t[:,:,2]), axis=-1)
print('A', a.shape)

b = np.column_stack((a[:,:,0].flatten(),a[:,:,1].flatten(),a[:,:,2].flatten()))
print(b.shape)

print('entre')
otherlabel = skMeanShift(bandwidth=60, bin_seeding=True).fit(b)
#29 con f2.png
#15 con 0408.png
#14 con 0408.png
#14 con 0508Raiz.png
#13 con 0508.png
print('Sali')
print(b.shape)
print('Cantidad de labels de sklearn: ',len(np.unique(otherlabel.labels_)))
print(np.unique(otherlabel.labels_))

#colors = []
#for j in range(len(np.unique(otherlabel.labels_))):
#    rc = []
#    gc = []
#    bc = []
#    aux = np.copy(b)
#    for i in range(aux.shape[0]):
#        if otherlabel.labels_[i] == j:
#            rc.append(aux[i,0])
#            gc.append(aux[i,1])
#            bc.append(aux[i,2])
#    colors.append([mean(rc),mean(gc),mean(bc)])

resutls = []
for j in range(len(np.unique(otherlabel.labels_))):
    aux = np.copy(b)
    for i in range(aux.shape[0]):
        if otherlabel.labels_[i] == j:
            aux[i] = 255
        else:
            aux[i] = 0
    aux = aux.reshape(a.shape)
    aux = np.clip(aux/255,0.0,1.1)
    resutls.append(aux)
    print('Figura nro: ', j)

plt.figure(0)
plt.imshow(resutls[1])
plt.show()



pond_binary = resutls[1][:,:,0]
skeleton = skeletonize(pond_binary)
print(pond_binary.shape)

# display results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(pond_binary, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

exit()

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()

# Find contours at a constant value of 0.8
contours = measure.find_contours(pond_binary, 0.9)
print("Numero de contornos encontrados: " + str(len(contours)))

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(pond_binary, cmap=plt.cm.gray)

for contour in contours:
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

contorno_prueba = np.array(contours[0])
print('Contorno de prueba: ', contorno_prueba.shape)
print(contorno_prueba)

shape_features = []

shape_features[0] = measure.perimeter(contorno_prueba,neighborhood=4)

print('Perimetro: ', shape_features[0])