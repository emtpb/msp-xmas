#MSMP Christmas Challenge, entry by Johannes Menzel

import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.animation as animation

Box = [0.0, 0.0 + 3.5j, 11.0 + 3.5j, 11.0, 0.0]
X=[0.0, -1.0 + -1.0j, 1.0 + 1.0j, 0.0, -1.0 + 1.0j, 1.0 + -1.0j]
M=[-1.0 + -1.0j, -1.0 + 1.0j, 0.0, 1.0 + 1.0j, 1.0 + -1.0j]
A=[-0.6 + -1.0j, 1.0j,0.6 + -1.0j,-0.8 + -0.1j, 0.8 + -0.1j]
S=[0.0 + 1.0j,0.5 + 0.7j, 0.0 + 1.0j, -0.5 + 0.7j, 0.5 + -0.7j, 0.0 - 1.0j, -0.5 + -0.7j]
print(A)
X_offset=1.75 + 1.75j
M_offset=X_offset + 2.5
A_offset=M_offset + 2.5
S_offset=A_offset + 2.5
print(len(A))
for i in range(len(X)):
    X[i] += X_offset
for i in range(len(M)):
    M[i] += M_offset
for i in range(len(A)):
    A[i] += A_offset
for i in range(len(S)):
    S[i] += S_offset

underline=[1.0 +- 0.2j, -9.0 + -0.2j, 2.0 + -0.4j]
for i in range(len(underline)):
    underline[i] += S[-2]
endpoints = [11.0 + 0.4j, 11.0, 0.0]
func_points = Box + X + M + A + S + underline + endpoints

intervals=[50,100,50,100,20,50,100,50,50,100,20,70,50,50,70,20,90,90,50,40,30,20,20,20,40,20,20,20,100,90,20,20,50]
print(func_points)
T=sum(intervals)
print(len(func_points), len(intervals))
x = np.linspace(func_points[0],func_points[1],intervals[0])
for i in range(1,len(func_points)-1):
    tmp = np.linspace(func_points[i],func_points[i+1],intervals[i])
    x = np.concatenate((x,tmp))

t = np.arange(0,T)
w0 = 2 * np.pi / T
coeff = []
e_func = []
for i in range(-60,60):
    x_i = 1/T * np.trapz(x*(np.e ** (-1j * w0 * i * t)))
    e_i = np.e ** (1j * w0 * i * t)
    print(x_i)
    coeff.append(x_i)
    e_func.append(e_i)

coeff = np.array(coeff)
x_hat = coeff[0] * e_func[0]
for i in range(1,len(coeff)):
    x_hat += coeff[i] * e_func[i]

coeff_anim = []
for j in range(T):
    points = [0]
    for i in range(len(coeff)):
        new_point = points[-1] + coeff[i] * e_func[i][j]
        points.append(new_point)
    points = np.array(points)
    coeff_anim.append(points)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


def animate(i):
    if(i < T):
        x_1 = np.real(x_hat[:i])
        y_1 = np.imag(x_hat[:i])

        x_2 = np.real(coeff_anim[i])
        y_2 = np.imag(coeff_anim[i])

        ax.clear()
        #ax.set_xlim([-1.5,7.5])
        #ax.set_ylim([-2.2,1.5])
        ax.plot(x_1,y_1)
        ax.plot(x_2,y_2)
    else:
        ax.clear()
        #ax.set_xlim([-1.5,7.5])
        #ax.set_ylim([-2.2,1.5])
        ax.plot(np.real(x_hat),np.imag(x_hat))

anim = animation.FuncAnimation(fig,animate,interval=20)
plt.show()
