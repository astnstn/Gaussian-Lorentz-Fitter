import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad



def fit(x, y, pnum, amps, means, stds): #main fitting function 
    
    
    file = open("gauss.py", 'w') #opens py file 
    
    #this code writes a function in a py file suitable to the parameters passed to the function
    file.write("import numpy as np\n") 
    file.write("def gauss(x, A, u, o):\n\treturn A*np.exp(-(((x-u)**2)/(2*(o**2)))) \n\n")
    file.write("def gausscombined(x, ")
    
    for i in range(pnum - 1):
        file.write("A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ", ")
        
    file.write("A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "o" + str(pnum - 1) + "):")
        
    file.write("\n")
    file.write("\t")
    file.write("return ")
    for i in range(pnum - 1):
        file.write("gauss(x, " + "A" + str(i) + ", " + "u" + str(i) + ", " + "o" + str(i) + ") + ")
    file.write("gauss(x, " + "A" + str(pnum - 1) + ", " + "u" + str(pnum - 1) + ", " + "o" + str(pnum - 1) + ")")
    
    file.close()
    
    import gauss #imports the generated py file 
    

    
    
    guesses = np.array([]) #empy array for parameter estimates
    
    
    for i in range(pnum): #loads array
        guesses = np.append(guesses, amps[i])
        guesses = np.append(guesses, means[i])
        guesses = np.append(guesses, stds[i])
    
    try: #attempts to find optimal parameters using the gauss function generated, guesses, and the data
        popt, pcov = curve_fit(gauss.gausscombined, x , y, guesses) #attempts to find optimal parameters based on function and guesses
    except RuntimeError:
        print("could not fit")
        return
    
    return popt, pcov #returns optimal parameters

