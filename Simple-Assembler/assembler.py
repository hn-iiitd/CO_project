import os
# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011", "R4": "100","R5": "101", "R6": "110", "FLAGS": "111"}  # Register numbers
O_A = {"add": "00000", "sub": "00001", "mul": "00110", "xor": "01010","or": "01011", "and": "01100", "addf": "10000" , "subf": "10001", "addf": "10000" , "subf": "10001" }    # Labelling operations in A
O_B = {"mov": "00010", "rs": "01000", "ls": "01001", "movf": "10010"}                                                    # Labelling operations in B
O_C = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}                                  # Labelling operations in C
O_D = {"ld": "00100", "st": "00101"}                                                                    # Labelling operations in D
O_E = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}                                   # Labelling operations in E
O_F = {"hlt": "11010"}    
O_G = {"movf": "10010"}      
# O_bonus={'reset':'10011','nop':'10100','inc':'10101','dec':'10110','addi':'10111'}         
O_nop_reset={'reset':'10011','nop':'10100'}
O_inc_dec={'inc':'10101','dec':'10110'}                                                                  # Labelling operations in F
O_add_imm={'addi':'10111'}
O = ["reset","nop","inc","dec","addi","add", "sub", "mul", "xor", "or", "and", "mov", "rs", "ls", "div","not", "cmp", "ld", "st", "jmp", "jlt", "jgt", "je", "hlt", "FLAG","addf", "subf", "movf"]
variables = {}
c_hlt = 0
counter = 0
flag = 0
check_hlt_after = 0
l_result = []
l_cmd = []
l_var = []
l_var_def = [] 

def add(r1, r2):
    sum = bin(int(r1) + int(r2))
    return sum[2:]
vl = []

def float_to_bin(a):
    
    l=a.split(".")
    q=bin(int(l[0]))
    q=q[2:]

    
    d=float('0.'+l[1])
    g=q[1:]
    while(d!=0):
        d=d*2
        e=str(d)
        
        l1=e.split(".")
        g+=l1[0]
        d=float('0.'+l1[1])
    
    d=str(d)
    x=0
    x=len(q[1:])+3
    if len(g)<5:

        for i in range(5-len(g)):
            g+='0'

    x=str(bin(x))
    x=x[2:]

    c=l[0][1:]+l[1]
    if len(x)<3:
        j=''
        for i in range(3-len(x)):
            j+='0'
        j+=x
        return j+g
    else:
        return x+g

# Function to convert Type A command to machine code
def convert_OA(a):
    if (a in O_A.keys()):
        x = O_A[a] + "00"  # Unused BITS
        return x
    if (a in R):
        return R[a]

# Function to convert Type B command to machine code
def convert_OB(a):
    if (a in O_B.keys()):
        x = O_B[a] + "0"  # Unused BITS
        return x
    if (a in R):
        return R[a]
    else:
        a = a.replace("\n", "")
        a = a.replace("$", "")
        num = str(bin(int(a)))
        left_over = 9-len(num)
        x = '0'*left_over+num[2:]
        return x

# Function to convert Type C command to machine code
def convert_OC(a):
    if (a in O_C.keys()):
        x = O_C[a] + '00000'
        return x
    else:
        return R[a]

# Function to convert Type D command to machine code
def convert_OD(a):
    if (a in O_D.keys()):
        x = O_D[a]
        return x + '0'
    elif (a in R):
        x = R[a]
        return x
    else:
        return variables[a]
    
def convert_O_nop_reset(a):
    if (a in O_nop_reset.keys()):
        
        x=O_nop_reset[a]
        return x+'0'*(16-5)
def convert_O_add_imm(a):
    if (a in O_add_imm.keys()):
        x=O_add_imm[a]+'0'
        return x
    if a in R:
        return R[a]
    else:
        a=a.replace('\n', '').replace("$", '')
        num=str(bin(int(a)))[2:]
        x='0'*(7-len(num))+num
        return x
def convert_O_inc_dec(a):
    if a in O_inc_dec:
        x=O_inc_dec[a]
        return x+8*'0'
    if a in R:
        return R[a]
def convert_OG(a) :
    if (a in O_G.keys()):
        x = O_G[a]  # Unused BITS
        return x
    if (a in R):
        return R[a]
    else:
        a = a.replace("\n", "")
        a = a.replace("$", "")
        
        return float_to_bin(a)

def variable_maker():
    global counter
    tot=0
    var_c=0
    file = "input_file.txt"
    f = open(file, 'r')

    for line in f:
        line=line.strip()
        line=line.split()
        if line==[]:
            # counter+=1
            continue
        elif line[0]=='var':
            var_c+=1
    f.seek(0)
    for line in f:
        line=line.replace('\n', '')
        if line=='':
            continue
        else:
            line = line.strip()
            k = line.split(":")
            if (len(k) > 1):
                line = k[1]
                line = line.strip()
                variables[k[0]]='0'*(7-len(bin(tot-var_c)[2:]))+bin(tot-var_c)[2:]
            tot+=1
            l = line.split(" ")
            if l[0] == "var" or l[0][-1]==':':
                l[1] = l[1].replace("\n", "")
                if (len(variables.keys()) == 0):
                    variables[l[1]] = add(counter-var_c-1,1)#"0000001"
                    variables[l[1]] ='0'*(7-len(variables[l[1]]))+variables[l[1]]
                    vl.append(variables[l[1]])
                else:
                    variables[l[1]] = add(int(vl[-1],2), 1)
                    variables[l[1]] = "0"*(7-len(variables[l[1]])) + variables[l[1]]
                    vl.append(variables[l[1]])
    

# Reading instructions from file and giving machine code in the output file
def file_work():
    file = "input_file.txt"
    f = open(file, 'r')
    out = open("output_file.txt", 'w+')
    for line in f:
        line = line.strip()
        k = line.split(":")
        if (len(k) > 1):
            line = k[1]
            line = line.strip()
        l = line.split(" ")
        l = line.split(" ")
        if l[0] in O_A.keys():
            out.write(convert_OA(l[0]))
            out.write(convert_OA(l[1]))
            out.write(convert_OA(l[2]))
            l[3] = l[3].replace("\n", "")
            out.write(convert_OA(l[3]))
            out.write("\n")
        elif l[0] in O_B.keys() and l[2][0] == '$':
            out.write(convert_OB(l[0]))
            out.write(convert_OB(l[1]))
            out.write(convert_OB(l[2]))
            out.write("\n")
        elif l[0] in O_C.keys():
            out.write(convert_OC(l[0]))
            out.write(convert_OC(l[1]))
            l[2] = l[2].replace("\n", "")
            out.write(convert_OC(l[2]))
            out.write("\n")
        elif l[0] in O_D.keys():
            out.write(convert_OD(l[0]))
            out.write(convert_OD(l[1]))
            l[2] = l[2].replace("\n", "")
            out.write(convert_OD(l[2]))
            out.write("\n")
        elif l[0] in O_E.keys():
            out.write(O_E[l[0]] + "0"*4)
            l[1] = l[1].replace("\n", "")
            out.write(variables[l[1]])
            out.write("\n")
        elif l[0] in O_F.keys():
            out.write(O_F[l[0]] + "0" * 11)
        elif l[0] in O_add_imm:
            out.write(convert_O_add_imm(l[0]))
            out.write(convert_O_add_imm(l[1]))
            l[2] = l[2].replace("\n", "")
            out.write(convert_O_add_imm(l[2]))
            out.write('\n')
        elif l[0] in O_inc_dec:
            out.write(convert_O_inc_dec(l[0]))
            out.write(convert_O_inc_dec(l[1]))
            out.write('\n')
        elif l[0] in O_nop_reset:
            out.write(convert_O_nop_reset(l[0]))
            out.write('\n')
        elif l[0] in O_G.keys() and l[2][0] == '$':
            out.write(convert_OG(l[0]))
            out.write(convert_OG(l[1]))
            out.write(convert_OG(l[2]))
            out.write("\n")
        else:
            pass
    f.close()
    out.close()

# check for extra spaces in the instructions
def check_space(k):
    global counter, f2
    if '' in k:
        f2.write(f"Error: Extra space in line {counter}\n")
        return 1
    return 0

# Check for errors in Type A
def check_A(k):
    global counter, f2
    l_errors = []
    if len(k) != 4:
        l_errors.append(
            f"Error in Line {counter}: {k[0]} must contain 3 parameters")
    else:
        if (k[1] not in R or k[2] not in R or k[3] not in R):
            l_errors.append(
                f"Error in Line {counter}: Register is not defined")

        if k[1] == "FLAGS" or k[2] == "FLAGS" or k[3] == "FLAGS":
            l_errors.append(
                f"Incorrect use of FLAGS register in line {counter}")

    if len(l_errors) == 0:

        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1
def check_OG(k):
    global counter, f2
    l_errors = []
    if (len(str(bin(int(k[2][1:])))[2:])) > 8:
            l_errors.append(
                f"Illegal Immediate values (more than 8 bits) at line {counter}")
    if len(k) != 3:
            l_errors.append(
                f"Error in Line {counter}: {k[0]} must contain 2 parameters")
    else:
            if k[1] == "FLAGS" or k[2] == "FLAGS":
                l_errors.append(
                    f"Incorrect use of FLAGS register in line {counter}")
            if k[1] not in R:
                l_errors.append(
                    f"Error in Line {counter}: Register is not defined")
    if len(l_errors) == 0:
            return 0
    else:
            for i in l_errors:
                f2.write(i+'\n')
            return 1
    
# Check for errors in mov statements
def check_mov(k):
    global counter, f2
    l_errors = []
    if k[-1][0] == '$':
        if (len(str(bin(int(k[2][1:])))[2:])) > 7:
            l_errors.append(
                f"Illegal Immediate values (more than 7 bits) at line {counter}")
        if len(k) != 3:
            l_errors.append(
                f"Error in Line {counter}: {k[0]} must contain 2 parameters")
        else:
            if k[1] == "FLAGS" or k[2] == "FLAGS":
                l_errors.append(
                    f"Incorrect use of FLAGS register in line {counter}")
            if k[1] not in R:
                l_errors.append(
                    f"Error in Line {counter}: Register is not defined")
        if len(l_errors) == 0:
            return 0
        else:
            for i in l_errors:
                f2.write(i+'\n')
            return 1
    else:
        if len(k) != 3:
            l_errors.append(
                f"Error in Line {counter}: {k[0]} must contain 2 parameters")
        else:
            if k[1] == "FLAGS":
                l_errors.append(
                    f"Incorrect use of FLAGS register in line {counter}")

            if k[1] not in R or k[2] not in R:
                l_errors.append(
                    f"Error in Line {counter}: Register is not defined")
        if len(l_errors) == 0:
            return 0
        else:
            for i in l_errors:
                f2.write(i+'\n')
            return 1

# Check for errors in TYPE B statements
def check_B(k):
    global counter, f2
    l_errors = []
    if (len(str(bin(int(k[2][1:])))[2:])) > 7:
        l_errors.append(
            f"Illegal Immediate values (more than 7 bits) at line {counter}")

    if len(k) != 3:
        l_errors.append(
            f"Error in Line {counter}: {k[0]} must contain 2 parameters")

    else:
        if (k[1] not in R):
            l_errors.append(
                f"Error in Line {counter}: Register is not defined")
        if k[1] == "FLAGS":
            l_errors.append(
                f"Incorrect use of FLAGS register in line {counter}")
    if len(l_errors) == 0:
        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1

# Check for errors in TYPE C statements
def check_C(k):
    global counter, f2
    l_errors = []
    if len(k) != 3:
        l_errors.append(f"Error in Line {counter}: {k[0]} must contain 2 parameters")
    else:
        if k[1] == "FLAGS" or k[2] == "FLAGS":
            l_errors.append(f"Incorrect use of FLAGS register in line {counter}")

        if k[1] not in R or k[2] not in R:
            l_errors.append(f"Error in Line {counter}: Register is not defined")
    if len(l_errors) == 0:
        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1

# Check for errors in TYPE D statement
def check_D(k):
    global counter, f2
    l_errors = []
    if len(k) != 3:
        l_errors.append(
            f"Error in Line {counter}: {k[0]} must contain 2 parameters")
    else:

        if k[1] == "FLAGS":
            l_errors.append(
                f"Incorrect use of FLAGS register in line {counter}")

        if k[1] not in R:
            l_errors.append(f"Error in Line {counter}: Register is not defined")
    if len(l_errors) == 0:
        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1

# Check for errors in TYPE E statements
def check_E(k):
    global counter, f2
    if len(k) != 2:
        f2.write(f"Error in Line {counter}: {k[0]} must contain 1 parameters\n")
        return 1
    return 0
def check_nop_reset(k):
    global counter, f2
    if len(k) != 1:
        f2.write(f"Error in Line {counter}: {k[0]} must contain 0 parameters\n")
        return 1
    return 0

def check_inc_dec(k):
    global counter, f2
    l_errors=[]
    if len(k)!=2:
        l_errors.append(f"Error in Line {counter}: {k[0]} must contain 1 parameters\n")
    else:
        if k[1]=="FLAGS":
            l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        if k[1] not in R:
            l_errors.append(f"Error in Line {counter}: Register is not defined")
    if len(l_errors) == 0:
        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1
def check_add_imm(k):
    global counter,f2
    l_errors=[]
    if (len(str(bin(int(k[2][1:])))[2:])) > 7:
        l_errors.append(
            f"Illegal Immediate values (more than 7 bits) at line {counter}")
    if len(k)!=3:
        l_errors.append(f"Error in Line {counter}: {k[0]} must contain 2 parameters\n")
    else:
        if k[1]=='FLAGS':
            l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        if k[1] not in R:
            l_errors.append(f"Error in Line {counter}: Register is not defined")
        
    if len(l_errors) == 0:
        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1

# Check for errors in TYPE F statements
def check_F(k):
    global counter, f2
    if (len(k) != 1):
        f2.write(f"Error in Line {counter}: {k[0]} must contain no parameters\n")
        return 1
    
    return 0

def var(k):
    if k[-1] == '\n':
        k = k[:-1]
    l2=[]
    l3=[]
    l = k.strip().split(" ")
    for i in l:
        l2=i.split('\t')
        for j in l2:
            l3.append(j)
    l_cmd.append(l3[0])
    if l3 == ['']:
        return
    if (l3[0] in O or l3[0] == 'var' or l3[0][-1] == ':'):
        if l3[0] == 'var':
            l_var_def.append(l3[1])
        elif l3[0][-1] == ':':
            l_var_def.append(l3[0][:-1])
def check_var_def(k):
    global counter, f2
    if k[0] == "jmp" or k[0] == "jlt" or k[0] == "jgt" or k[0] == "je":
        if k[1] not in l_var_def:
            f2.write(f"Error on line {counter}:No Label/variable name {k[1]}\n")
            return 1
    else:
        if k[2] not in l_var_def:
            f2.write(
                f"Error on line {counter}:No such memory address named {k[2]} exist\n")
            return 1
    return 0

def error_controller(k):
    global c_hlt, l_cmd, counter, flag, check_hlt_after, l_result, f2
    if k[-1] == '\n':
        k = k[:-1]
    l2=[]
    l3=[]
    l = k.strip().split(" ")
    for i in l:
        l2=i.split('\t')
        for j in l2:
            l3.append(j)
    l_cmd.append(l3[0])
    if l3 == ['']:
        return
    if (l3[0] in O or l3[0] == 'var' or l3[0][-1] == ':'):
        counter += 1
        if flag == 1 and l[0] == 'var':
            f2.write(
                f"Error in Line {counter}: Variables must be declared at the very beginning\n")
            l_result.append(1)
        l_result.append(check_space(l3))
        if l3[0] == "jmp" or l3[0] == "jlt" or l3[0] == "jgt" or l3[0] == "je":
            l_result.append(check_var_def(l3))
        elif l3[0] == "ld" or l3[0] == "st":
            l_result.append(check_var_def(l3))
        if l3[0] == "mov":
            flag = 1
            l_result.append(check_mov(l3))
        elif l3[0] in O_A:
            flag = 1
            l_result.append(check_A(l3))
        elif l3[0] in O_G:
            flag=1
            l_result.append(check_OG(l3))
        elif l3[0] in O_B:
            flag = 1
            l_result.append(check_B(l3))
        elif l3[0] in O_C:
            flag = 1
            l_result.append(check_C(l3))
        elif l3[0] in O_D:
            flag = 1
            l_result.append(check_D(l3))
        elif l3[0] in O_E:
            flag = 1
            l_result.append(check_E(l3))
        elif l3[0] in O_F:
            flag = 1
            c_hlt += 1
            if c_hlt == 1:
                check_hlt_after = counter
                l_result.append(check_F(l3))
            elif c_hlt > 1:
                l_result.append(1)
                f2.write("hlt operation used more than once\n")
        elif l3[0] in O_add_imm:
            flag = 1
            l_result.append(check_add_imm(l3))
        elif l3[0] in O_inc_dec:
            flag = 1
            l_result.append(check_inc_dec(l3))
        elif l3[0] in O_nop_reset:
            flag = 1
            l_result.append(check_nop_reset(l3))
    else:
        counter += 1
        f2.write(f"Error in Line {counter}: Invalid operand\n")
        l_result.append(1)
    return l_result

def check_hlt():
    global f2
    if 'hlt' not in l_cmd:
        f2.write("Error: No hlt instruction present\n")
        a.append(1)

    elif 'hlt' != l_cmd[-1]:
        f2.write("Cant execute command after halt\n")
        a.append(1)
        exit()
file = "input_file.txt"

f2 = open('output_file.txt', 'w')
f=open(file, 'w')
while (1):
    try:
        
        line = input()
        f.write(line+'\n')
    except EOFError:
        break
f.close()
# To make a list of all variables , labels and memory addresses
f = open(file, 'r')
f2=open("output_file.txt", 'w+')
for line in f:
    var(line)
f.seek(0)
a=[]
# for error checking
for line in f:
    u = line.split(":")
    if (len(u) > 1):
        line=u[1].strip()
    a = error_controller(line)
check_hlt()

# will run this if there is no error
variable_maker()
if 1 not in a:
    file_work()
f2.seek(0)
for i in f2:
    if i[-1]=='\n':
        
        print(i[:-1])
    else:
        print(i)
    
os.remove(file)
os.remove("output_file.txt")
f.close()
f2.close()
