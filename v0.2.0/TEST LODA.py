import matplotlib.pyplot as plt
import pickle

file = open("SAVED.txt", 'rb')

fit = pickle.load(file)

file.close()

plt.figure(2)
plt.plot(fit.xspace, fit.yspace)