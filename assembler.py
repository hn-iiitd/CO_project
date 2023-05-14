# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011",
     "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
O_A = {"add": "00000", "sub": "00001", "mul": "00110",
       "xor": "01010", "or": "01011", "and": "01100"}#0010101100000101
O_B = {"mov": "00010", "rs": "01000", "ls": "01001"}
O_C = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}
O_D = {"ld": "00100", "st": "00101"}
O_E = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
O_F = {"hlt": "11010"}
O = ["add","sub","mul","xor","or","and","mov","rs","ls","div","not","cmp","ld","st","jmp","jlt","jgt","je","hlt","FLAG"]
variables = {}
def add(r1, r2):
    sum = bin(int(r1) + int(r2))
    return sum[2:]
vl = []
def convert_OA(a):
    if(a in O_A.keys()):
        x = O_A[a] + "00" #Unused BITS
        return x
    if(a in R):
        return R[a]
def convert_OB(a):
    if(a in O_B.keys()):
        x = O_B[a] + "0" #Unused BITS
        return x
    if(a in R):
        return R[a]
    else:
        a = a.replace("\n","")
        a = a.replace("$","")
        num= str(bin(int(a)))
        left_over=9-len(num)
        x = '0'*left_over+num[2:]
        return x
def convert_OC(a):
    if(a in O_C.keys()):
        x = O_C[a] + '00000'
        return x
    else:
        return R[a]
def convert_OD(a):
    if(a in O_D.keys()):
        x=O_D[a]
        return x + '0'
    elif(a in R):
        x=R[a]
        return x;      
    else:
        return variables[a]



def file_work():
    file = "test.txt"
    f = open(file,'r')
    out = open("out.txt",'w+')
    for line in f:
        line = line.strip()
        l = line.split(" ")
        if l[0] == "var":
            l[1] = l[1].replace("\n","")
            if(len(variables.keys()) == 0):
                variables[l[1]] = "0000001"
                vl.append(variables[l[1]])

            else:
                variables[l[1]] = add(vl[len(vl)-1],1)
                variables[l[1]] = "0"*(7-len(variables[l[1]])) + variables[l[1]]
                vl.append(variables[l[1]])
        if l[0] in O_A.keys():
            out.write(convert_OA(l[0]))
            out.write(convert_OA(l[1]))
            out.write(convert_OA(l[2]))
            l[3] = l[3].replace("\n","")
            out.write(convert_OA(l[3]))
            out.write("\n")
        elif l[0] in O_B.keys() and l[2][0] == '$'  :
            out.write(convert_OB(l[0]))
            out.write(convert_OB(l[1]))
            out.write(convert_OB(l[2]))
            out.write("\n")
        elif l[0] in O_C.keys() :
            out.write(convert_OC(l[0]))
            out.write(convert_OC(l[1]))
            l[2] = l[2].replace("\n","")
            out.write(convert_OC(l[2]))
            out.write("\n")
        elif l[0] in O_D.keys():
            # print(l)
            # print(variables)
            # print(vl)
            out.write(convert_OD(l[0]))
            out.write(convert_OD(l[1]))
            l[2] = l[2].replace("\n","")
            out.write(convert_OD(l[2]))
            out.write("\n")
        elif l[0] in O_E.keys():
            out.write(O_E[l[0]] + "0"*4)
            l[1] = l[1].replace("\n","")
            out.write(variables[l[1]])
            out.write("\n")
        elif l[0] in O_F.keys():
            out.write(O_F[l[0]] + "0" *11)
        else:
            pass
    f.close()
    # print("yoyo")
    out.seek(0)
    for i in out:
        if i[-1]=='\n':
            print(i[:-1])
        else:
            print(i)
    out.close()


l_result=[]


def check_space(k):
    if '' in k:
        print("Error: space")
        exit()

def check_A(k):
    if len(k)!=4:
        print("Wrong instruction for TYPE A register")
        exit()

    if (k[1] not in R or k[2] not in R or k[3] not in R):
        print("Wrong register name")
        exit()
        
    if k[1]=="FLAGS" or k[2]=="FLAGS" or k[3]=="FLAGS":
        print("Wrong use of flags")
        exit()
    

def check_mov(k):
    if k[-1][0]=='$':
        if len(k)!=3:
            print("Wrong instruction in TYPE B registers")
            exit()
            
        if k[1]=="FLAGS" or k[2]=="FLAGS":
            print("Wrong use of flags")
            exit()
            
        if k[1] not in R:
            print("Wrong register")
            exit()
            
    else:
        if len(k)!=3:
            print("Wrong instruction in TYPE C registers")
            exit()
            
        if k[1]=="FLAGS":
            print("Wrong use of flags")
            exit()
            
        if k[1] not in R or k[2] not in R:
            print("Wrong register")
            exit()
            
    
        
def check_B(k):
    if len(k)!=3:
        print("Wrong instruction for TYPE B register")
        exit()
        
    if (k[1] not in R or k[2] not in R or k[3] not in R):
        print("Wrong register name")
        exit()
        
    if k[1]=="FLAGS":
        print("Wrong use of flags")
        exit()
         
    

def check_C(k):
    if len(k)!=3:
        print("Wrong instruction for TYPE C register")
        exit()
        
    if k[1]=="FLAGS" or k[2]=="FLAGS":
        print("Wrong use of flags")
        exit()
        
    if k[1] not in R or k[2] not in R:
        print("Wrong register names")
        exit()
        
    

def check_D(k):
    if len(k)!=3:
        print("Wrong instruction for TYPE D register")
        exit()
        
    if k[1]=="FLAGS":
        print("Wrong use of flags")
        exit()
        
    if k[1] not in R:
        print("Wrong register names")
        exit()
        
    

def check_E(k):
    if len(k)!=2:
        print("Wrong instruction for TYPE E register")
        exit()
        
    
def check_F(k):
    
    if (len(k) != 1):
            print("Wrong instruction for TYPE F register")
            exit()
            
    
c_hlt=0
def error_controller(k):
    global c_hlt
    if k[-1]=='\n':
        k=k[:-1]
    l=k.strip().split(" ")
    if l==['']:
        return
    if (l[0] in O or l[0]=='var' or l[0][-1]==':'):
        (check_space(l))
        
        if l[0]=="mov":
            (check_mov(l))
        elif l[0] in O_A:
            (check_A(l))
        elif l[0] in O_B:
            (check_B(l))
        elif l[0] in O_C:
            (check_C(l))
        elif l[0] in O_D:
            (check_D(l))
        elif l[0] in O_E:
            (check_E(l))
        elif l[0] in O_F:
            c_hlt+=1
            if c_hlt==1:
                (check_F(l))
            elif c_hlt>1:
                print("hlt operation used more than once")
                exit()
    else:
        print("Incorrect operation")
        (1)
    return l_result

file = "test.txt"
f = open(file,'r')
# out = open("out.txt",'w+')
for line in f:
    error_controller(line)
file_work()
f.close()
# f.seek(0)

