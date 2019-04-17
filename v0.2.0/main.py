import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, TextBox
import singlegaussian
import fit_class

data = np.loadtxt("GaussTestData.txt", skiprows=1, unpack = False) #imports x and y data
#data[:,1] += 600

class Window: #plot object
    def __init__(self):
        self.data = None
        self.xspace = None
        self.fit = None
        self.peak = {}
        self.bounds = {
                       'Background' : [-np.inf, np.inf],
                      }
        self.current_peak = None
        self.background = 0
        
        self.fig = plt.figure("Curvefit", figsize=(8, 8))
        self.mainAx = self.fig.add_axes([0.1, 0.3, 0.7, 0.6])
        #self.mainAx.plot(data[0], data[1], ".")

        ##button axes#####
        self.buttonAx = {}
        self.button = {}
        self.buttonState = {
                            'Add' : False,
                            'Gauss' : False,
                            'Lorentz' : False,
                            }
        
        self.buttonAx['Add'] = plt.axes([0.83, 0.82, 0.1, 0.075])
        self.button['Add'] = Button(self.buttonAx['Add'] ,'Add', color='grey')
        self.button['Add'].on_clicked(self.add_clicked)
        
        self.buttonAx['Gauss'] = plt.axes([0.83, 0.72, 0.1, 0.075])
        self.button['Gauss'] = Button(self.buttonAx['Gauss'] ,'Gauss', color='grey')
        self.button['Gauss'].on_clicked(self.gauss_clicked)
        
        self.buttonAx['Lorentz'] = plt.axes([0.83, 0.62, 0.1, 0.075])
        self.button['Lorentz'] = Button(self.buttonAx['Lorentz'] ,'Lorentz', color='grey')
        self.button['Lorentz'].on_clicked(self.lorentz_clicked)
        
        ###
        
#        self.buttonAx['AmpBound'] = plt.axes([0.65, 0.2, 0.065, 0.03])
#        self.button['AmpBound'] = Button(self.buttonAx['AmpBound'] ,'Bound', color='grey')
#        
#        self.buttonAx['MeanBound'] = plt.axes([0.65, 0.15, 0.065, 0.03])
#        self.button['MeanBound'] = Button(self.buttonAx['MeanBound'] ,'Bound', color='grey')
        
#        self.buttonAx['StdBound+'] = plt.axes([0.65, 0.10, 0.04, 0.03])
#        self.button['StdBound+'] = Button(self.buttonAx['StdBound+'] ,'+', color='grey')
#        self.button['StdBound+'].on_clicked(self.std_up_bound_clicked)
#        self.buttonAx['StdBound-'] = plt.axes([0.60, 0.10, 0.04, 0.03])
#        self.button['StdBound-'] = Button(self.buttonAx['StdBound-'] ,'-', color='grey')
#        self.button['StdBound-'].on_clicked(self.std_low_bound_clicked) 
        
#        self.buttonAx['BgBound+'] = plt.axes([0.65, 0.05, 0.04, 0.03])
#        self.button['BgBound+'] = Button(self.buttonAx['BgBound+'], '+', color ='grey')
#        self.button['BgBound+'].on_clicked(self.bg_up_bound_clicked)
#        self.buttonAx['BgBound-'] = plt.axes([0.60, 0.05, 0.04, 0.03])
#        self.button['BgBound-'] = Button(self.buttonAx['BgBound-'], '-', color ='grey')
#        self.button['BgBound-'].on_clicked(self.bg_low_bound_clicked)
#        ###
#        
        self.buttonAx['Peak-'] = plt.axes([0.83, 0.5, 0.035, 0.03])
        self.button['Peak-'] = Button(self.buttonAx['Peak-'], '<', color = 'grey')
        self.button['Peak-'].on_clicked(self.toggle_peaks_left) 
        
        self.peak_number_ax = plt.axes([0.85, 0.54, 0.06, 0.03])
        self.peak_number_ax.set_axis_off()
        self.buttonAx['Peak+'] = plt.axes([0.895, 0.5, 0.035, 0.03])
        self.button['Peak+'] = Button(self.buttonAx['Peak+'], '>', color = 'grey')
        self.button['Peak+'].on_clicked(self.toggle_peaks_right)

        ##sliders#####
        self.sliderAx = {}
        self.slider = {}
        self.sliderVals = {
                          'Amp' : 0.5,
                          'Mean' : 0.5,
                          'Std' : 0.5
                          }
        
        self.sliderAx['Amp'] = plt.axes([0.15, 0.2, 0.25, 0.03])
        self.slider['Amp'] = Slider(self.sliderAx['Amp'], "Amp", 0, 1, valinit = 0.5, color='grey')
        self.slider['Amp'].on_changed(self.amp_slider_changed)
        
        self.sliderAx['Mean'] = plt.axes([0.15, 0.15, 0.25, 0.03])     
        self.slider['Mean'] = Slider(self.sliderAx['Mean'], "Mean", 0, 1, valinit = 0.5, color='grey')
        
        self.sliderAx['Std'] = plt.axes([0.15, 0.10, 0.25, 0.03])     
        self.slider['Std'] = Slider(self.sliderAx['Std'], "Std", 0, 4, valinit = 2, color='grey')
        self.slider['Std'].on_changed(self.std_slider_changed)
        
        self.sliderAx['Bg'] = plt.axes([0.15, 0.05, 0.25, 0.03])     
        self.slider['Bg'] = Slider(self.sliderAx['Bg'], "Bg", 0, 1, valinit = 0.5, color='grey')
        self.slider['Bg'].on_changed(self.bg_slider_changed)
        
        #TEXT BOX
        
        self.textboxAx = {}
        self.textbox = {}
        
        self.textboxAx['Bg'] = plt.axes([0.5, 0.05, 0.06, 0.03])
        self.textbox['Bg'] = TextBox(self.textboxAx['Bg'], "", "0")
        self.textbox['Bg'].on_submit(self.bg_submit)
        
        self.textboxAx['Std'] = plt.axes([0.5, 0.10, 0.06, 0.03])
        self.textbox['Std'] = TextBox(self.textboxAx['Std'], "", "0")
        self.textbox['Std'].on_submit(self.std_submit)
        
        self.textboxAx['Mean'] = plt.axes([0.5, 0.15, 0.06, 0.03])
        self.textbox['Mean'] = TextBox(self.textboxAx['Mean'], "", "0")
        self.textbox['Mean'].on_submit(self.mean_submit)
        
        self.textboxAx['Amp'] = plt.axes([0.5, 0.2, 0.06, 0.03])
        self.textbox['Amp'] = TextBox(self.textboxAx['Amp'], "", "0")
        self.textbox['Amp'].on_submit(self.amp_submit)
        
        self.clickid = self.fig.canvas.mpl_connect('button_press_event', self.mainAx_click)
        
        ####
        self.datapoints = None

    def add_data(self, data):
        self.data = data
        xlim = ( min(data[:,0]) , max(data[:,0]) )
        ylim = ( min(data[:,1]) , max(data[:,1]) )
        
        

        self.mainAx.set_xlim(xlim)
        self.mainAx.set_ylim(ylim)
        
        self.datapoints, = self.mainAx.plot(data[:,0], data[:,1], '.')
        
        self.xspace = np.linspace(min(data[:,0]) , max(data[:,0]), 1000)
        return
    
    def add_peak(self, x, y):
        peakname = str(len(self.peak))
        self.peak[peakname] = [x, y, 0]
        self.current_peak = peakname
        self.draw()
    
    def add_fit(self, lorentzian = False):
        
        if len(self.peak) == 0:
            print("No peaks chosen!")
            return
        
        if lorentzian == True:
            estimates = []
            for peak in self.peak.values():
                estimates += [peak[1], peak[0], peak[2]*2.4]
            estimates += [self.background]
                
            self.fit = fit_class.Fit(data, estimates)
        
        
        estimates = []
        for peak in self.peak.values():
            estimates += [peak[1], peak[0], peak[2]]
        estimates += [self.background]
            
        self.fit = fit_class.Fit(data, estimates)
        
        return

    def mainAx_click(self, event):
        
        if event.inaxes == self.mainAx:
            
            if self.buttonState['Add'] == True:
                self.add_peak(event.xdata, event.ydata)
                self.buttonState['Add'] = False
                self.update()
            
    
    def add_clicked(self, event):
        
        self.buttonState['Add'] = not self.buttonState['Add']
        self.update()
        
    def gauss_clicked(self, event):
        if self.peak:
            self.add_fit()
            
            self.buttonState['Gauss'] = not self.buttonState['Gauss']
            if self.buttonState['Gauss'] == True:
                self.buttonState['Lorentz'] = False
            self.fit.fitgaussian()
            self.update()
        
    def lorentz_clicked(self, event):
        if self.peak:
            self.add_fit()
            
            self.fit.fitlorentzian()
            self.update()
            self.buttonState['Lorentz'] = not self.buttonState['Lorentz']
            if self.buttonState['Lorentz'] == True:
                self.buttonState['Gauss'] = False
        
            self.update()
        
    def bg_up_bound_clicked(self, event):
        self.bounds['Background'][1] = self.background
        return
    
    def bg_low_bound_clicked(self, event):
        self.bounds['Background'][0] = self.background
        return
    
    def std_low_bound_clicked(self, event):
        return
    
    def std_up_bound_clicked(self, event):
        return
    
    def amp_slider_changed(self, event):
        return
    
    def mean_slider_changed(self, event):
        return
    
    def std_slider_changed(self, event):
        self.textboxAx['Std'].clear()
        self.textbox['Std'] = TextBox(self.textboxAx['Std'], "", "{:.2f}".format(event))
        self.textbox['Std'].on_submit(self.std_submit)
        
        if self.current_peak:
            self.peak[self.current_peak][2] = event
        self.update()
        
        return
    
    def bg_slider_changed(self, event):
        self.background = event
        
        #self.textbox['Bg'].set_val("{:.2f}".format(event))
        
        self.textboxAx['Bg'].clear()
        self.textbox['Bg'] = TextBox(self.textboxAx['Bg'], "", "{:.2f}".format(event))
        self.textbox['Bg'].on_submit(self.bg_submit)
        
        self.update()
        return
    
    def bg_submit(self, event):
        val = float(event)
        maxval = val + self.mainAx.get_ylim()[1]/10
        minval = val - self.mainAx.get_ylim()[1]/10
        
        self.sliderAx['Bg'].clear()
        self.slider['Bg'] = Slider(self.sliderAx['Bg'], "Bg", minval, maxval, valinit = val, color='grey')
        self.slider['Bg'].on_changed(self.bg_slider_changed)
        self.background = val
        self.update()
    
    def std_submit(self, event):
        val = float(event)
        maxval = val + val*2
        minval = val - val*2
        
       
        
        self.sliderAx['Std'].clear()
        self.slider['Std'] = Slider(self.sliderAx['Std'], "Std", minval, maxval, valinit = val, color='grey')
        self.slider['Std'].on_changed(self.std_slider_changed)
        self.peak[self.current_peak][2] = val
        self.update()
        
        return
    
    def mean_submit(self, event):
        return
    
    def amp_submit(self, event):
        return
        
    def draw(self):

        ylimi = self.mainAx.get_ylim()
        xlimi = self.mainAx.get_xlim()        
        
        self.mainAx.clear()
        self.mainAx.axhline(y = 0)
        
        #redraws data
        if type(self.data) != None:
            
            self.mainAx.plot(data[:,0], data[:,1], ".")
        
        #redraws peak
        if self.peak and self.fit == None:
            for peak in self.peak.values():
                self.mainAx.plot(peak[0], peak[1], 'x', color = 'red')
                if peak[2]:
                    self.mainAx.plot(self.xspace, singlegaussian.gauss(self.xspace, peak[1] - self.background, peak[0], peak[2], self.background))
               
        #shows current peak
        if self.current_peak and self.fit == None:
            self.peak_number_ax.clear()
            peaknum = str(int(self.current_peak) + 1)
            self.peak_number_ax.text(0.05, 0.5, "peak: " + peaknum, transform = self.peak_number_ax.transAxes)
            self.peak_number_ax.set_axis_off()

        #shows background line
        if self.background:
            self.mainAx.axhline(y = self.background, linestyle = ':', color = 'red')
            
        #plot fit
        if self.fit:
            self.mainAx.plot(self.fit.xspace, self.fit.yspace)
        
        #resets limits
        self.mainAx.set_ylim(ylimi)
        self.mainAx.set_xlim(xlimi)
        
        self.fig.canvas.draw()
    

        
    def toggle_button_color(self, button):
        onCol = 'red'
        offCol = 'grey'
                
        if self.buttonState[button] == True:
            
            self.button[button].color = onCol
        elif self.buttonState[button] == False:
            self.button[button].color = offCol
            
    def toggle_peaks_left(self, event):
        if self.current_peak == None:
            return
        number = int(self.current_peak)
        if str(number - 1) in self.peak.keys():
            self.current_peak = str(number - 1)
            self.draw()
        return
    def toggle_peaks_right(self, event):
        if self.current_peak == None:
            return
        number = int(self.current_peak)
        if str(number + 1) in self.peak.keys():
            self.current_peak = str(number + 1)
            self.draw()
        return
        
    def update(self):

        self.draw()
        
        for button in self.buttonState.keys():
            self.toggle_button_color(button)
            


window = Window()
window.add_data(data)
window.draw()
window.update()





#np.savetxt("GaussTestData.txt", np.c_[data[:,0], data[:,1]])







