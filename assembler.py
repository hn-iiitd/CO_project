# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011","R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
O_A = {"add": "00000", "sub": "00001", "mul": "00110","xor": "01010", "or": "01011", "and": "01100"}
O_B = {"mov": "00010", "rs": "01000", "ls": "01001"}
O_C = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}
O_D = {"ld": "00100", "st": "00101"}
O_E = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
O_F = {"hlt": "11010"}
O = ["add", "sub", "mul", "xor", "or", "and", "mov", "rs", "ls", "div",
     "not", "cmp", "ld", "st", "jmp", "jlt", "jgt", "je", "hlt", "FLAG"]
variables = {}


def add(r1, r2):
    sum = bin(int(r1) + int(r2))
    return sum[2:]


vl = []


def convert_OA(a):
    if (a in O_A.keys()):
        x = O_A[a] + "00"  # Unused BITS
        return x
    if (a in R):
        return R[a]


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


def convert_OC(a):
    if (a in O_C.keys()):
        x = O_C[a] + '00000'
        return x
    else:
        return R[a]


def convert_OD(a):
    if (a in O_D.keys()):
        x = O_D[a]
        return x + '0'
    elif (a in R):
        x = R[a]
        return x
    else:
        return variables[a]


def file_work():
    file = "test.txt"
    f = open(file, 'r')
    out = open("out.txt", 'w+')
    for line in f:
        line = line.strip()
        l = line.split(" ")
        if l[0] == "var":
            l[1] = l[1].replace("\n", "")
            if (len(variables.keys()) == 0):
                variables[l[1]] = "0000001"
                vl.append(variables[l[1]])

            else:
                variables[l[1]] = add(vl[len(vl)-1], 1)
                variables[l[1]] = "0" * \
                    (7-len(variables[l[1]])) + variables[l[1]]
                vl.append(variables[l[1]])
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
        else:
            pass
    f.close()

    out.seek(0)
    for i in out:
        if i[-1] == '\n':
            print(i[:-1])
        else:
            f2.write(i)
    out.close()


l_result = []


def check_space(k):
    global counter,f2
    if '' in k:
        f2.write(f"Error: Extra space in line {counter}\n")
        return 1
    return 0
        #exit()


def check_A(k):
    global counter,f2
    l_errors=[]
    if len(k) != 4:
        l_errors.append(f"Error: Wrong instruction syntax for TYPE A register in line {counter}")
    # return 0
        #exit()

    if (k[1] not in R or k[2] not in R or k[3] not in R):
        l_errors.append(f"Error: Incorrect Register name in line {counter}")

        #exit()

    if k[1] == "FLAGS" or k[2] == "FLAGS" or k[3] == "FLAGS":
        l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        #exit()
    if len(l_errors)==0:

        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1


def check_mov(k):
    global counter,f2
    l_errors=[]
    if k[-1][0] == '$':
        if (len(str(bin(int(k[2][1:])))[2:]))>7:
            l_errors.append(f"Illegal Immediate values (more than 7 bits) at line {counter}")
          
        if len(k) != 3:
            l_errors.append(f"Error: Wrong instruction syntax for TYPE B register in line {counter}")
        
            #exit()

        if k[1] == "FLAGS" or k[2] == "FLAGS":
            l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
          
            #exit()

        if k[1] not in R:
            l_errors.append(f"Error: Incorrect Register name in line {counter}")
            #exit()
            
        if len(l_errors)==0:

            return 0
        else:
            for i in l_errors:
                f2.write(i+'\n')
            return 1
            

    else:
        if len(k) != 3:
            l_errors.append(f"Error: Wrong instruction syntax for TYPE C register in line {counter}")
            return 1
            #exit()

        if k[1] == "FLAGS":
            l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
            #exit()
            return 1

        if k[1] not in R or k[2] not in R:
            l_errors.append(f"Error: Incorrect Register name in line {counter}")
            #exit()
            return 1
        if len(l_errors)==0:

            return 0
        else:
            for i in l_errors:
                f2.write(i+'\n')
            return 1
        
    # return 0


def check_B(k):
    global counter,f2
    l_errors=[]
    if (len(str(bin(int(k[2][1:])))[2:]))>7:
        l_errors.append(f"Illegal Immediate values (more than 7 bits) at line {counter}")
      
    if len(k) != 3:
        l_errors.append(f"Error: Wrong instruction syntax for TYPE B register in line {counter}")
        #exit()
       

    if (k[1] not in R or k[2] not in R or k[3] not in R):
        l_errors.append(f"Error: Incorrect Register name in line {counter}")
        #exit()
    

    if k[1] == "FLAGS":
        l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        #exit()

    # if len(str(bin(int(k[2][1:])))[2:])>7:
    #     print( f"Illegal Immediate values (more than 7 bits) at line {counter}")
    #     return 1
    if len(l_errors)==0:

        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1

def check_C(k):
    global counter,f2
    l_errors = []
    if len(k) != 3:
        l_errors.append(f"Error: Wrong instruction syntax for TYPE C register in line {counter}")
        #exit()

    

    if k[1] == "FLAGS" or k[2] == "FLAGS":
        l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        #exit()

    if k[1] not in R or k[2] not in R:
        l_errors.append(f"Error: Incorrect Register name in line {counter}")
        #exit()
    if len(l_errors)==0:

        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1


def check_D(k):
    global counter,f2
    l_errors=[]
    if len(k) != 3:
        l_errors.append(f"Error: Wrong instruction syntax for TYPE D register in line {counter}")
        #exit()

    

    if k[1] == "FLAGS":
        l_errors.append(f"Incorrect use of FLAGS register in line {counter}")
        #exit()


    if k[1] not in R:
        l_errors.append(f"Error: Incorrect Register name in line {counter}")
        #exit()
    if len(l_errors)==0:

        return 0
    else:
        for i in l_errors:
            f2.write(i+'\n')
        return 1



def check_E(k):
    global counter,f2
    if len(k) != 2:

        f2.write(f"Error: Wrong instruction syntax for TYPE E register in line {counter}\n")
        #exit()
        return 1
    return 0 


def check_F(k):
    global counter,f2
    if (len(k) != 1):

        f2.write(f"Error: Wrong instruction syntax for TYPE F register in line {counter}\n")
        #exit()
        return  1
    return 0


c_hlt = 0
counter = 0
flag = 0
check_hlt_after = 0
l_result=[]
l_cmd=[]
l_var=[]
l_var_def=[]
def var(k):
    if k[-1] == '\n':
        k = k[:-1]
    
    l = k.strip().split(" ")
    l_cmd.append(l[0])
    if l == ['']:
        return
    if (l[0] in O or l[0] == 'var' or l[0][-1] == ':'):

        if l[0]=='var':
            l_var_def.append(l[1])
        elif l[0][-1]==':':
            l_var_def.append(l[0][:-1])
# def check
def check_var_def(k):    
    global counter,f2
    if k not in l_var_def:
        f2.write(f"Error on line {counter}:Label not find\n")
        return 1
    return 0
def error_controller(k):
    global c_hlt,l_cmd,counter,flag,check_hlt_after,l_result,f2
    if k[-1] == '\n':
        k = k[:-1]
    l = k.strip().split(" ")
    l_cmd.append(l[0])
    if l == ['']:
        return
    if (l[0] in O or l[0] == 'var' or l[0][-1] == ':'):
        counter += 1
        if flag == 1 and l[0] == 'var':
            f2.write(f"Var statement used after instruction at line {counter}\n")
            l_result.append(1)
            #exit()
        l_result.append(check_space(l))
        if l[0]=="jmp" or l[0]=="jlt" or l[0]=="jgt" or l[0]=="je" :
            l_result.append(check_var_def(l[1]))
        elif l[0]=="ld" or l[0]=="st":
            l_result.append(check_var_def(l[2]))

        if l[0] == "mov":
            flag = 1
            l_result.append(check_mov(l))
        elif l[0] in O_A:
            flag = 1
            l_result.append(check_A(l))
        elif l[0] in O_B:
            flag = 1
            l_result.append(check_B(l))

        elif l[0] in O_C:
            flag = 1
            l_result.append(check_C(l))
        elif l[0] in O_D:
            flag = 1
            l_result.append(check_D(l))
        elif l[0] in O_E:
            flag = 1
            l_result.append(check_E(l))
        elif l[0] in O_F:
            flag = 1
            c_hlt += 1
            if c_hlt == 1:
                check_hlt_after = counter
                l_result.append(check_F(l))
            elif c_hlt > 1:
                l_result.append(1)
                f2.write("hlt operation used more than once\n")
                #exit()

    else:
        counter+=1
        f2.write(f"Incorrect operation at {counter}\n")
        l_result.append(1)    
    return l_result
    
def check_hlt():
    global f2
    if 'hlt' not in l_cmd:
        f2.write("hlt not used\n")
        a.append(1)
    
    elif 'hlt'!=l_cmd[-1]:
        f2.write("hlt not the last command\n")
        a.append(1)

file = "test.txt"
f = open(file, 'r')
f2=open('out.txt', 'w')

for line in f:
    var(line)
f.seek(0)
for line in f:
    a=error_controller(line)
check_hlt()
f2.close()

if 1 not in a:
    file_work()
f.close()


