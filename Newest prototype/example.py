from interactive_fitter import Window
import numpy as np

x, y = np.loadtxt("1996quarter.txt", skiprows=1, unpack=True)
window = Window(x, y)
