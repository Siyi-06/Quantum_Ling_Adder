from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.extensions.quantum_initializer.initializer import Initialize
import matplotlib.pyplot as plt
import random
import math

'''Calculate QC'''
def w(x):
    count=0
    while x:
        count+=1
        x&=(x-1)
    return count
def QC(x):
    QC=12*x-6*w(int(x/2))-6*math.floor(math.log2(x/2))-8-2
    print("QC=", QC)
    return QC

'''Important settings'''
add_bit=3   # Users can customize add_bit.
s_number=add_bit+1
total_qubit_number=QC(add_bit)

'''random addition'''
rand_int_a = random.randint(0, 2**add_bit-1)
rand_addend_a = bin(rand_int_a)[2:].zfill(add_bit)
rand_int_b = random.randint(0, 2**add_bit-1)
rand_addend_b = bin(rand_int_b)[2:].zfill(add_bit)
print("a =",rand_addend_a ,"b =",rand_addend_b)
rand_int_sum=rand_int_a+rand_int_b
rand_sum = bin(rand_int_sum)[2:].zfill(add_bit+1)
print("real sum =",rand_sum )
circuit = QuantumCircuit(total_qubit_number,s_number)
print(add_bit, "bits quantum Ling adder")

'''initialize'''

strr=''
for i in range(add_bit):
    strr=strr+'00'+rand_addend_b[i]+rand_addend_a[i]
print(strr)
Initial_state='0'*(total_qubit_number-4*add_bit)+strr
print("Initial_state",Initial_state)
circuit.append(Initialize(Initial_state), range(total_qubit_number))

'''customize OR gate'''
qc = QuantumCircuit(3, name='OR')
qc.x(0)
qc.x(1)
qc.ccx(0,1,2)
qc.x(0)
qc.x(1)
qc.x(2)
OR_gate = qc.to_instruction()
'''Different Steps'''
def step1(circuit,a0,b0,acilla0,acilla1):
    circuit.ccx(a0,b0,acilla0)
    circuit.cx(a0, acilla1)
    circuit.cx(b0, acilla1)
    circuit.cx(acilla0, acilla1)
    circuit.cx(a0, b0)
def step1_uncomputation(circuit,a0,b0,acilla0,acilla1):
    circuit.cx(acilla0, acilla1)
    circuit.cx(a0, acilla1)
    circuit.ccx(a0,acilla1,acilla0)
def step2(circuit,p_i,g_i,p_ii,g_ii,acilla0,acilla1):
    circuit.ccx(p_i, p_ii, acilla0)
    circuit.append(OR_gate, [g_i, g_ii, acilla1])
def step2_last(circuit,g_i,g_ii,acilla1):
    circuit.append(OR_gate, [g_i, g_ii, acilla1])
def step2_uncomputation(circuit,p_i,g_i,p_ii,g_ii,acilla0,acilla1):
    circuit.append(OR_gate, [g_i, g_ii, acilla1])
    circuit.ccx(p_i, p_ii, acilla0)
def step2_last_uncomputation(circuit,g_i,g_ii,acilla1):
    circuit.append(OR_gate, [g_i, g_ii, acilla1])
###################################################################
def step3_G(circuit,gx,px,gy,py,acilla0, acilla1): #p0=0,p1=0; g0=gl0
    circuit.ccx(gy,px, acilla0)
    circuit.append(OR_gate, [gx,acilla0, acilla1])
def step3_P(circuit,px,py,acilla2): #p0=0,p1=0; g0=gl0
    circuit.ccx(py,px, acilla2)
#(gx, px) ◦ (gy, py) = (gx + px · gy, px · py) (10)
#Hi = Gi + Pi−1 · Gi−2, Hi=final G?
def propagation(circuit,gx,px,gy,py,ancilla_base): #gp
    ancilla1=ancilla_base+1
    ancilla2=ancilla_base+2
    p_next=px
    #g_next=gx|p_special&gy #00 0
    print("G")
    step3_G(circuit, gx, px, gy, py,ancilla_base, ancilla1)
    g_next=ancilla1
    ancilla_base=ancilla1+1
    #g_next = gx | gy & px  # 00 0
    if (py!=3) and (px!=3):
        print("P")
        step3_P(circuit,px,py,ancilla2)
        p_next=ancilla2
        ancilla_base=ancilla2+1
    return g_next,p_next,ancilla_base#p_next


""" Utility functions"""
pow2 = lambda x: (2 ** x)
log2 = lambda x: x.bit_length()

'''Brent Kung Tree'''
def BKTree(bitwidth):
    log2_bitwidth = log2(bitwidth - 1)  # Upsweep length for BK
    """ Creates the prefix tree.         
    """
    bitwidth_i = bitwidth - 1  # Counting from 0
    matrix = [[None for i in range(bitwidth_i)] for i in range(bitwidth_i)]
    for idx_row in range(log2_bitwidth):
        shift_length = pow2(idx_row + 1)  # Shift lenght; Sequence in the loop 2, 4, 8, 16..
        starting_index = shift_length - 2  # Starting indexes in the matrix; Sequence in the loop 0 2 6 14 ...
        starting_value = pow2(
            idx_row) - 1  # Starting values in the matrix; Sequence in the loop 0 1 3 7 15(shift_length/2 - 1)
        # Mades the row values and indexes sequences
        values_seq = list(range(starting_value, bitwidth_i, shift_length))
        indexes_seq = list(range(starting_index, bitwidth_i, shift_length))
        if not indexes_seq:  # There is no other index
            continue
            # If the root of prefixtree wasnt saved yet. The index (bitwidth) is not power of two.
            # indexes_seq = [bitwidth_i - 1] # Save the right-most index {The index of index -> (-1 -1)}
        # Fill the row
        for index, val in zip(indexes_seq, values_seq):
            matrix[idx_row][index] = val
    """ Creates the inverse tree. 
    """
    for idx_row in range(1, log2_bitwidth + 1):
        shift = 2 ** idx_row  # Sequence  2 4 8 16 32
        values_start = shift - 1  # Sequence 1 3 7 15
        indexes_start = (-4 + 3 * (2 ** idx_row)) // 2  # Sequence 1 4 10 22 46 etc.
        values = range(values_start, bitwidth_i, shift)
        indexes = range(indexes_start, bitwidth_i, shift)
        # Fill the row
        for index, val in zip(indexes, values):
            matrix[-idx_row][
                index] = val  # Do not manipulate with idx_row, else it will not be usable for Lander Sklansky and Han Carlson adders
    return matrix

def Brent_Kung(circuit,g_location, p_location,ancilla_base):
    print("BK_Begin")
    print("length", len(g_location))
    bit_num = len(g_location)
    # establish bit_num BK tree, do propagation and generation
    BK_Matrix = BKTree(bit_num)
    size = bit_num - 1
    print("BKtest","g_location", g_location, "p_location", p_location)
    for i in range(size):
        for j in range(size):
            if BK_Matrix[i][j] != None:  # j小了一个1
                index_now = j + 1
                if BK_Matrix[i][j]==0:
                    p_location_x=0
                else:
                    p_location_x = p_location[BK_Matrix[i][j]-1]
                #列表p左移，G3,P2
                print("g_"+str(index_now),g_location[index_now],
                      "p_"+str(index_now),p_location[index_now],
                      "g_"+str(BK_Matrix[i][j]),g_location[BK_Matrix[i][j]],
                      "p_"+str(BK_Matrix[i][j]),p_location_x)
                g_location[index_now], p_location[index_now],ancilla_base= propagation(circuit,g_location[index_now],
                                                                       p_location[index_now],g_location[BK_Matrix[i][j]],
                                                                       p_location[BK_Matrix[i][j]],ancilla_base)
    print(BK_Matrix)
    print("BK_End")
    return ancilla_base

def step3(circuit, p_location, g_location,H_location,ancilla_base):
    print("Ling_Begin")
    print("length", len(g_location))
    bit_num=len(g_location)
    #establish Ling-based Brent Kung Propagation Tree to get H
    G_number = [0 for i in range(add_bit)]
    P_number = [0 for i in range(add_bit)]
    index_BK_1=[i for i in range(0,bit_num,2)]
    index_BK_2 = [i for i in range(1, bit_num, 2)]
    g_BK_1=[g_location[i] for i in index_BK_1]
    p_BK_1 = [p_location[i] for i in index_BK_1]
    g_BK_2=[g_location[i] for i in index_BK_2]
    p_BK_2 = [p_location[i] for i in index_BK_2]
    print("g_location=",g_location,"p_location=",p_location)
    print("g_BK_1",g_BK_1,"p_BK_1",p_BK_1)
    print("g_BK_2",g_BK_2,"p_BK_2",p_BK_2)
    print("index_BK_1",index_BK_1,"index_BK_2",index_BK_2)
    #BK trees=>H
    ancilla_base=Brent_Kung(circuit,g_BK_1, p_BK_1,ancilla_base)
    Brent_Kung(circuit,g_BK_2, p_BK_2,ancilla_base)
    print("After BK")
    print("g_BK_1",g_BK_1,"p_BK_1",p_BK_1)
    print("g_BK_2",g_BK_2,"p_BK_2",p_BK_2)
    for i in range(len(index_BK_1)):
        G_number[index_BK_1[i]]=g_BK_1[i]
        #print("G_"+str(index_BK_1[i]),g_BK_1[i])
        P_number[index_BK_1[i]]=p_BK_1[i]
        #print("P_"+str(index_BK_1[i]),p_BK_1[i])
    for i in range(len(index_BK_2)):
        G_number[index_BK_2[i]]=g_BK_2[i]
        #print("G_"+str(index_BK_2[i]),g_BK_2[i])
        P_number[index_BK_2[i]]=p_BK_2[i]
        #print("P_"+str(index_BK_2[i]),p_BK_2[i])
    print(G_number,P_number)
    # H_BK_1=Brent_Kung(g_BK_1,p_BK_1)
    # H_BK_2=Brent_Kung(g_BK_2, p_BK_2)
    for i in range(bit_num):
        H_location[i] = G_number[i]
        #H_number[i] = G_number[i]|(P_number[i-1]&G_number[i-2])
    print("G0", G_number[0],"g0",g_location[0])
    H_location[0] = g_location[0]  # H0 = g0
    print("Ling_End")
    print("H",H_location)
    return H_location,G_number,P_number
###################################################################
def step4(H_i, d_ii, p_i):
    # circuit.cx(d_ii, p_i)
    # circuit.cswap(H_i, d_ii, p_i)
    circuit.ccx(H_i, p_i, d_ii)
def step4_last(H_i,p_i,acilla0):
    circuit.ccx(H_i,p_i, acilla0)
'''Establish the proposed adder'''
#Step 1
for index in range(add_bit):
    step1(circuit, 4*index, 4*index+1, 4*index+2, 4*index+3) #d=4*index+1,g=4*index+2,p=4*index+3
    print("Step 1",4*index, 4*index+1, 4*index+2, 4*index+3)
circuit.barrier()

#Step 2
p_location=[0 for i in range(add_bit)]
g_location=[0 for i in range(add_bit)]
p_location[0]=3
p_location[1]=3
g_location[0]=2

Step2_ancilla_base=4*add_bit
ancilla_base=Step2_ancilla_base
odd_count=add_bit-1
even_count=add_bit-1
if (add_bit-1)%2==0:
    odd_count=odd_count-1
else:
    even_count=even_count-1
for index in range(0, even_count, 2):
    print("Step2_even", index)
    step2(circuit, 4 * index + 3, 4 * index + 2, 4 * (index + 1) + 3, 4 * (index + 1) + 2, ancilla_base,ancilla_base + 1)
    p_location[index+2]=ancilla_base
    g_location[index+1] = ancilla_base+1
    if index==0:
        H2=ancilla_base + 1
    ancilla_base=ancilla_base+2
if even_count!=add_bit-1:
    print("Step2_last", even_count)
    index=even_count
    step2_last(circuit, 4 * index + 2, 4 * (index + 1) + 2, ancilla_base)
    g_location[index+1] = ancilla_base
    ancilla_base = ancilla_base + 1
#circuit.barrier()
for index in range(1, odd_count , 2):
    print("Step2_odd", index)
    step2(circuit, 4 * index + 3, 4 * index + 2, 4 * (index + 1) + 3, 4 * (index + 1) + 2, ancilla_base,ancilla_base + 1)
    p_location[index+2]=ancilla_base
    g_location[index+1] = ancilla_base+1
    ancilla_base=ancilla_base+2
if odd_count != add_bit-1:
    print("Step2_last", odd_count)
    index = odd_count
    step2_last(circuit, 4 * index + 2, 4 * (index + 1) + 2, ancilla_base)
    g_location[index+1] = ancilla_base
    ancilla_base = ancilla_base + 1
print("ancilla_base",ancilla_base)
print("p",p_location)
print("g",g_location)
circuit.barrier()
# GL0=g0
# PL1=8
# GL1=9
# step2_last(circuit,g2,g3,20)
# GL3=20

#Step 3
#G0=g0
#P0=0,P1=0,前两个操作不做
#输入所有p，g的位置
H_location=[0 for i in range(add_bit)]
step3(circuit, p_location, g_location,H_location,ancilla_base)
#H_location=step3(circuit, p_location, g_location,H_location)
#[2,17,22,24]
circuit.barrier()
#Step 4
# step4(H0,d1,p0), step4(H1,d2,p1)
H1=2
index=1
#S0
step4(H1,4*index+1,4*(index-1)+3) #Hi-1,di,pi-1
index=2
step4(H2,4*index+1,4*(index-1)+3)
'''Hi位置怎么定'''
for index in range(3,add_bit):
    step4(H_location[index-1],4*index+1,4*(index-1)+3) #d=4*index+1,g=4*index+2,p=4*index+3
    print("H_location",H_location[index])
    print("Step 4",4*index+1,4*(index-1)+3)
index=add_bit-1
#最后两位，Hn,Sn+1 16,12,
step4_last(H_location[add_bit-1],4*index+3,total_qubit_number-1)#last qubit
circuit.barrier()

print("Uncomputation")
#Step 2-Uncomputation
if odd_count != add_bit-1:
    ancilla_base = ancilla_base - 1
    print("Step2_last", odd_count)
    index = odd_count
    step2_last_uncomputation(circuit, 4 * index + 2, 4 * (index + 1) + 2, ancilla_base)

for index in range(odd_count-2,-1 , -2):
    print("Step2_odd", index)
    ancilla_base = ancilla_base - 2
    step2_uncomputation(circuit, 4 * index + 3, 4 * index + 2, 4 * (index + 1) + 3, 4 * (index + 1) + 2, ancilla_base,ancilla_base + 1)
if even_count!=add_bit-1:
    print("Step2_last", even_count)
    ancilla_base = ancilla_base - 1
    index=even_count
    step2_last_uncomputation(circuit, 4 * index + 2, 4 * (index + 1) + 2, ancilla_base)
for index in range(even_count-2, -2, -2):
    print("Step2_even", index)
    ancilla_base=ancilla_base-2
    step2_uncomputation(circuit, 4 * index + 3, 4 * index + 2, 4 * (index + 1) + 3, 4 * (index + 1) + 2, ancilla_base,ancilla_base + 1)
circuit.barrier()
#################################################################
#Step 1-Uncomputation
for index in range(add_bit-1,-1,-1):
    step1_uncomputation(circuit, 4*index, 4*index+1, 4*index+2, 4*index+3) #d=4*index+1,g=4*index+2,p=4*index+3
    print("Step 1",4*index, 4*index+1, 4*index+2, 4*index+3)
circuit.barrier()


'''Simulation'''
print("Simulation")
# measure_list=[1,5,11,17,25] #S0,1,2,3,4
measure_list=[1+i*4 for i in range(add_bit)]
measure_list.append(total_qubit_number-1)
circuit.measure(measure_list, range(add_bit+1))
print("Finish setting")
# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')
# Execute
print("Execute")
result = execute(circuit, simulator, shots=3, memory=True).result()
print("memory")
memory = result.get_memory(circuit)
print(memory)
print("real sum =",rand_sum )
flag=0
S_number=memory[0]
for i in range(add_bit+1):
    if S_number[i]!=str(rand_sum[i]):
        flag=flag+1
        print("i",i,S_number[i],int(rand_sum[i]))
        # Si = Hi−1 · di + Hi−1 · (di ⊕ pi−1) , if 0 < i < n
        # Si = (Hi−1 * pi−1) ⊕ di
if flag==0:
    print("Corret!")
else:
    print("Wrong!",flag)

'''Draw Diagram'''
#print(circuit.draw(output='latex_source'))
# circuit.draw(output='mpl')
# plt.show()



