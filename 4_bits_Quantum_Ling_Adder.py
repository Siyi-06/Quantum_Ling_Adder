from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.extensions.quantum_initializer.initializer import Initialize
import matplotlib.pyplot as plt
import random

'''Important settings'''
total_qubit_number=26
s_number=5
add_bit=4

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
def step3(circuit,GL_i,PL_ii,GL_iii,acilla0,acilla1):
    circuit.ccx(GL_i,PL_ii, acilla0)
    circuit.append(OR_gate, [GL_iii,acilla0, acilla1])
def step3_uncomputation(circuit, GL_i, PL_ii, GL_iii, acilla0, acilla1):
    circuit.append(OR_gate, [GL_iii, acilla0, acilla1])
    circuit.ccx(GL_i, PL_ii, acilla0)
def step4(H_i,d_ii,p_i):
    # circuit.cx(d_ii,p_i)
    # circuit.cswap(H_i,d_ii,p_i)
    circuit.ccx(H_i, p_i, d_ii)
def step4_last(H_i,p_i,acilla0):
    circuit.ccx(H_i,p_i, acilla0)


'''Whole structure'''
circuit = QuantumCircuit(total_qubit_number,s_number)
print("4 bits quantum Ling adder")

'''initialize'''
'''random addition'''
rand_int_a = random.randint(0, 2**add_bit-1)
rand_addend_a = bin(rand_int_a)[2:].zfill(add_bit)
rand_int_b = random.randint(0, 2**add_bit-1)
rand_addend_b = bin(rand_int_b)[2:].zfill(add_bit)
print("a =",rand_addend_a ,"b =",rand_addend_b)
rand_int_sum=rand_int_a+rand_int_b
rand_sum = bin(rand_int_sum)[2:].zfill(add_bit+1)
print("real sum =",rand_sum )

# rand_addend_a=1010
# rand_addend_b=1101

Initial_state='00000000'+rand_addend_b[0]+rand_addend_a[0]+'0000'+rand_addend_b[1]+rand_addend_a[1]+'0000'+rand_addend_b[2]+rand_addend_a[2]+'00'+rand_addend_b[3]+rand_addend_a[3]
print("Initial_state",Initial_state)
circuit.append(Initialize(Initial_state), range(26))

'''Establish the proposed adder'''
#################################################################
step1(circuit,0,1,2,3)
d0=1
g0=2
p0=3
step1(circuit,4,5,6,7)
d1=5
g1=6
p1=7
step1(circuit,10,11,12,13)
d2=11
g2=12
p2=13
step1(circuit,16,17,18,19)
d3=17
g3=18
p3=19
circuit.barrier()
#################################################################
step2(circuit,p0,g0,p1,g1,8,9)
GL0=g0
PL1=8
GL1=9
step2_last(circuit,g2,g3,20)
GL3=20

step2(circuit,p1,g1,p2,g2,14,15)
PL2=14
GL2=15
circuit.barrier()
#################################################################
H0=GL0
H1=GL1
step3(circuit,GL0,PL1,GL2,21,22)
H2=22
step3(circuit,GL1,PL2,GL3,23,24)
H3=24
circuit.barrier()
#################################################################
step4(H0,d1,p0)
step4(H1,d2,p1)
step4(H2,d3,p2)
step4_last(H3,p3,25)
circuit.barrier()
#################################################################
######################Uncomputation##############################
#################################################################
'''
step3_uncomputation(circuit,GL1,PL2,GL3,23,24)
step3_uncomputation(circuit,GL0,PL1,GL2,21,22)
circuit.barrier()
'''
#################################################################
step2_uncomputation(circuit,p1,g1,p2,g2,14,15)
step2_last_uncomputation(circuit,g2,g3,20)
step2_uncomputation(circuit,p0,g0,p1,g1,8,9)
circuit.barrier()
#################################################################
step1_uncomputation(circuit,0,1,2,3)
step1_uncomputation(circuit,4,5,6,7)
step1_uncomputation(circuit,10,11,12,13)
step1_uncomputation(circuit,16,17,18,19)
circuit.barrier()
#################################################################



'''Simulation'''
print("Simulation")
measure_list=[1,5,11,17,25] #S0,1,2,3,4
circuit.measure(measure_list, range(5))
print("Finish setting")
# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')
# Execute
print("Execute")
result = execute(circuit, simulator, shots=3, memory=True).result()
print("memory")
memory = result.get_memory(circuit)
print(memory)


'''Draw Diagram'''
# print(circuit.draw(output='latex_source'))
# circuit.draw(output='mpl')
# plt.show()