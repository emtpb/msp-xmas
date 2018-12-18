"Von Lennart Knaup"

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as sio
import scipy.signal as sig


plt.close('all')
    

# Create sound signal
sampl_freq = 44100
time = 5 #s
half_time = time/2
n = sampl_freq*half_time
t = np.linspace(0,half_time,n)

"First half of signal"
y1s = sig.chirp(t,1000,time/2,2000,method = 'quadratic') + 1.5*np.sin(2*np.pi*1200*t)
y2s = sig.chirp(t,1200,time/2,2500,method = 'quadratic') + np.sin(2*np.pi*1700*t)
y3s = sig.chirp(t,1400,time/2,3000,method = 'quadratic') + np.sin(2*np.pi*2300*t)

"Delete the unnecessary part"
y1s[t<1.25] = 0
y2s[t<1.5] = 0
y3s[t<1.9] = 0
y2s[y2s >23]

"reversed second half"
y1r = y1s[::-1]
y2r = y2s[::-1]
y3r = y3s[::-1]



"Combine  the parts"
y1 = np.append(y1s,y1r)
y2 = np.append(y2s,y2r) 
y3 = np.append(y3s,y3r) 

y = y1 +y2 +y3

"Stamm"
stamm = np.zeros((690,182))
begin = int(182/2-10)
end = int(182/2+10)
stamm[0:38,begin:end] = -1

"calculate spectrogram"
f, t, spec = sig.spectrogram(y,sampl_freq,nperseg = int(sampl_freq/32))
limit = 0.02
spec[spec>limit] = spec[spec>limit]/10
spec = spec*100
spec = spec + stamm


"plot spectrogram"
plt.figure()
plt.pcolormesh(t, f, spec,cmap = 'BrBG')

plt.ylim((800,3500))
plt.axis('Off')

"export signal to .wav"
sio.write('wundervoller_Weihnachtsklang.wav', int(sampl_freq), y)
plt.show()