import numpy as np
import mathfunctions

class Gaussian(mathfunctions.MathFunction):
    def __init__(self, amp, mean, sigma):
        def gauss(x, amp, mean, sigma):
            return amp*np.exp(-(((x-mean)**2)/(2*(sigma**2))))
        super().__init__(gauss, params = (amp, mean, sigma), name = "GaussianFunction")
        
class Line(mathfunctions.MathFunction):
    def __init__(self, m, c):
        def line(x, m, c):
            return m*x + c
        super().__init__(line, params = (m, c), name = "LinearFunction")
    

