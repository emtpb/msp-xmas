import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.image as ppi
import matplotlib.cbook as ppc
import os


def equation_plot():
    """
    Plot the "christmas equation" and some christmas background.
    """

    def format_plot(sx, sy, st_x, st_y):
        # change plot style
        plt.xkcd()
        # switch off all labels
        plt.tick_params(
            axis='both',
            which='both',
            bottom='off',
            top='off',
            labelbottom='off',
            labelleft='off',
            left='off',
            right='off')
        # plot for orientation, "but don't display"
        plt.scatter(np.arange(10), np.arange(10), color='black')
        # stars
        plt.scatter(st_x, st_y, marker=(5, 1), color='gold', s=500)
        # background
        ax = plt.gca()
        ax.set_facecolor('black')
        # initial snow
        snow, = ax.plot(sx, sy, 'x', color='white')
        # branch
        branch = ppc.get_sample_data(os.path.dirname(os.path.abspath(__file__)) + '/branch.png', False)
        branch = ppi.imread(branch)
        plt.figimage(branch, 50, -75, zorder=1)
        return snow

    def update_snow(snow_iter, snow_y, interval):
        # end time of loop
        t_end = time.time() + interval
        while time.time() < t_end:
            # update stars
            snow_y = snow_y - np.random.rand(1)/10
            zero = snow_y < 0
            snow_y[zero] = 10 + snow_y[zero]
            snow_iter.set_ydata(snow_y)
            plt.pause(0.01)
        return snow_y

    # maximize figure
    mng = plt.get_current_fig_manager()
    try:
        if os.name == 'nt':
            mng.window.showMaximized()
        else:
            mng.resize(*mng.window.maxsize())
    except AttributeError:
        pass

    # initial snow
    snow_x = np.random.random_sample(200)*10
    snow_y = np.random.random_sample(200)*10

    # initial stars
    stars_x = np.array([1, 1.5, 3, 4, 5, 6, 7, 9, 8.5])
    stars_y = np.array([1, 8, 9, 3, 0, 6, 3, 8, 1])

    # basic font for equations
    font = {'family': 'sans',
            'weight': 'normal',
            'size': 55
            }

    # plot the equation parts, pause, reorder and repeat
    format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'red'
    plt.text(2, 7, r'The christmas', fontdict=font)
    plt.text(3, 4, r'equation', fontdict=font)
    font['size'] = 10
    font['color'] = 'darkgrey'
    plt.text(9, 0, r'Fabian Woitschek', fontdict=font)
    font['size'] = 55
    plt.pause(3)
    plt.clf()

    snow_iteration = format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'yellow'
    plt.text(0, 6, r'$y = \frac{\ln(\frac{x}{m} - sa)}{r^2}$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 3)
    plt.text(7, 6, r'$| \cdot r^2$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 1)
    plt.text(0, 3, r'$yr^2 = \ln(\frac{x}{m} - sa)$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 2)
    plt.text(7, 3, r'$| exp()$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 1)

    plt.clf()
    snow_iteration = format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'lime'
    plt.text(0, 6, r'$yr^2 = \ln(\frac{x}{m} - sa)$', fontdict=font)
    plt.text(7, 6, r'$| exp()$', fontdict=font)
    plt.text(0, 3, r'$e^{yr^2} = e^{\ln(\frac{x}{m} - sa)}$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 2)
    plt.text(7, 3, r'$| shorten$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 1)

    plt.clf()
    snow_iteration = format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'c'
    plt.text(0, 6, r'$e^{yr^2} = e^{\ln(\frac{x}{m} - sa)}$', fontdict=font)
    plt.text(7, 6, r'$| shorten$', fontdict=font)
    plt.text(0, 3, r'$e^{yr^2} = \frac{x}{m} - sa$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 2)
    plt.text(7, 3, r'$| \cdot m$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 1)

    plt.clf()
    snow_iteration = format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'm'
    plt.text(0, 6, r'$e^{yr^2} = \frac{x}{m} - sa$', fontdict=font)
    plt.text(7, 6, r'$| \cdot m$', fontdict=font)
    plt.text(0, 3, r'$me^{yr^2} = x - sam$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 2)
    plt.text(7, 3, r'$| reorder$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 1)

    plt.clf()
    snow_iteration = format_plot(snow_x, snow_y, stars_x, stars_y)
    font['color'] = 'red'
    plt.text(0, 6, r'$me^{yr^2} = x - sam$', fontdict=font)
    plt.text(7, 6, r'$| reorder$', fontdict=font)
    plt.text(0, 3, r'$me^{rry} = x - mas$', fontdict=font)
    snow_y = update_snow(snow_iteration, snow_y, 2)

    plt.clf()
    format_plot(snow_x, snow_y, stars_x, stars_y)
    font['size'] = 80
    plt.text(0, 4, r'$me^{rry} = x - mas$', fontdict=font)
    # fireworks
    fire = ppc.get_sample_data(os.path.dirname(os.path.abspath(__file__)) + '/firework.png', False)
    fire = ppi.imread(fire)
    plt.figimage(fire, 775, 325, zorder=10)
    plt.pause(2)


if __name__ == '__main__':
    equation_plot()
    plt.show()
