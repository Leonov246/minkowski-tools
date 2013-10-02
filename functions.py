import numpy as np
import math

def minkowski_sum( A, B ):
	C = []
	for Apoints in A:
		for Bpoints in B:
			C.append(Apoints + Bpoints)
	return np.array(C)

def sort_np_array( A, dimension=1, index=1, reverse=0 ):
	'''
	Sort a numpy array by the dimension "dimension" where 1 = by columns and 0 = by rows. "index" specifies which row/column number to sort by (i.e. for euclidian data, 1 = yaxis and 0 = xaxis)
	Note: argsort only sorts by rows, so to sort by columns the array must be transposed.
	'''
	a = np.array(A)
	#print a
	if dimension == 1:
		a = a.transpose()
	idx = np.argsort(a[index])
	if reverse:
		idx = idx[::-1]
	#pdb.set_trace()
	b = a[:,idx]
	if dimension == 1:
		b=b.transpose()
	return b
	

def convex_build_figure( A ):
	'''
	building a list of points in a figure under the assumption that the figure is convex at all points.  
	'''
	a = sort_np_array( A )
	#print a
	first = a[0]
	pre = first
	post = first
	other = []
	prelast = first
	postlast = first
	for i, entry in enumerate(a):
		if  entry[0] > first[0] or (entry[0] == a[0][0] and entry[1] > a[0][1]):
			pre = np.column_stack( (pre, entry) )
		elif entry[0] != first[0] and entry[0] < postlast[0]:
			postlast = entry
			post = np.column_stack( (entry, post) )
		else:
			if entry[0] != first[0] and entry[1] != first[1]:
				other.append(entry)
	#import pdb; pdb.set_trace()
	if not other: #if other is empty
		out = np.column_stack( (pre, post) ).transpose()
	else:
		other = sort_np_array( other, index=0, reverse=1 )
		other = other.transpose()
		out = np.column_stack( (pre, other, post) ).transpose()
	return out			
			
def translate( v, dim=0, dist=1 ):
	'''
	translation for a two-dimensional vector
	'''
	return v[dim] + dist

def create_rotation_matrix( axis, angle, dim=2 ):
	if dim == 2:
		mat = np.array( [ [np.cos( angle ), -np.sin( angle ) ],[ np.sin( angle ), np.cos( angle ) ] ] )
	else:
		if axis == 0:
			mat = np.array([ [ 1, 0, 0 ], [ 0, np.cos( angle ), -np.sin( angle ) ], [ 0, np.sin( angle ), np.cos( angle ) ] ])
		elif axis == 1:
			mat = np.array([ [ np.cos( angle ), 0, np.sin( angle ) ], [ 0, 1, 0 ], [ -np.sin( angle ), 0, np.cos( angle ) ] ])
		else:
			mat = np.array([ [ np.cos( angle ), -np.sin( angle ), 0 ], [ np.sin( angle ), np.cos( angle ), 0 ], [ 0, 0, 1 ] ])
	return mat

def rotate( v, axis, angle, dim=2 ):
	rmat = create_rotation_matrix( axis, angle, dim )
	vrot = np.dot(rmat, v)
	return vrot

def rotate_shape( A, axis, angle, dim=2 ):
	Arot = np.array([])
	center = find_center( A )
	print center
	Alen = len(A)
	Ap = np.copy(A)
	translate_shape( Ap, 0, -center[0] )
	translate_shape( Ap, 1, -center[1] )
	for vec in Ap:
		vrot = rotate( vec, axis, angle, dim )
		Arot = np.append( Arot, vrot )
	Arot = np.reshape( Arot, (Alen, 2) )
	translate_shape( Arot, 0, center[0] )
	translate_shape( Arot, 1, center[1] )
	return Arot

def translate_shape( A, axis, dist ):
	Atrans = A.transpose()
	Atrans[axis] += dist
	return Atrans.transpose()

def find_center( A ):
	dims = len(A[0])
	print A[0]
	center = np.zeros_like( A[0] )
	center = center.astype( float )
	Acols = A.transpose()
	#import pdb; pdb.set_trace()
	for i in range( dims ):
		print np.mean( Acols[i])
		center[i] = np.mean( Acols[i] )
		print center[i]
	print center
	return center

def sort_truncate( A, reverse ):
	sort_np_array( A )
	

def build_convex_object( A ):
	Atrans = A.transpose()
	idx_maxx = Atrans[0].argmax()
	idx_maxy = Atrans[1].argmax()
	idx_minx = Atrans[0].argmin()
	idx_miny = Atrans[1].argmin()

	x_max = A[ idx_maxx ]
	x_min = A[ idx_minx ]
	y_max = A[ idx_maxy ]
	y_min = A[ idx_miny ]

	q1 = []
	q2 = []
	q3 = []
	q4 = []

	for point in A:
		if point[0] >= y_min[0] and point[1] <= x_max[1]:
			q1.append( point )
		elif point[1] > x_max[1] and point[0] > y_max[0]:
			q2.append( point )
		elif point[1] > x_min[1] and point[0] < y_max[0]:
			q3.append( point )
		else:
			q4.append( point )

def discard_and_sort( A, section = 'ul'):
	'''
	takes sorted list A and returns only the points outside a partitioned area created by a line from min to max A. 'section' refers to the upper-left or lower-right section of the partitioned rectangle
	'''
	if len(A) == 2:
		return A
	Aout = []
	Atrans = A.transpose()
	max_idx = Atrans[0].argmax()
	min_idx = Atrans[0].argmin()
	Amax = A[ max_idx ]
	Amin = A[ min_idx ]
	slope = (Amax[1] - Amin[1])/(Amax[0] - Amin[0])
	for point in A:
		if (point[0] == Amax[0] and point[1] == Amax[1]) or (point[0] == Amin[0] and point[1] == Amin[1]):
			Aout.append( point )
		else:
			#import pdb; pdb.set_trace()
			testpoint = point_slope( point[0], slope, Amax[0], Amax[1] )
			if section == 'ul' or section == 'ur':
				if testpoint > point[1]:
					Aout.append( point )
			elif section == 'll' or section == 'lr':
				if testpoint < point[1]:
					Aout.append( point )
	Aout = np.array(Aout)
	Alen = len(Aout)
	if Alen <= 2:
		return Aout
	Amid = math.floor(Alen/2)
	Aleft = Aout[:Amid+1]
	Aright = Aout[Amid:]
	if Aleft.size == 0 or Aright.size == 0:
		import pdb; pdb.set_trace()
	#import pdb; pdb.set_trace()
	Rleft = discard_and_sort( Aleft, section )
	Rright = discard_and_sort( Aright, section )
	#print 'Left:'
	#print Rleft
	#print 'Right:'
	#print Rright
	#import pdb; pdb.set_trace()
	Aret = np.concatenate( [Rleft, Rright] ) 
	return Aret
	
def unique(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1) 
    return a[ui]
			
	
def point_slope( x, slope, x0, y0 ):
	return slope*(x-x0) + y0

def find_slope( p0, p1 ):
	return (p1[1] - p0[1])/(p1[0]-p0[0])

def calc_slopes( A, pivotpoint ):
	slopes = np.zeros( len(A) )
	for i, point in enumerate(A):
		#import pdb; pdb.set_trace()
		slopes[i] = find_slope( point, pivotpoint )
	return slopes
		
def find_extreme_idx( a, order='min' ):
	'''
	finds the extreme point (min or max) in numpy array a and returns its index. The function ignores NaNs (because of how argsort sorts the NaN)
	'''
	if order == 'max':
		a = -a
	idx = np.argsort(a)
	minidx = idx[0]
	return minidx		

def find_increasing_perimeter(A):
	'''
	finds the convex perimeter of array A. By default it will find the lower left perimeter of the set of points A entered.
	'''
	Amax = A[len(A)-1]
	Amin = A[0]
	maxslopes = calc_slopes(A, Amax)
	minslopes = calc_slopes(A, Amin)
	maxidx = find_extreme_idx(maxslopes, order='max')
	minidx = find_extreme_idx(minslopes)
	if Amin[0] == A[maxidx][0] and Amin[1] == A[maxidx][1] and Amax[0] == A[minidx][0] and Amax[1] == A[minidx][1]:
		retarray = np.array([Amin, Amax])
	elif maxidx == minidx:
		retarray =  np.array( [ Amin, A[maxidx], Amax ] )
	elif maxidx == minidx + 1:
		retarray = np.array( [ Amin, A[minidx], A[maxidx], Amax ] )
	else:
		Adis = discard_lessthan(A[minidx:maxidx+1])
		retarray = np.vstack( (Amin, find_increasing_perimeter(Adis), Amax) )
	return retarray

def discard_lessthan(A):
	'''
	This function discards all points with x positions less than that of the first point. It assumes the input has been sorted by y values. The input is a numpy 2-D array where all where rows represent x-y pairs of points.
	'''
	Areduced = []
	for points in A:
		if points[0] >= A[0][0]:
			Areduced.append(points)
	return np.array(Areduced)

def build_perimeter(A):
	'''
	Builds the entire perimeter of object A assuming a convex shape.
	'''
	lowslice = find_increasing_perimeter(A)
	AT = np.copy(A.T)
	AT[1] = -AT[1]
	B = find_increasing_perimeter(AT.T)
	BT = np.copy(B.T)
	BT[1] = -BT[1]
	highslice = np.copy(BT.T[::-1])
	retarr = np.vstack((lowslice, highslice))
	return retarr
	
