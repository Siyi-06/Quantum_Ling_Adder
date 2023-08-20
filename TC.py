'''Draw TC Diagram in the paper'''

import numpy as np
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')
def w(x: np.array):
    y = np.zeros_like(x)
    for i, xi in enumerate(x):
        cnt = 0
        while xi > 0:
            cnt += xi % 2
            xi = int(xi / 2)
        y[i] = cnt
    return y

x = np.arange(2, 11, 1)
y1=70*x-21*np.floor(np.log2(x))-21*np.floor(np.log2(x-1))-49-21*w(x)-21*w(x-1)
y2 = 196*x
y3 = 49*x
# The TC cost function of Quantum Ling Adder
y4=91*x-42*np.floor(np.log2(x/2))-84-42*w(x/2)-14
plt.semilogy(x,y1,label="Draper In-place CLA", linewidth=2, color='forestgreen',linestyle = "dotted")
plt.semilogy(x,y2,label="Takahashi CLA", linewidth=2, color='tab:cyan',linestyle = "--")
plt.semilogy(x,y3,label="Takahashi Combination", linewidth=2, color='tab:blue',linestyle = "-.")
plt.semilogy(x,y4,label="Our Adder", linewidth=2,color='red')
for a, b in zip([x[0]],[y1[0]]):
	plt.text(a, b*0.8, '%.0f'%b, ha='center', va='bottom',color='forestgreen', fontsize=10.5)
for a, b in zip(x[1:],y1[1:]):
	plt.text(a, b*0.69, '%.0f'%b, ha='center', va='bottom',color='forestgreen', fontsize=10.5)
for a, b in zip(x,y2):
	plt.text(a, b*1.16, '%.0f'%b, ha='center', va='bottom',color='tab:cyan', fontsize=10.5)
#####################
for a, b in zip(x[:2],y3[:2]):
	plt.text(a, b*1.1, '%.0f'%b, ha='center', va='bottom', color='tab:blue',fontsize=10.5)
for a, b in zip([x[2]],[y3[2]]):
	plt.text(a, b*0.9, '%.0f'%b, ha='center', va='top', color='tab:blue',fontsize=10.5)
for a, b in zip(x[3:6],y3[3:6]):
	plt.text(a, b*0.93, '%.0f'%b, ha='center', va='top', color='tab:blue',fontsize=10.5)
for a, b in zip(x[6:],y3[6:]):
	plt.text(a, b*1.23, '%.0f'%b, ha='center', va='top', color='tab:blue',fontsize=10.5)


#####################
for a, b in zip([x[0]],[y4[0]]):
	plt.text(a, b*0.96, '%.0f'%b, ha='center', va='top',color='red', fontsize=10.5)
for a, b in zip([x[1]],[y4[1]]):
	plt.text(a, b*0.8, '%.0f'%b, ha='center', va='top',color='red', fontsize=10.5)
for a, b in zip([x[2]],[y4[2]]):
	plt.text(a, b*1.1, '%.0f'%b, ha='center', va='bottom',color='red', fontsize=10.5)
for a, b in zip(x[3:],y4[3:]):
	plt.text(a, b*1.06, '%.0f'%b, ha='center', va='bottom',color='red', fontsize=10.5)

ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel("n")
plt.ylabel("TC")
plt.show()