import random
'''Important settings'''
add_bit=100
s_number=add_bit+1

'''Randomly set a and b, calculate the correct sum real_sum'''
rand_int_a = random.randint(0, 2**add_bit-1)
rand_addend_a = bin(rand_int_a)[2:].zfill(add_bit)
rand_int_b = random.randint(0, 2**add_bit-1)
rand_addend_b = bin(rand_int_b)[2:].zfill(add_bit)
print("a =",rand_addend_a ,"b =",rand_addend_b)
rand_int_sum=rand_int_a+rand_int_b
rand_sum = bin(rand_int_sum)[2:].zfill(add_bit+1)
print("real_sum =",rand_sum )
a=rand_int_a
b=rand_int_b

'''Step1: calculate pl_i, gl_i, d'''
gl=a&b #gli = ai· bi
pl=a|b #pli = ai + bi
d=a^b  #di = ai ⊕ bi
str_gl = bin(gl)[2:].zfill(add_bit)
str_pl = bin(pl)[2:].zfill(add_bit)
str_d= bin(d)[2:].zfill(add_bit)
print("gl=",str_gl)
print("pl=",str_pl)
print("d=",str_d)

'''step2: precalculation'''
gl_i=bin(gl>>1)[2:].zfill(add_bit-1)
gl_i_1=bin(gl)[2:].zfill(add_bit)[1:]
pl_i=bin(pl>>1)[2:].zfill(add_bit-1)
pl_i_1=bin(pl)[2:].zfill(add_bit)[1:]
# print(int(gl_i,2),gl_i,gl_i_1,pl_i,pl_i_1)
g=int(gl_i,2)|int(gl_i_1,2) #gi = gli + gli−1
p=int(pl_i,2)&int(pl_i_1,2) #pi = pli· pli−1
g_str=(bin(g)[2:]+str_gl[add_bit-1]).zfill(add_bit)
#p_str=(bin(p)[2:]+str_pl[add_bit-1]).zfill(add_bit)
p_str=(bin(p)[2:]+str_pl[add_bit-1]).zfill(add_bit)
print("p_str_fake",p_str)
p_str=(bin(p)[2:][1:]+str(0)+str(0)).zfill(add_bit)
# print(g_str,p_str)

'''Step3: Brent-Kung tree'''
#(gx, px) ◦ (gy, py) = (gx + px · gy, px · py) (10)
#Hi = Gi + Pi−1 · Gi−2, Hi=final G?
def propagation(gx,px,gy,py,p_special): #gp
    #g_next=gx|p_special&gy #00 0
    g_next = gx | gy & px  # 00 0
    #g_next =( gx^gy) ^ (gx ^px)
    p_next=px&py
    return g_next,p_next#p_next


""" Utility functions"""
pow2 = lambda x: (2 ** x)
log2 = lambda x: x.bit_length()


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

def Brent_Kung(g_number, p_number):
    print("BK_Begin")
    print("length", len(g_number))
    bit_num = len(g_number)
    # establish bit_num BK tree, do propagation and generation
    BK_Matrix = BKTree(bit_num)
    size = bit_num - 1
    print("BKtest","g_number", g_number, "p_number", p_number)
    for i in range(size):
        for j in range(size):
            if BK_Matrix[i][j] != None:  # j小了一个1
                index_now = j + 1
                if BK_Matrix[i][j]==0:
                    p_number_x=0
                else:
                    p_number_x = p_number[BK_Matrix[i][j]-1]

                # print("g_"+str(BK_Matrix[i][j]),g_number[BK_Matrix[i][j]],
                #       "p_"+str(BK_Matrix[i][j]-1),p_number_x,
                #       "g_"+str(index_now),g_number[index_now],
                #       "p_"+str(index_now),p_number[index_now],
                #       "p_"+str(index_now-1),p_number[index_now-1])

                #g_number[index_now], p_number[index_now] = propagation(g_number[index_now],
                #                                                       p_number[index_now-1],g_number[BK_Matrix[i][j]],
                #                                                       p_number_x,)

                # g_number[index_now], p_number[index_now] = propagation(g_number[index_now],
                #                                                        p_number[index_now],g_number[BK_Matrix[i][j]],
                #                                                        p_number[BK_Matrix[i][j]],p_number_x)

                #列表p左移，G3,P2
                g_number[index_now], p_number[index_now] = propagation(g_number[index_now],
                                                                       p_number[index_now],g_number[BK_Matrix[i][j]],
                                                                       p_number[BK_Matrix[i][j]],p_number[index_now])
                # print("propagation")
                # #
                # print("g_"+str(BK_Matrix[i][j]),g_number[BK_Matrix[i][j]],
                #       "p_"+str(BK_Matrix[i][j]-1),p_number_x,
                #       "g_"+str(index_now),g_number[index_now],
                #       "p_"+str(index_now),p_number[index_now],
                #       "p_"+str(index_now-1),p_number[index_now-1])

    # print(BK_Matrix)
    print("BK_End")
    return g_number, p_number

def Ling_Brent_Kung(g_number,p_number,H_number):
    print("Ling_Begin")
    print("length", len(g_number))
    bit_num=len(g_number)
    #establish Ling-based Brent Kung Propagation Tree to get H
    G_number = [0 for i in range(add_bit)]
    P_number = [0 for i in range(add_bit)]
    #BK_1,BK_2
    index_BK_1=[i for i in range(0,bit_num,2)]
    index_BK_2 = [i for i in range(1, bit_num, 2)]
    g_BK_1=[g_number[i] for i in index_BK_1]
    p_BK_1 = [p_number[i] for i in index_BK_1]
    g_BK_2=[g_number[i] for i in index_BK_2]
    p_BK_2 = [p_number[i] for i in index_BK_2]
    print("g_number=",g_number,"p_number=",p_number)
    print("g_BK_1",g_BK_1,"p_BK_1",p_BK_1)
    print("g_BK_2",g_BK_2,"p_BK_2",p_BK_2)
    print("index_BK_1",index_BK_1,"index_BK_2",index_BK_2)
    #BK trees=>H
    Brent_Kung(g_BK_1, p_BK_1)
    Brent_Kung(g_BK_2, p_BK_2)
    print("After BK")
    print("g_BK_1",g_BK_1,"p_BK_1",p_BK_1)
    print("g_BK_2",g_BK_2,"p_BK_2",p_BK_2)
    #print(g_number, p_number)
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
        H_number[i] = G_number[i]
        #H_number[i] = G_number[i]|(P_number[i-1]&G_number[i-2])
    print("G0", G_number[0],"g0",g_number[0])
    H_number[0] = g_number[0]  # H0 = g0
    print("Ling_End")
    return H_number,G_number,P_number

g_number=[0 for i in range(add_bit)]
p_number=[0 for i in range(add_bit)]
H_number=[0 for i in range(add_bit)]

for i in range(add_bit):
    g_number[add_bit-1-i]=int(g_str[i])
    # print("g_"+str(add_bit-1-i)+"=",g_number[add_bit-1-i])
for i in range(add_bit):
    p_number[add_bit - 1 - i] = int(p_str[i])
    # print("p_" + str(add_bit - 1 - i) + "=", p_number[add_bit - 1 - i])
print("g=",g_str,"p=",p_str) #list
print("g_number=",g_number,"p_number=",p_number) #list

H_number,G_number,P_number=Ling_Brent_Kung(g_number,p_number,H_number)

print("H",H_number)
print("G",G_number)
print("P",P_number)
'''Step4: Sum'''
S_number=[0 for i in range(add_bit+1)]
#S0 = d0
S_number[0]=int(str_d[::-1][0])
print("d_0",str_d[::-1][0],"S_0",S_number[0])
#Si = Hi−1 · di + Hi−1 · (di ⊕ pi−1) , if 0 < i < n
#Si = (Hi−1 * pi−1) ⊕ di
for i in range(1,add_bit):
    #S_number[i] = (H_number[i - 1] & int(p_number[i - 1])) ^ int(str_d[add_bit - 1 - i])
    #S_number[i] = (H_number[i-1] & int(P_number[i-1])) ^ int(str_d[add_bit - 1 - i])
    S_number[i]=(H_number[i-1]&int(str_pl[::-1][i-1]))^int(str_d[::-1][i])
#Sn = pn · Hn
S_number[add_bit]=int(str_pl[::-1][add_bit-1])&H_number[add_bit-1]
#S_number[add_bit]=p_number[add_bit-1]&H_number[add_bit-1]
#print("p_n=",P_number[add_bit-1]),"H_n=",H_number[add_bit-1])# p=P
#S_number[add_bit]=int(P_number[add_bit-1])&H_number[add_bit-1]
print("p_n=",int(str_pl[::-1][add_bit-1]),"P_n=",P_number[add_bit-1],"p_n=",p_number[add_bit-1],"H_n=",H_number[add_bit-1])  ### p=pl!!!!!!!!!!!!
#print("S_"+str(add_bit)+"=",S_number[add_bit])
#print("S_number_list",S_number)
S_number.reverse()
print("S_number",S_number)
print("Real_sum",rand_sum) #左高右低
# S_number[add_bit]=str(int(str_pl[add_bit-1])&H_number[add_bit-1])
# print("p_n=",int(str_pl[add_bit-1]),"H_n=",H_number[add_bit-1])  ### p=pl!!!!!!!!!!!!
flag=0
for i in range(add_bit+1):
    if S_number[i]!=int(rand_sum[i]):
        flag=flag+1
        print("i",i,S_number[i],int(rand_sum[i]))
        # Si = Hi−1 · di + Hi−1 · (di ⊕ pi−1) , if 0 < i < n
        # Si = (Hi−1 * pi−1) ⊕ di
        print("H_" + str(i - 1), H_number[i - 1], "p_" + str(i - 1), str_pl[::-1][i - 1], "d_" + str(i), str_d[::-1][i])
        print("S_" + str(i), S_number[i])
if flag==0:
    print("Corret!")
else:
    print("Wrong!",flag)
'''
a = 1000110101 b = 1110000101
real_sum = 10110111010
gl= 1000000101
pl= 1110110101
d= 0110110000
g= 1000001111 p= 1100100001
g_number= [1, 1, 1, 1, 0, 0, 0, 0, 0, 1] p_number= [1, 0, 0, 0, 0, 1, 0, 0, 1, 1]
Ling_Begin
length 10
g_number= [1, 1, 1, 1, 0, 0, 0, 0, 0, 1] p_number= [1, 0, 0, 0, 0, 1, 0, 0, 1, 1]
g_BK_1 [1, 1, 0, 0, 0] p_BK_1 [1, 0, 0, 0, 1]
g_BK_2 [1, 1, 0, 0, 1] p_BK_2 [0, 0, 1, 0, 1]
index_BK_1 [0, 2, 4, 6, 8] index_BK_2 [1, 3, 5, 7, 9]
BK_Begin
length 5
BKtest g_number [1, 1, 0, 0, 0] p_number [1, 0, 0, 0, 1]
g_0 1 p_-1 0 g_1 1 p_1 0 p_0 1
propagation
g_0 1 p_-1 0 g_1 1 p_1 0 p_0 1
g_2 0 p_1 0 g_3 0 p_3 0 p_2 0
propagation
g_2 0 p_1 0 g_3 0 p_3 0 p_2 0
g_1 1 p_0 1 g_3 0 p_3 0 p_2 0
propagation
g_1 1 p_0 1 g_3 0 p_3 0 p_2 0
g_1 1 p_0 1 g_2 0 p_2 0 p_1 0
propagation
g_1 1 p_0 1 g_2 0 p_2 0 p_1 0
g_3 0 p_2 0 g_4 0 p_4 1 p_3 0
propagation
g_3 0 p_2 0 g_4 0 p_4 0 p_3 0
BK_End
BK_Begin
length 5
BKtest g_number [1, 1, 0, 0, 1] p_number [0, 0, 1, 0, 1]
g_0 1 p_-1 0 g_1 1 p_1 0 p_0 0
propagation
g_0 1 p_-1 0 g_1 1 p_1 0 p_0 0
g_2 0 p_1 0 g_3 0 p_3 0 p_2 1
propagation
g_2 0 p_1 0 g_3 0 p_3 0 p_2 1
g_1 1 p_0 0 g_3 0 p_3 0 p_2 1
propagation
g_1 1 p_0 0 g_3 0 p_3 0 p_2 1
g_1 1 p_0 0 g_2 0 p_2 1 p_1 0
propagation
g_1 1 p_0 0 g_2 1 p_2 0 p_1 0
g_3 0 p_2 0 g_4 1 p_4 1 p_3 0
propagation
g_3 0 p_2 0 g_4 1 p_4 0 p_3 0
BK_End
After BK
g_BK_1 [1, 1, 0, 0, 0] p_BK_1 [1, 0, 0, 0, 0]
g_BK_2 [1, 1, 1, 0, 1] p_BK_2 [0, 0, 0, 0, 0]
[1, 1, 1, 1, 0, 1, 0, 0, 0, 1] [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
G0 1 g0 1
Ling_End
H [1, 1, 1, 1, 0, 1, 0, 0, 0, 1]
G [1, 1, 1, 1, 0, 1, 0, 0, 0, 1]
P [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
d_0 0 S_0 0
p_n= 1 P_n= 0 p_n= 1 H_n= 1
S_number [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0]
Real_sum 10110111010
i 4 1 0
Wrong! 1
'''