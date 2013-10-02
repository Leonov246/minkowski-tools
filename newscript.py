import numpy as np
from functions import discard_and_sort
from functions import unique
import matplotlib.pyplot as plt

arr = np.random.rand( 40, 2 )
xarr =  np.array([[0. ,0. ], [1. ,1. ]])
import pdb; pdb.set_trace()
arr = np.concatenate([xarr, arr])
print arr
#arr = np.array([[.4, .5], [.5, .4], [.1, .1], [.9, .9]])
plt.scatter(arr.T[0], arr.T[1])
plt.show()

arridx = np.argsort(arr.T[0])
arr = (arr.T[:,arridx]).T

#import pdb; pdb.set_trace()
newarr = discard_and_sort( arr, 'ul' )
#import pdb; pdb.set_trace()
uarr = unique( newarr )

plt.scatter(arr.T[0], arr.T[1])
plt.plot(uarr.T[0], uarr.T[1], color='red')
plt.show()

#print newarr
#print uarr
