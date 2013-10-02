import numpy as np
import math

class simplex():
    def __init__(self, A, B):
        return 0

def gjk(A, B):
    simplex = initialize_simplex(A, B):
    return 0

def initialize_simplex():
	dots = mass_dot(A[0], B)
	maxidx = dots.argmax()
	minidx = dots.argmin()
	simplex = np.array([A[0]-B[maxidx], A[0]-B[minidx]])
    return simplex

def compute_min_norm():
    return 0

def reduce():
    return 0

def mass_dot(pivot, A):
	products = []
	for point in A:
		products.append(np.dot(pivot, point))
	return np.array(products)
