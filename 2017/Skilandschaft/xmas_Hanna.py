# MSMP christmas challenge
# Hanna Schmiegel, 20.12.2017

import numpy as np
import matplotlib.pyplot as plt
import pylab

# load Data
da = np.load('Daten.npz')
temps = np.array([5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85])

# plot
fig1, ax = plt.subplots()
fig1.subplots_adjust(left=0, right=1, top=1, bottom=0)

# stars
x = da['freq_all'].item()[5][2100:5500]
y_star = da['imp_all'].item()[5][2100:5500]+2000*abs(np.sin(0.05*x)+np.sin(0.05*2*x+2.5)+np.sin(0.05*2*x+5.8634))
ax.plot(x[::40], y_star[::40], linestyle='none', marker=(5, 1, 90), color=(1, 1, 0),  markersize=15)
ax.plot(x[20::40], y_star[20::40], linestyle='none', marker='*', color=(0.95, 0.88, 0),  markersize=15)
# snow
y_snow = da['imp_all'].item()[5][2100:5500]+2000*abs(np.sin(0.05*x)+np.sin(0.1*2*x+2.5)+np.sin(0.2*2*x+5.8634))
ax.plot(x[::2], y_snow[::2], linestyle='none', marker='.', color=(0.75, 1, 1))
ax.plot(x[1::2], y_snow[1::2], linestyle='none', marker='.', color=(1, 1, 1))

# mountain
for ind, t in enumerate(temps):
    if ind == 0:
        ax.semilogy(da['freq_all'].item()[t][2100:5500], da['imp_all'].item()[t][2100:5500], linewidth=5, color=(1, 1, 1))
    elif ind < 8:
        ax.semilogy(da['freq_all'].item()[t][2100:5500], da['imp_all'].item()[t][2100:5500], linewidth=1.5, color=(0.1, 1, 1))
    elif ind < 16:
        ax.semilogy(da['freq_all'].item()[t][2100:5500], da['imp_all'].item()[t][2100:5500], linewidth=1.5, color=(0.3, 1, 1))
    elif ind < 24:
        ax.semilogy(da['freq_all'].item()[t][2100:5500], da['imp_all'].item()[t][2100:5500], linewidth=1.5, color=(0.5, 1, 1))
    else:
        ax.semilogy(da['freq_all'].item()[t][2100:5500], da['imp_all'].item()[t][2100:5500], linewidth=1.5, color=(0.7, 1, 1))
    ax.axis([da['freq_all'].item()[t][2100], da['freq_all'].item()[t][5500], 4, 2000])
    ax.axis('off')

    ax.semilogy(da['freq_all'].item()[t][2670:5500]-(da['freq_all'].item()[t][2600]-da['freq_all'].item()[t][2100]), da['imp_all'].item()[t][2670:5500]-15, linewidth=1.5, color=(0.9, 1, 1))

fig1.set_facecolor((0, 0, 0.1))
pylab.fill_between(da['freq_all'].item()[5][2100:5500], 4, da['imp_all'].item()[5][2100:5500], color=(0.8, 1, 1))

# text
plt.xkcd()
ax.text(2.2e6, 5, 'Frohe\nWeihnachten!', fontsize=80, color='w')

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()
