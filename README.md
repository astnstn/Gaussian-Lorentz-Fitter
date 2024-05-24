# Gaussian and Lorentzian (Cauchy) distrubution curve fitting

Program uses graphical input with some matplotlib widgets to quickly estimate parameters which are then passed to the scipy optimize curve_fit function.

**WARNING:** This is a very old noob project and the code isn't very pretty. I still like the idea though so I intend to rewrite somewhen. 

The relevant files are in the 'Newest prototype' folder. This uses only Gaussian curves with a small linear offset (y=0) added. The older versions use button and slider widgets which are self-explanatory. 

### Usage

See `example.py` for how to create an interactive fitter window.

- Add a Gaussian curve with middle mouse click
- Drag resulting node by holding left mouse button
- Change the standard deviation of the curve with the scroll-wheel
- Press space to switch between viewing the individual functions and the composite curve
- Press A to perform a curve fit with the current estimated parameters

https://github.com/astnstn/Gaussian-Lorentz-Fitter/assets/46248022/73015daa-6efa-4992-9878-68f2449c1c22

