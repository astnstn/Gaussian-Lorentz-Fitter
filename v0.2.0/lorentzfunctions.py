import numpy as np
def lorentz(x, A, u, T):
	return (A) / ( 1 + ( ((x - u)/(T/2))**2 )) 

def lorentzcombined(x,A0, u0, T0, A1, u1, T1, A2, u2, T2, C):
	return lorentz(x, A0, u0, T0) + lorentz(x, A1, u1, T1) + lorentz(x, A2, u2, T2) + C