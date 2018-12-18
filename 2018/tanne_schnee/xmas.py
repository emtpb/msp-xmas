import numpy as np
import matplotlib.pyplot as plt


log = np.append(np.full((45), np.nan),np.full((10),0))
green1 = np.append(np.full((20), np.nan),np.full((60),0.1))
green2 =np.append(np.full((24), np.nan),np.full((52),0.12))

bg_color = '0.5'

fig = plt.figure(facecolor=bg_color)
axes = fig.add_subplot(111)
axes.patch.set_facecolor(bg_color)
plt.axis('off')
plt.ion()
plt.show()


while True:
    for i in np.linspace(0,0.1,10):
        plt.plot(log+i,'s', c='#614126')
    
    for i in np.linspace(0,0.7,100):
        green=np.append(np.full((30+int(i*10*2.8)), np.nan),np.full((40-int(20*i*2.8)),0.1))
        plt.plot(green+i,'gs')
    del green

    plt.plot(np.append(np.full(49,np.nan),[0.81]),'r*', markersize=20)
    snowarray =np.random.rand(100,10)
    plt.plot(snowarray**2,'w.')
    
    plt.draw()
    plt.pause(0.0000000001)
    plt.plot(snowarray**2,'.',c='0.5', markersize=10)
    del snowarray
