# Gaussian-Fitter
Matplotlib and scipy to fit Gaussian/lorentzian curves to raw data.
Works 90% of the time.
Does not currently allow for adding background offset.

Use: 

- change the x-y data at the top of "main". It uses np.loadtxt.
- Run "main"
- click "add" and then click on a point
- adjust the std slider to set standard deviation
- click fit or fit_l for gaussian/lorentzian fit

![alt text](https://i.imgur.com/hbLN29z.png)