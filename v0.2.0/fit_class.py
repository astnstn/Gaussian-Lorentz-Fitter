import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
import pickle

def gaussian_function_string(peaks):
        string =       (
                            "import numpy as np\n"
                            "def gauss(x, A, u, o):\n\treturn A*np.exp(-(((x-u)**2)/(2*(o**2)))) \n\n"
                            "def gausscombined(x,"
                            )
        
        for i in range(peaks - 1):
            
            string += "A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ", "
        
        string += "A" + str(peaks - 1) + ", " + "u" + str(peaks - 1) + ", " + "o" + str(peaks - 1) + ", C):"
        string += "\n\treturn "
        
        for i in range(peaks - 1):   
            
            string += "gauss(x, " + "A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ") + "
        string += "gauss(x, " + "A" + str(peaks - 1) + ", " + "u" + str(peaks - 1) + ", " + "o" + str(peaks - 1) + ") + C"
        
        return string
    
    
def lorentzian_function_string(peaks):
        string =       (
                            "import numpy as np\n"
                            "def lorentz(x, A, u, T):\n\treturn (A) / ( 1 + ( ((x - u)/(T/2))**2 )) \n\n"
                            "def lorentzcombined(x,"
                            )
                            
        for i in range(peaks - 1):
            
            string += "A" + str(i) + ", " + "u" + str(i) + ", " + "T" + str(i) + ", "
        
        string += "A" + str(peaks - 1) + ", " + "u" + str(peaks - 1) + ", " + "T" + str(peaks - 1) + ", C):"
        string += "\n\treturn "
        
        for i in range(peaks - 1):     
            string += "lorentz(x, " + "A" + str(i) + ", " + "u" + str(i) + ", " + "T" + str(i) + ") + "
        string += "lorentz(x, " + "A" + str(peaks - 1) + ", " + "u" + str(peaks - 1) + ", " + "T" + str(peaks - 1) + ") + C"
        
        return string

        
class Fit:
    def __init__(self, data, estimates):
        self.data = data
        self.xdata = data[:,0]
        self.ydata = data[:,1]
        
        self.type = None
        
        self.estimates = estimates
        self.peaks = int((len(estimates) - 1)/3)
        
        self.xspace = np.linspace(min(self.xdata), max(self.xdata), 1000)
        self.yspace = None
        
        self.opt = None
        self.cov = None
    
    def fitgaussian(self):
        file = open("gaussfunctions.py", "w")
        file.write(gaussian_function_string(self.peaks))
        file.close()
        
        self.type = "gaussian"

        
        import gaussfunctions
        popt, pcov = curve_fit(gaussfunctions.gausscombined, self.xdata , self.ydata, self.estimates)
        self.opt, self.cov = popt, pcov
        
        self.yspace = gaussfunctions.gausscombined(self.xspace, *self.opt)
        
    def fitlorentzian(self):
        file = open("lorentzfunctions.py", "w")
        file.write(lorentzian_function_string(self.peaks))
        file.close()
        
        self.type = "lorentz"

        
        import lorentzfunctions
        popt, pcov = curve_fit(lorentzfunctions.lorentzcombined, self.xdata , self.ydata, self.estimates)
        self.opt, self.cov = popt, pcov
        
        self.yspace = lorentzfunctions.lorentzcombined(self.xspace, *self.opt)
        
    
    def save_fit(self, name):
        file = open(name + ".txt", 'wb')
        pickle.dump(self, file)
        file.close()
    

        
        
    
    
    




