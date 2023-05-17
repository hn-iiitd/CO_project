# This part checks the validation of the variables 
################################################
def check_variable_declaration_beginning(L1,f):#Kunal
    variable_number=1                                     #24 lines
    flag=0
    variables=[]
    D={}
    for i in range(0,len(L1)):#i is line number
        if flag==0:
            if L1[i][0]=='var':
                if len(L1[i])!=2:
                    f.write("invalid use of variable ")
                    exit()
                if L1[i][1] in variables:
                    f.write("same variable declared multiple times ")
                    exit()
                variables.append(L1[i][1])
                D[L1[i][1]]=variable_number+i
                variable_number=variable_number+1
            if L1[i][0]!='var':
                flag=1
        else:
            if L1[i][0]=='var':
                f.write("variable not declared in beginning")
                exit()
    D1={i:bin(D[i])[2:] for i in D.keys()}
    return variables,D1
######################################################
#******************************************************************************************************************************#
# This part of the code consists of the error handling 
######################################################
def check_label(L,f):#Harsh Rawat
    c=0#line numbers                                       #19 lines
    labels=[]
    D={}
    for i in L:
        if i[0]=='var':
            continue
        if i[0].count(":")==1:
            if i[0][:-1] not in labels:
                labels.append(i[0][:-1])
                D[c]=i[0][:-1]
            # else:
            #     print("error in line",c)
            #     raise SyntaxError("multiple definition for same label")
        if (i[0].count(":")>1):
            f.write("invalid label name")
            exit()
        c=c+1
    D_new={D[i]:bin(i)[2:] for i in D.keys()}
    return D_new,labels
##########################################################
##########################################################
def check_hlt(L,f):#Harsh Rawat                                      
    global is_error                                      #25 lines
    c=0
    l=[]
    for i in range(0,len(L)):
        if (":" not in L[i]):
            if (L[i].strip()=='hlt'):
                if (L[i]!=''):
                    l.append(L[i])
                    c=c+1
        else:
            l=[j for j in L[i].split(":")]
            for j in l:
                if (j.strip()=='hlt'):
                    c=c+1
    if (c>1):
        f.write("hlt used multiple times")
        exit()
    if (c==0):
        f.write("hlt not used")
        exit()
    if (l[-1].strip()=='hlt'):
        return None
    else:
        f.write("hlt not used as last instruction")
        exit()
#####################################################
#####################################################

def check_flags(L2,f):#Kunal
    for i in range(0,len(L2)):#i is line number                     #11 lines
        if 'flags' in L2[i]:
            if (L2[i][0]=='ld' and L2[i][1]=='FLAGS'):
                f.write("cannot load value to flags")
                exit()
            if ((L2[i][0]=='add') or(L2[i][0]=='sub') or(L2[i][0]=='mul') or(L2[i][0]=='div') and L2[i][1]=='FLAGS'):
                f.write("invalid operation on flag")
                exit()
            if L2[i][0]=='mov' and L2[i][1]!='FLAGS':
                f.write("invalid operation")
                exit()
#############################################################################
#dictionary for syntax
#########################################################################
#Kumar Mrinal
syntax={
    "00000":{"mnemonic":"add","num_registers":3,"other":0,"type":"A"},               #21 lines
    "00001":{"mnemonic":"sub" ,"num_registers":3,"other":0,"type":"A"},
    "00110":{"mnemonic":"mul" ,"num_registers":3,"other":0,"type":"A"},
    "00111":{"mnemonic":"div" ,"num_registers":3,"other":0,"type":"C"},
    "00010":{"mnemonic":"mov","num_registers":1,"other":0,"type":"B"},
    "00011":{"mnemonic":"mov","num_registers":2,"other":0,"type":"C"},
    "00100":{"mnemonic":"ld","num_registers":1,"other":"mem_addr","type":"D"},
    "00101":{"mnemonic":"st","num_registers":1,"other":"mem_addr","type":"D"},
    "01000":{"mnemonic":"rs","num_registers":1,"other":0,"type":"B"},#$ i/o is a 7 bit value
    "01001":{"mnemonic":"ls","num_registers":1,"other":0,"type":"B"},#$ i/o is a 7 bit value
    "01010":{"mnemonic":"xor","num_registers":3,"other":0,"type":"A"},
    "01011":{"mnemonic":"or","num_registers":3,"other":0,"type":"A"},
    "01100":{"mnemonic":"and","num_registers":3,"other":0,"type":"A"},
    "01101":{"mnemonic":"not","num_registers":3,"other":0,"type":"C"},
    "01110":{"mnemonic":"cmp","num_registers":2,"other":0,"type":"C"},
    "01111":{"mnemonic":"jmp","num_registers":0,"other":"mem_addr","type":"E"},
    "11100":{"mnemonic":"jlt","num_registers":0,"other":"mem_addr","type":"E"},
    "11101":{"mnemonic":"jgt","num_registers":0,"other":"mem_addr","type":"E"},
    "11111":{"mnemonic":"je","num_registers":0,"other":"mem_addr","type":"E"},
    "11010":{"mnemonic":"hlt","num_registers":0,"other":0,"type":"E"}
    }
########################################################################################
#dictionary to map registers with their code
###########################################################################################################
registers ={'R0':'000', 'R1':'001', 'R2':'010', 'R3':'011','R4':'100', 'R5':'101','R6':'110','FLAGS':'111'}#Harsh Vishwakarma

#list of mnemonics,flags
                                              #23 lines
mnemonics=["add","sub","mul","div","mov","ld","st","rs","ls","xor","or","and","not","cmp","jmp","jgt","je","hlt","jlt"]
flags={'V':0,'L':0,'G':0,'E':0}
is_error=False

# file opening instructions

with open('program.txt','w') as f:
    while True:
        try:
            k=input()
            f.write(k+'\n')
        except EOFError:
            break

    
with open('program.txt','r') as f:
    s=f.read()
    L=s.split('\n')
f_output=open("machine_code.txt","w+")#output file in same folder
check_hlt(L,f_output)
L1=[i.strip().split() for i in L if i!='']
for i in f_output:
    print(i)
# print(L1)
# print(L)

semantics=[(i,syntax[i]["mnemonic"])for i in syntax.keys()]
c=0# c is line number
variables,D=check_variable_declaration_beginning(L1,f_output)
D_labels,label=check_label(L1,f_output)
check_flags(L1,f_output)
##########################################################################################################
##########################################################################################################
for i in L1:#Kunal
    if L1.index(i)==len(L1)-2:
        c=c+1
    if i[0]=="var":                         #22 line
        continue
    if i[0] not in mnemonics and i[0][:-1] in label:
        i.pop(0)
    if (i[0]=="mov"):
        if ((i[2] in ['R0','R1','R2','R3','R4','R5','R6','FLAGS']) and (i[1] in  ['R0','R1','R2','R3','R4','R5','R6','FLAGS'])):
            s1="00011"+"0"*5+registers[i[1]]+registers[i[2]]
            #print(s1)
            f_output.write(s1+"\n")
            continue
        if ((i[1] not in  ['R0','R1','R2','R3','R4','R5','R6','FLAGS']) and (i[2] not in ['R0','R1','R2','R3','R4','R5','R6','FLAGS'])):
            s="line "+str(L1.index(i)-len(variables))
            f_output.write("invalid name of register"+s)
            exit()
    if i[0] in mnemonics:
        if (i[0]=="hlt"):
            s1="11010"+"0"*11
            #print(s1)
            f_output.write(s1+"\n")
            break
########################################################################################
########################################################################################
        #i[0]=syntax[i[0]]["mnemonic"]
        for j in range(0,len(semantics)):#Kumar Mrinal
            if (semantics[j][1]==i[0]):
                i[0]=semantics[j][0]
                break
        if (syntax[i[0]]["type"]=="A"):#type A
            # if ((registers[i[1]] in registers.keys()) and (registers[i[2]] in registers.keys()) and (registers[i[3]] in registers.keys())):
            try:
                s1=i[0]+"0"*2+registers[i[1]]+registers[i[2]]+registers[i[3]]
            except:
                f_output.write(f"invalid register name {L1.index(i)-len(variables)}")
                exit()
            # else:
            #     s="line "+str(L1.index(i)-len(variables))
            #     f_output.write("invalid register name "+s)
            #     exit()
        if (syntax[i[0]]["mnemonic"]=="mov"and i[2]  in variables):          #26 line
            v=bin(int(i[2][1:]))[2:]
            if (len(v)==7):
                s1="00010"+"0"+registers[i[1]]+v
            elif (len(v)<7):
                v="0"*(7-len(v))+v
                s1="00010"+"0"+registers[i[1]]+v
            else:
                s="line no. "+str(L1.index(i)-len(variables))
                f_output.write("cannot take input more than 7 bits"+s)
                exit()
###########################################################################################
###########################################################################################
        if (syntax[i[0]]["mnemonic"]=="mov"and i[2] in ['R0','R1','R2','R3','R4','R5','R6','flag']):#Harsh Vishwakarma
            s1="00011"+"0"*5+registers[i[1]]+registers[i[2]]
        if (syntax[i[0]]["type"]=="B"):
            v=bin(int(i[2][1:]))[2:]
            if (len(v)==7):
                s1=i[0]+"0"+registers[i[1]]+v                               #35 line
            elif (len(v)<7):
                v="0"*(7-len(v))+v
                s1=i[0]+"0"+registers[i[1]]+v
            else:
                s="line no. "+str(L1.index(i)-len(variables))
                f_output.write("cannot take input more than 7 bits"+s)
                exit()
        if (syntax[i[0]]["type"]=="C"):
            if (((i[1]) in registers) and (i[2] in registers)):
                s1=i[0]+"0"*5+registers[i[1]]+registers[i[2]]
            else:
                s="line "+str(L1.index(i)-len(variables))
                f_output.write("invalid registers "+s)
                exit()
        if (syntax[i[0]]["type"]=="D"):
            if i[2] not in variables:
                s="line "+str(L1.index(i)-len(variables))
                f_output.write("undeclared variable"+s)
                exit()
            else:
                reg=i[1]
                if reg in registers:
                    if len(D[i[2]])==7:
                        s1=i[0]+"0"+registers[i[1]]+D[i[2]]
                    else:
                        s1=i[0]+"0"+registers[i[1]]+"0"*(7-len(D[i[2]]))+D[i[2]]
                else:
                    s="line "+str(L1.index(i)-len(variables))
                    f_output.write("invalid registers "+s)
                    exit()
##################################################################################
        if (syntax[i[0]]["type"]=="E"):#Harsh Rawat
            if (i[1] not in D_labels):
                s="line "+str(L1.index(i)-len(variables))
                f_output.write("undeclared label "+s)
                exit()
            if (len(D_labels[i[1]])==7):
                s1=i[0]+"0"*4+D_labels[i[1]]                  #16 line
            else:
                s1=i[0]+"0"*4+"0"*(7-len(D_labels[i[1]]))+D_labels[i[1]]
        if (syntax[i[0]]["type"]=="F"):
            s1=i[0]+"0"*11
        f_output.write(s1+"\n")
        c=c+1
    else:
        s="line "+str(L1.index(i)-len(variables))
        f_output.write("typo in instruction "+s)
        exit()