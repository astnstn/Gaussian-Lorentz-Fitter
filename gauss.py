import numpy as np
def gauss(x, A, u, o):
	return A*np.exp(-(((x-u)**2)/(2*(o**2)))) 

def gausscombined(x, A0, u0, o0, A1, u1, o1, A2, u2, o2):
	return gauss(x, A0, u0, o0) + gauss(x, A1, u1, o1) + gauss(x, A2, u2, o2)