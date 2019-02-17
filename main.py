import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import gaussfit


x, y = np.loadtxt("us1penny.txt", skiprows=1, unpack = True) #imports x and y data



fig = plt.figure() #create fig
ax = fig.add_subplot(111) #create axes for plot and buttons
button_add_ax = plt.axes([0.78, 0.79, 0.1, 0.075]) 
button_fit_ax = plt.axes([0.78, 0.69, 0.1, 0.075])
ax.plot(x,y, '.') #plot data as points


def plotfit(opt, cov): #function to plot fit found for data
    global x
    xlin = np.linspace(min(x), max(x), 1000) #create x line data
    import gauss #import generated gaussian function
    ax.plot(xlin, gauss.gausscombined(xlin, *opt)) #plot with optimal parameters
    plt.draw()



add = False #adding points toggle
peaknum = 0 #number of peaks added
amps = [ ] #amplitudes of peaks
means = [ ] #means
stds = [ ] #standard deviations

def addpoint(event): #"add" button pressed
    global add 
    print("Add pressed!")
    
    add = not add #toggle button and change color
    if add == True:
        b_add.color = '0.4'
    else:
        b_add.color = '0.85'
    return

def applyfit(event): #calls gaussfit function 
    opt, cov = gaussfit.fit(x, y, peaknum, amps, means, stds)  #finds optimal parameters using selected guesses
    print("Fit pressed!")

    plotfit(opt, cov) #calls the plotting function
    
    return opt, cov #returns optimal parameters and errors if needed



def on_clicked(event): #when the mouse is clicked
    global ix, iy
    global add
    global peaknum
    button = event.button #checks which mouse button was clicked
    
    ix, iy = event.xdata, event.ydata
    
    if add == True and button == 3: #if the button was rmb and add button is toggled on 
            
        ax.plot(ix, iy, 'o', color='red') #plots the point 
        amps.append(iy) #appends point x and y coords to mean and amplitudes
        means.append(ix)
        stds.append(0.2) #standard deviation set to 0.2 (placeholder)
        peaknum += 1 #number of peaks + 1
        plt.draw()
    
        
b_add = Button(button_add_ax, "Add", color='0.85', hovercolor='0.95') #creates "add" button
b_add.on_clicked(addpoint)

b_fit = Button(button_fit_ax, "Fit") #creates "fit" button
b_fit.on_clicked(applyfit)

cid = fig.canvas.mpl_connect('button_press_event', on_clicked) #mouse click event

plt.show()