import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
from src import a_lib as lib
from sklearn.cluster import estimate_bandwidth
from sklearn.datasets import make_blobs
from skimage import morphology as morp
import PixelArithmetic as k

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

def main():
    n_cluster = 5
    X, y_true = make_blobs(n_samples=50, centers=n_cluster, cluster_std=1.2, random_state=7)
    print(X.shape)
    print(X)

    model = MeanShift(epsilon=3, iters= 100)
    model.fit(X)
    labels = model.predict(X)
    centroids = model.centroids_

    plt.style.use('classic')
    plt.scatter(X[:,0], X[:,1], c = labels, s=100)
    plt.scatter(centroids[:,0], centroids[:,1], c='r', s=50, marker= 'x')
    plt.show()

if __name__ == '__main__':
    main()