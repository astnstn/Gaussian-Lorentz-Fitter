import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
import logging

import gaussfit

x, y = np.loadtxt("lorrentztest.txt", skiprows=1, unpack = True) #imports x and y data


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(filename='fitterlog.txt', filemode = 'w', level=logging.DEBUG)



class plot_image: #plot object
    def __init__(self): #contains fit object with data points, buttons, conditions for buttons 
        
        logging.info("plot created")
        
        self.add = False 
        
        self.fit_obj = None 
        self.std_val = None
        self.amp_s_val = 2.5
        self.figure = plt.figure(figsize=(8, 8)) #plot figure
        self.axis = self.figure.add_subplot(111) #subplot
        self.axis.set_ylim(min(y), max(y))
        self.axis.set_xlim(min(x), max(x))
        
        self.button_add_ax = plt.axes([0.78, 0.79, 0.1, 0.075])  #button axes
        self.button_fit_ax = plt.axes([0.78, 0.69, 0.1, 0.075])
        self.button_set_ax = plt.axes([0.78, 0.59, 0.1, 0.075])
        self.slider_std_ax = plt.axes([0.15, 0.1, 0.25, 0.03]) 
        self.slider_mean_ax = plt.axes([0.15, 0.2, 0.25, 0.03])
        self.slider_amp_ax = plt.axes([0.15, 0.3, 0.25, 0.03])
        
        plt.subplots_adjust(bottom=0.45)  
        
        #create buttons and assign functions
        self.b_add = Button(self.button_add_ax, "Add", color='0.95', hovercolor='0.8')
        self.b_add.on_clicked(self.add_point_clicked) 
        
        self.b_fit = Button(self.button_fit_ax, "Fit") 
        self.b_fit.on_clicked(self.applyfit)

        
        
        self.b_set = Button(self.button_set_ax, "Set")
    
    
        self.s_std = None
        
        
        self.s_amp = Slider(self.slider_amp_ax, 'Amp', 0, 1, valinit = 0.5)
        self.s_amp.on_changed(self.amp_slider_changed)
        self.s_mean = Slider(self.slider_mean_ax, "Mean", 0, 1, valinit = 0.5)
        
        
        #mouse click function
        self.cid = self.figure.canvas.mpl_connect('button_press_event', self.on_clicked) #mouse click event, calls on_clicked function 
        
        
    def draw(self): #drawing function which redraws entire figure
        
        #logging.info("plot (re)drawn")
        
        ylimo = self.axis.get_ylim()
        xlimo = self.axis.get_xlim()
        #colors the button
        if self.add == True: 
            self.b_add.color = '0.5'
           
        else:
            self.b_add.color = '0.95'
        
        
        
        
        
        self.axis.clear()
        
        
        
        #redraws data
        self.axis.plot(self.fit_obj.x, self.fit_obj.y, 'o') 
        self.axis.plot(self.fit_obj.means, self.fit_obj.amps, 'o')
        
        self.axis.set_ylim(ylimo)
        self.axis.set_xlim(xlimo)
        
        self.figure.show()
        
   
    
    def amp_slider_changed(self, value):
        
        if self.fit_obj.number_of_peaks > 0:
            self.fit_obj.amps[-1] = value
            self.draw()
    
    
    
    #addsa fit object with data to the plot
    def addfitobject(self, datax, datay):
        
        logging.info("fit object added")
        
        fit = fit_obj(datax, datay)
        self.fit_obj = fit    
        
        self.s_std = Slider(self.slider_std_ax, 'Std', 0, (max(datax)/5)/2.4, valinit = (max(datax)/5)/4.8, color='grey' )
        
        self.s_std.on_changed(self.slider_changed)
        self.std_val = (max(datax)/5)/4.8
        
        
    #toggles add, calls draw
    def add_point_clicked(self, value):
        
        logging.info("'add point' clicked")
        
        if self.add == False and self.fit_obj.number_of_peaks != 0:
                
                self.fit_obj.stds.append(self.std_val)
                logging.info("std added ({:.0f})".format(len(self.fit_obj.stds)))
                print(self.fit_obj.stds)
        self.add = not self.add
        
        self.draw()
        
        
    #changes the std value when changed
    def slider_changed(self, value):
        
        self.std_val = value
        
        import gauss
        self.draw()
        self.axis.plot(self.fit_obj.xline, gauss.gauss(self.fit_obj.xline, self.fit_obj.amps[-1], self.fit_obj.means[-1], self.std_val),  color='grey', linestyle=':')

        return
        
    #main on clicked function
    def on_clicked(self, value):
      
        x = self.figure.transFigure.inverted().transform((value.x,value.y))[0]
        y = self.figure.transFigure.inverted().transform((value.x,value.y))[1]
        
        
        
        #condition to add point
        if self.add == True and self.in_button(x, y) == False:
            
            logging.info("point added")
            
            self.add = False
            
            plt.sca(self.slider_amp_ax)
            plt.cla()
            self.s_amp = Slider(self.slider_amp_ax, 'Amp', value.ydata - (value.ydata/10), value.ydata + (value.ydata/10), valinit = value.ydata)
            
            self.s_amp.on_changed(self.amp_slider_changed)
            
            #add amplitude and mean
            self.fit_obj.means.append(value.xdata)
            self.fit_obj.amps.append(value.ydata)
            
            logging.info("mean added ({:.0f})".format(len(self.fit_obj.means)))
            logging.info("amp added ({:.0f})".format(len(self.fit_obj.amps)))
            
            #self.fit_obj.stds.append(0.2)
            self.s_std.color = 'red'
            self.fit_obj.number_of_peaks += 1
            
            
            #create amp slider
            
            
            self.draw()
            return
        
     
        
        
    #detects if the mouse is in a button 
    def in_button(self, x, y):
        
        bound_add = self.button_add_ax.get_position()
        return bound_add.contains(x, y)
        
    def applyfit(self, value):
        
        logging.info("\n")
        logging.info("=======apply fit pressed=======")
        
        self.draw()
        self.fit_obj.stds.append(self.std_val)
        logging.info("std added ({:.0f})".format(len(self.fit_obj.stds)))
        self.fit_obj.fit()
        self.plotfit()
        print(self.fit_obj.opt)

    def plotfit(self): #function to plot fit found for data
        import gauss
        
        self.draw()
        self.axis.plot(self.fit_obj.xline, gauss.gausscombined(self.fit_obj.xline, *self.fit_obj.opt), color='red') #plot with optimal parameters
        
        
        

class fit_obj:
    def __init__(self, datax, datay):
        self.number_of_peaks = 0
        self.means = []
        self.stds = []
        self.amps = []
        self.x = datax
        self.y = datay
        self.opt = None
        self.cov = None
        
        self.xline = np.linspace(min(self.x), max(self.x), 1000)
        
    def fit(self):
        
        logging.info("\n")
        logging.info("fit function of fit_obj called")
        
        
        
        #logging.info("gaussfit imported\n")
        logging.info("number of peaks: {:.0f}".format(self.number_of_peaks))
        logging.info("amps: {:.0f}".format(len(self.amps)))
        logging.info("means: {:.0f}".format(len(self.means)))
        logging.info("stds: {:.0f}".format(len(self.stds)))
        
        logging.info("calling gaussfit.fit: \n")
        opt, cov = gaussfit.fit(self.x, self.y, self.number_of_peaks, self.amps, self.means, self.stds)
        
        self.opt = opt
        self.cov = cov
        return opt, cov
        


my_plot = plot_image()
my_plot.addfitobject(x, y)
my_plot.draw()

logging.info("TeST")










