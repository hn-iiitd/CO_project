# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011",
     "R4": "100", "R5": "101", "R6": "110", "FLAG": "111"}
O_A = {"add": "00000", "sub": "00001", "mul": "00110",
       "xor": "01010", "or": "01011", "and": "01100"}
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


file = "file.txt"
f = open(file,'r')
out = open("out.txt",'w')
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
out.close()
