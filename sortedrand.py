import numpy as np
import matplotlib.pyplot as plt
import math

npoints = 100
'''
offset = 1
rscale = 0.3
lscale = 0.0
x = np.linspace( 0, 1, npoints )
x = lscale*x
y = np.copy(x)
rndx = rscale*(offset + np.random.rand( npoints ))
rndy = rscale*(np.random.rand( npoints ) - offset )

line = np.array([ x+rndx, y+rndy ]).T
#line = np.array([ rndx, rndy ]).T
'''
maxr = 1
angle = 6.28*np.random.rand(npoints)
radius = maxr*np.random.rand(npoints)

cangle = np.cos(angle)
sangle = np.sin(angle)

x = radius*cangle
y = radius*sangle

line = np.array([x, y]).T

a = line
aT = a.T
idx = np.argsort(aT[0])
bT = aT[:, idx]
b = bT.T

#plt.scatter( bT[0], bT[1] )
#plt.show()

from functions import calc_slopes
from functions import find_extreme_idx
from functions import find_increasing_perimeter
from functions import build_perimeter



B = build_perimeter(b)
print B

plt.scatter(bT[0], bT[1])
plt.plot( B.T[0], B.T[1])
#plt.plot(BperT[0], BperT[1])
#plt.plot(Borig.T[0], Borig.T[1])
plt.show()

'''
import pdb; pdb.set_trace()
slopes = calc_slopes( b, b[0] )
newidx = find_extreme_idx( slopes )
print newidx
print slopes[ newidx ]
print math.isnan( slopes[newidx] )
'''
