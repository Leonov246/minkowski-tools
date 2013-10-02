import numpy as np
import matplotlib.pyplot as plt
from functions import sort_np_array as npsort
from functions import convex_build_figure as cvbuild
from functions import rotate_shape
from functions import minkowski_sum

#b = [[4, 4], [1, 6], [3, 2], [3, 6], [1, 2], [0, 4], [2, 7], [2, 1]]
b = [ [2, 4], [4, 4], [3, 4-np.sqrt(2)] ]
b = np.array(b)
c = cvbuild(b)
crot = rotate_shape( b, 0, np.pi/4, 2 )
print crot
#import pdb; pdb.set_trace()
#print ' '
new = minkowski_sum( crot, -b )
anothernew = minkowski_sum( -crot, b )
again = minkowski_sum( -b, crot )
again = cvbuild( again ).transpose()

anothernew = cvbuild( anothernew ).transpose()
crot = cvbuild( crot )
new = cvbuild( new )
new = new.transpose()
#print ' '
#print crot
c = c.transpose()
crot = crot.transpose()
plt.plot( c[0], c[1] )
plt.plot( crot[0], crot[1] )
plt.plot( new[0], new[1] )
plt.plot( anothernew[0], anothernew[1] )
plt.plot( again[0], again[1] )
plt.show()
