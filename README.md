# Gaussian and Lorentzian (Cauchy) distrubution curve fitting

Program uses graphical input with some matplotlib widgets to quickly estimate parameters which are then passed to the scipy optimize curve_fit function.

**DISCLAIMER:** This is a very old project I create when I was still learning Python and Git in undergrad. I didn't really anticipate any interest. A rewrite is probably needed but for now I'm updating the readme to give better instructions on how to use the program.

The relevant files are in the 'Newest prototype' folder. This uses only Gaussian curves with a small linear offset (y=0) added. The older versions use button and slider widgets which are self-explanatory. 

### Usage

- Add a Gaussian curve with middle mouse click
- Drag resulting node by holding left mouse button
- Change the standard deviation of the curve with the scroll-wheel
- Press space to switch between viewing the individual functions and the composite curve
- Press A to perform a curve fit with the current estimated parameters

https://github.com/astnstn/Gaussian-Lorentz-Fitter/assets/46248022/73015daa-6efa-4992-9878-68f2449c1c22

