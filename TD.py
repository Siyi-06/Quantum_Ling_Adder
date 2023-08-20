'''Draw TD Diagram in the paper'''

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(2, 11, 1)
y1=24+3*np.floor(np.log2(x))+3*np.floor(np.log2(x-1))+3 * np.floor(np.log2(x/3)) + 3 * np.floor(np.log2((x - 1)/3))
y2 = 90*np.log2(x)
y3 = 54*np.log2(x)
# The TD cost function of Quantum Ling Adder
y4=27+6*np.log2(x/2)+6*np.log2(x/6)
plt.semilogy(x,y1,label="Draper In-place CLA", linewidth=2, color='forestgreen',linestyle = "dotted")
plt.semilogy(x,y2,label="Takahashi CLA", linewidth=2, color='tab:cyan',linestyle = "--")
plt.semilogy(x,y3,label="Takahashi Combination", linewidth=2, color='tab:blue',linestyle = "-.")
plt.semilogy(x,y4,label="Our Adder", linewidth=2,color='red')
ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for a, b in zip(x,y1):
	plt.text(a, b+0.3, '%.0f'%b, ha='center', va='bottom',color='forestgreen', fontsize=10.5)
for a, b in zip(x,y2):
	plt.text(a, b*1.06, '%.0f'%b, ha='center', va='bottom',color='tab:cyan', fontsize=10.5)
for a, b in zip(x,y3):
	plt.text(a, b*1.06, '%.0f'%b, ha='center', va='bottom', color='tab:blue',fontsize=10.5)
for a, b in zip(x,y4):
	plt.text(a, b*0.95, '%.0f'%b, ha='center', va='top',color='red', fontsize=10.5)

plt.xlabel("n")
plt.ylabel("TD")

plt.legend(bbox_to_anchor=(0,1.02,1,0.2),frameon=False, loc="lower right",mode="expand", borderaxespad=0, ncol=2)
plt.show()