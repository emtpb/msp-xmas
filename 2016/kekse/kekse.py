import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Slider

x = np.arange(-100, 100, 1)
y = np.arange(-100, 100, 1)

[X, Y] = np.meshgrid(x,y)

Z = np.sqrt(X**2+Y**2) < 70


f = 0.7
mappe = np.array([[1, 1, 1], [0.8*f, 0.5*f, 0]])
cm = mpl.colors.ListedColormap(mappe)

fig, ax = plt.subplots()
plt.pcolormesh(Z, cmap=cm)
plt.title('Weihnachtsplaetzchen im Backofen')
plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labelleft='off',
    left='off',
    right='off')    # labels along the bottom edge are off

axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])

slider_f = Slider(axfreq, 'Temp / $^\circ$C', 20, 300, valinit=20)


def update(val):
    f = 1 - slider_f.val/300
    mappe = np.array([[1, 1, 1], [0.8 * f, 0.5 * f, 0]])
    cm = mpl.colors.ListedColormap(mappe)
    plt.set_cmap(cm)
    fig.canvas.draw_idle()

slider_f.on_changed(update)

plt.show()
