import imageio.v2
import matplotlib.pyplot as plt
import numpy as np
import skimage.morphology

import src.PixelArithmetic as k
from src.a_lib import laplacian_filter as lp
from src.a_lib import to_yiq,to_rgb,mediana_filter
from sklearn.cluster import MeanShift as sms
from sklearn.cluster import estimate_bandwidth
import cv2

def euclidean_distance(x,center):
    return np.sqrt(np.sum((x-center)**2))

def gaussian_kernel(distance, epsilon):
    return (1/(epsilon * np.sqrt(2*np.pi))) * np.exp(-0.5*((distance/epsilon))**2)

def neighbourhood(X, x_centroid, epsilon):
    in_neighbourhood = []
    for x in X:
        distance = euclidean_distance(x, x_centroid)
        if distance <= epsilon:
            in_neighbourhood.append(x)
    return in_neighbourhood

class MeanShift:
    def __init__(self, epsilon, iters=100):
        self.epsilon = epsilon
        self.iters = iters
        self.centroids_ = []
    def fit(self,_X):
        X = np.copy(_X)

        for _ in range(self.iters):
            print('Iteracion numero: ',_)
            for i in range(len(X)):
                neighbours = neighbourhood(X, X[i], self.epsilon)

                m_num = 0
                m_dem = 0

                for neighbour in neighbours:
                    distance = euclidean_distance(neighbour, X[i])
                    weight = gaussian_kernel(distance, self.epsilon)
                    m_num += (weight * neighbour)
                    m_dem += weight

                X[i] = m_num/m_dem
        self.centroids_ = np.copy(X)



    def predict(self,X):
        labels = []

        for x in X:
            distances = [euclidean_distance(x, center) for center in self.centroids_]
            labels.append(distances.index(min(distances)))

        return labels


im = imageio.v2.imread('../../resource/p1.png')
#im = np.clip(im/255,0.0,1.0)
im = np.clip(im,0,255)
#im = k.RGBtoYIQ_array(im)

t = np.copy(im)
#t = to_yiq(t)
#t = cv2.medianBlur(imc,5)
#t = cv2.medianBlur(t,3)
#t = to_rgb(np.clip(t/255,0.0,1.0))
#plt.imshow(t)
#plt.show()

print(t.shape)
a = np.stack((t[:,:,0],t[:,:,1],t[:,:,2]), axis=-1)
print(a.shape)

#r={}
#for i in range(a.shape[0]):
#    for j in range(a.shape[1]):
#        r[(i,j)]=[a[i,j,0],a[i,j,1]]

#print(len(r))

#fig, axs = plt.subplots(1, 2, figsize=(10, 4))
#fig = plt.figure()
b = np.column_stack((a[:,:,0].flatten(),a[:,:,1].flatten(),a[:,:,2].flatten()))

#model = MeanShift(epsilon=28,iters=25) #0.00023
#model.fit(b)
#labels = model.predict(b)
#centroids = model.centroids_

print(b.shape)
#print('Cantidad de labels: ',len(np.unique(labels)))
#print(np.unique(labels))
print('entre')
#bandwidth = estimate_bandwidth(b, quantile=1, n_samples=1000)
#print('bandiwhth valor ',bandwidth)
otherlabel = sms(bandwidth=29, bin_seeding=True).fit(b)
print('Sali')
print(b.shape)
print('Cantidad de labels de sklearn: ',len(np.unique(otherlabel.labels_)))
print(np.unique(otherlabel.labels_))

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(b[:,0], b[:,1], b[:,2], c=labels)
#ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c='r', s=50, marker= 'x')
#ax.set_xlabel('Eje R')
#ax.set_ylabel('Eje G')
#ax.set_zlabel('Eje B')
#plt.show()
#
#print(len(labels))

for i in range(len(b)):
    if otherlabel.labels_[i] == 0:
        b[i] = 0
    if otherlabel.labels_[i] == 1:
        b[i] = 0
    if otherlabel.labels_[i] == 2:
        b[i] = 255
c = b.reshape(a.shape)
c = np.clip(c/255,0.0,1.1)
print(a.shape,'     ',c.shape)
print(np.array_equal(a, c))
plt.imshow(c)
plt.show()

d = skimage.morphology.opening(c)
#d = skimage.morphology.dilation(d)
print(d.shape)
plt.imshow(d)
plt.show()
#d = lp(to_yiq(c),4)
#d = to_rgb(d)
#plt.imshow(d)
#plt.show()

