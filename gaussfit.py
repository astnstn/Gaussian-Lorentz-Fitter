import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(filename='fitterlog.txt', filemode = 'w+', level=logging.DEBUG)

def fit(x, y, pnum, amps, means, stds): #main fitting function 
    
    logging.info("gaussfit.fit started:")
    logging.info("number of peaks: {:.0f}".format(pnum))
    logging.info("amps: {:.0f}".format(len(amps)))
    logging.info("means: {:.0f}".format(len(means)))
    logging.info("stds: {:.0f}".format(len(stds)))
    
    file = open("gauss.py", 'w') #opens py file 
    
    #this code writes a function in a py file suitable to the parameters passed to the function
    file.write("import numpy as np\n") 
    file.write("def gauss(x, A, u, o):\n\treturn A*np.exp(-(((x-u)**2)/(2*(o**2)))) \n\n")
    file.write("def gausscombined(x, ")
    
    logging.info("gauss function arguments:")
    for i in range(pnum - 1):
        file.write("A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ", ")
        logging.info("A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ", ")
        
    file.write("A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "o" + str(pnum - 1) + "):")
        
    logging.info("A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "o" + str(pnum - 1))   
    
    
    file.write("\n")
    file.write("\t")
    file.write("return ")
    for i in range(pnum - 1):
        file.write("gauss(x, " + "A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ") + ")
        
    file.write("gauss(x, " + "A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "o" + str(pnum - 1) + ")")
    
    file.close()
    logging.info("gauss file written and closed")
    import gauss #imports the generated py file 
    
    logging.info("gauss imported")
    
    
    guesses = np.array([]) #empy array for parameter estimates
    
    
    for i in range(pnum): #loads array
        guesses = np.append(guesses, amps[i])
        guesses = np.append(guesses, means[i])
        guesses = np.append(guesses, stds[i])
    
    logging.info("estimates loaded")
    logging.info("number of estimates: {:.0f}".format(len(guesses)))
    
    
    try: #attempts to find optimal parameters using the gauss function generated, guesses, and the data
        popt, pcov = curve_fit(gauss.gausscombined, x , y, guesses) #attempts to find optimal parameters based on function and guesses
    except RuntimeError:
        print("could not fit")
        logging.info("Run Time Error")
        return
    except TypeError:
        print("could not fit")
        logging.info("Type Error")        
        return
    return popt, pcov #returns optimal parameters

def lorentzfit(x, y, pnum, amps, means, stds):
    Ts = [t*2.4 for t in stds]
    
    
    file = open("lorentz.py", 'w') #opens py file 
    
    #this code writes a function in a py file suitable to the parameters passed to the function
    
    
    file.write("import numpy as np\n") 
    file.write("def lorentz(x, A, u, T):\n\treturn (A) / ( 1 + ( ((x - u)/(T/2))**2 )) \n\n")
    file.write("def lorentzcombined(x, ")
    
    logging.info("lorentz function arguments:")
    for i in range(pnum - 1):
        file.write("A" + str(i) + ", " + "u" + str(i) + ", " + "T" + str(i) + ", ")
        logging.info("A" + str(i) + ", " + "u" + str(i) + ", " + "T" + str(i) + ", ")
        
    file.write("A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "T" + str(pnum - 1) + "):")
        
    logging.info("A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "T" + str(pnum - 1))   
    
    
    file.write("\n")
    file.write("\t")
    file.write("return ")
    for i in range(pnum - 1):
        file.write("lorentz(x, " + "A" + str(i) + ", " + "u" + str(i) + ", " + "T" + str(i) + ") + ")
        
    file.write("lorentz(x, " + "A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "T" + str(pnum - 1) + ")")
    
    file.close()
    logging.info("lorentz file written and closed")
    
    import lorentz #imports the generated py file 
    
    logging.info("lorentz imported")
    
    
    guesses = np.array([]) #empy array for parameter estimates
    
    
    for i in range(pnum): #loads array
        guesses = np.append(guesses, amps[i])
        guesses = np.append(guesses, means[i])
        guesses = np.append(guesses, stds[i]*2.4)
    
    logging.info("estimates loaded")
    logging.info("number of estimates: {:.0f}".format(len(guesses)))
    
    
    try: #attempts to find optimal parameters using the gauss function generated, guesses, and the data
        popt, pcov = curve_fit(lorentz.lorentzcombined, x , y, guesses) #attempts to find optimal parameters based on function and guesses
    except RuntimeError:
        print("could not fit")
        logging.info("Run Time Error")
        return
    except TypeError:
        print("could not fit")
        logging.info("Type Error")        
        return
    return popt, pcov #returns optimal parameters
    

