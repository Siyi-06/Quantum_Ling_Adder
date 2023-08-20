'''Draw QC Diagram in the paper'''

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
#print(w(x))
y1= 4 * x -np.floor(np.log2(x)) -w(x)
y2 = 2*x+np.floor(3*x/(np.log2(x)))
y3 = 2*x+np.floor(3*x/(np.log2(x)))
# The QC cost function of Quantum Ling Adder
y4=12*x-6*np.floor(np.log2(x/2))-10 -6*w(x/2)
plt.semilogy(x,y1,label="Draper In-place CLA", linewidth=2, color='forestgreen',linestyle = "dotted")
plt.semilogy(x,y2,label="Takahashi CLA", linewidth=2, color='tab:cyan',linestyle = "--")
plt.semilogy(x,y3,label="Takahashi Combination", linewidth=2, color='tab:blue',linestyle = "-.")
plt.semilogy(x,y4,label="Our Adder", linewidth=2,color='red')

for a, b in zip([x[0]],[y1[0]]):
	plt.text(a, b*0.99, '%.0f'%b, ha='center', va='top',color='forestgreen', fontsize=10.5)
for a, b in zip(x[1:3],y1[1:3]):
	plt.text(a, b*0.93, '%.0f'%b, ha='center', va='top',color='forestgreen', fontsize=10.5)
for a, b in zip([x[0],x[2]],[y3[0],y3[2]]):
	plt.text(a, b*1.06, '%.0f'%b, ha='center', va='bottom', color='tab:blue',fontsize=10.5)
for a, b in zip([x[1]],[y3[1]]):
	plt.text(a, b*0.98, '%.0f'%b, ha='center', va='top',color='tab:blue', fontsize=10.5)

for a, b in zip(x[3:],y1[3:]):
	plt.text(a, b*1.06, '%.0f'%b, ha='center', va='bottom',color='forestgreen', fontsize=10.5)
for a, b in zip(x[3:],y3[3:]):
	plt.text(a, b*0.93, '%.0f'%b, ha='center', va='top', color='tab:blue',fontsize=10.5)
for a, b in zip(x,y4):
	plt.text(a, b*1.3, '%.0f'%b, ha='center', va='top',color='red', fontsize=10.5)

ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xlabel("n")
plt.ylabel("QC")

plt.show()