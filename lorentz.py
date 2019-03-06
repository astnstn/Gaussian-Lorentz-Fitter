import numpy as np
def lorentz(x, A, u, T):
	return (A) / ( 1 + ( ((x - u)/(T/2))**2 )) 

def lorentzcombined(x, A0, u0, T0):
	return lorentz(x, A0, u0, T0)