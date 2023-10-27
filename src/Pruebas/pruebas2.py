import imageio.v2
import numpy as np
import PixelArithmetic as k

test = {
    (0,0): 'hola',
    (0,1): 'chau'
}

print(test[(0,1)])

im = imageio.v2.imread('../../resource/Figura-2-Imagen-binaria-con-cinco-objetos.png')
im = np.clip(im/255,0.0,1.0)
im = k.RGBtoYIQ_array(im)

t = np.copy(im)
print(t.shape)
a = np.stack((t[:,:,0],t[:,:,1]), axis=-1)
print(a.shape)

r={}
for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        r[(i,j)]=[a[i,j,0],a[i,j,1]]

print(len(r))
