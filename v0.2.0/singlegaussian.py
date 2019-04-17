import numpy as np

def gauss(x, A, u, o, C):
	return A*np.exp(-(((x-u)**2)/(2*(o**2)))) + C