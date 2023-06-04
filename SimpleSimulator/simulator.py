import os
O_A = {"add": "00000", "sub": "00001", "mul": "00110", "xor": "01010","or": "01011", "and": "01100"}    # Labelling operations in A
O_B = {"movB": "00010", "rs": "01000", "ls": "01001"}                                                    # Labelling operations in B
O_C = {"movC": "00011", "div": "00111", "not": "01101", "cmp": "01110"}                                  # Labelling operations in C
O_D = {"ld": "00100", "st": "00101"}                                                                    # Labelling operations in D
O_E = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}                                   # Labelling operations in E
O_F = {"hlt": "11010"}                                                                                  # Labelling operations in F
O = {"add", "sub", "mul", "xor", "or", "and", "mov", "rs", "ls", "div","not", "cmp", "ld", "st", "jmp", "jlt", "jgt", "je", "hlt", "FLAG"}
O_check = { "11010":"hlt","01111":"jmp",  "11100":"jlt",  "11101":"jgt",  "11111":"je", "00100":"ld" ,  "00101":"st","00011":"movC",  "00111":"div",  "01101":"not", "01110" :"cmp","00010":"movB", "01000":"rs",  "01001":"ls","00000":"add",  "00001":"sub", "00110":"mul" , "01010":"xor","01011":"or" , "01100":"and" }    # Labelling operations in A
final = {}
def find_from_dict(val,dict):
    for i in dict.keys():
        if(dict[i] == val ):
            return i
        else:
            continue
    return 0
R = {'R0' : '0'*16,
'R1' : '0'*16 , 
'R2' : '0'*16 ,
'R3' : '0'*16,
'R4' : '0'*16,
'R5' : '0'*16,
'R6' : '0'*16,
'FLAGS' : '0'*16}
Reg = {'000' : 'R0',
'001' : 'R1' , 
'010' : 'R2' ,
'011' : 'R3',
'100' : 'R4',
'101' : 'R5',
'110' : 'R6',
'111' : 'FLAGS'
}
# print(Reg['111'])
var= {} #st and ld
Flags = {
    'V':0 ,'L':0, 'G':0, 'E':0
}
flags_to_display = {
    'V':0 ,'L':0, 'G':0, 'E':0
}
k={}
pc_jmp = []
#functions for add,sub,moveR,moveI,mul,div,etc

def add(r1, r2):
    sum = int(r1,2) + int(r2,2) 
    return sum


def sub(r1, r2):
    sum = (int(r1,2) - int(r2,2))
    return sum
def mul(r1, r2):
    sum = (int(r1,2)*int(r2,2))
    return sum
def div(r1, r2):
    rem = '{0:016b}'.format(int(int(r1,2)%int(r2,2)))
    quo = '{0:016b}'.format(int(int(r1,2)/int(r2,2)))
    return rem,quo
def xor(r1, r2):
    r1 = str(r1)
    r2 = str(r2)
    r3 = []
    for i in range(min(len(r1), len(r2))):
        s = int(r1[i]) + int(r2[i])
        if (s == 2 or s == 0):
            r3.append(str(0))
        elif (s == 1):
            r3.append(str(1))
    r3 = "".join(r3)
    return r3
def orr(r1,r2):
    r1 =str(r1)    
    r2 =str(r2)  
    r3 = []
    r4 = ""
    for i in range(min(len(r1),len(r2))):
        s = int(r1[i]) + int(r2[i])
        if(s==2 or s==1):
            r3.append(str(1))
        elif(s==0):
            r3.append(str(0))
    r3 = "".join(r3)
    return r3
def reset_flags(Flags):
    Flags['V'] = 0
    Flags['E'] = 0
    Flags['G'] = 0
    Flags['L'] = 0
def andd(r1,r2):
    r1 =str(r1)    
    r2 =str(r2)  
    r3 = []
    r4 = ""
    for i in range(min(len(r1),len(r2))):
        s = int(r1[i]) + int(r2[i])
        if(s==2):
            r3.append(str(1))
        elif(s==0 or s==1):
            r3.append(str(0))
    r3 = "".join(r3)
    return r3

file_in = "input.txt" #input file change it to stdin
file_out = "out.txt"
f=open(file_in,'w')
while True:
    try:
        a=input()
        f.write(a+'\n')
    except EOFError:
        break
f.close()
f = open(file_in,'r')
i=0
for line in f:
    line = line.replace("\n", "")
    k[i]=line
    i+=1
f.close()
# print(k)
m = i-1 #total no. of instructions in dict
j = 0  #pc
w = 0  #writer count
while(j<i):
    c = O_check[k[j][0:5]]
    # print(c,k[j][0:5],sep='        ')
    if c in O_A :            
        if c=='add':
            if add(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]]) >=2^16 :
                flags_to_display['V'] = 1
                Flags['V'] = 1
                R[Reg[k[j][7:10]]] = '0'*16
            else:
                R[Reg[k[j][7:10]]] = str('{0:016b}'.format(add(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])))
        R[Reg["111"]] = 12*'0' + str(Flags['V']) + str(Flags['L']) + str(Flags["G"]) + str(Flags['E']);
        if c=='sub':
            if int(R[Reg[k[j][10:13]]],2)<int(R[Reg[k[j][13:16]]],2) :
                flags_to_display['V'] = 1
                Flags['V'] = 1
                R[Reg[k[j][7:10]]] = '0'*16
            else:
                R[Reg[k[j][7:10]]] = str('{0:016b}'.format(sub(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])))
        if c=='mul':
            if mul(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]]) >=2**16 -1:
                flags_to_display['V'] = 1
                Flags['V'] = 1
                R[Reg[k[j][7:10]]] = '0'*16
            else:
                R[Reg[k[j][7:10]]] = str('{0:016b}'.format(mul(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])))
        R[Reg["111"]] = 12*'0' + str(Flags['V']) + str(Flags['L']) + str(Flags["G"]) + str(Flags['E']);

        if c=='xor':
            R[Reg[k[j][7:10]]]= xor(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])
            reset_flags(Flags)
            reset_flags(flags_to_display)
        if c=='or':
            R[Reg[k[j][7:10]] ]= orr(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])
            reset_flags(Flags)
            reset_flags(flags_to_display)

        if c=='and':
            R[Reg[k[j][7:10]]] = andd(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])
            reset_flags(Flags)
            reset_flags(flags_to_display)


    elif c in O_B:
        if c == 'movB':# and k[j][0:5] == '00010':
            R[Reg[k[j][6:9]]] = str('{0:016b}'.format(int(str([k[j][9:16]][0]),2)))
        if c == 'rs':
            R[Reg[k[j][6:9]]] = str('{0:016b}'.format(int(R[Reg[k[j][6:9]]],2)>>int([k[j][9:16]],2)))
        if c == 'ls':
            R[Reg[k[j][6:9]]] = str('{0:016b}'.format(int(R[Reg[k[j][6:9]]],2)<<int([k[j][9:16]],2)))
        reset_flags(Flags)
        reset_flags(flags_to_display)

    elif c in O_C:
        if c=='movC':
            R[Reg[k[j][10:13]]] = str('{0:016b}'.format(int(R[Reg[k[j][13:16]]],2)))
        
            reset_flags(Flags)
            reset_flags(flags_to_display)

       
        if c == 'div':
            if(int(R[Reg[k[j][13:16]]],2)==0):
                flags_to_display['V'] = 1
                Flags['V'] = 1
                R['R1'] = '0'*16
                R['R0'] = '0'*16
            else:
                R['R1'] , R['R0'] = div(R[Reg[k[j][10:13]]],R[Reg[k[j][13:16]]])
        R[Reg["111"]] = 12*'0' + str(Flags['V']) + str(Flags['L']) + str(Flags["G"]) + str(Flags['E']);

        if c== 'not':
            R[Reg[k[j][10:13]]] = str('{0:016b}'.format(~int(R[Reg[[k[j][13:16]]]],2)))
            reset_flags(Flags)
            reset_flags(flags_to_display)

        if c== 'cmp':
            
            if(int(R[Reg[k[j][10:13]]],2) < int(R[Reg[k[j][13:16]]],2)):
                flags_to_display['L'] = 1;
                Flags["L"] = 1
            elif(int(R[Reg[k[j][13:16]]],2) == int(R[Reg[k[j][10:13]]],2)):
                flags_to_display['E'] = 1;
                Flags["E"] = 1
            elif(int(R[Reg[k[j][10:13]]],2) > int(R[Reg[k[j][13:16]]],2)):
                flags_to_display['G'] = 1;
                Flags["G"] = 1
            R[Reg["111"]] = 12*'0' +str(Flags['V']) + str(Flags['L']) + str(Flags["G"]) + str(Flags['E']);

    elif c in O_D:
        if c=='ld' and k[j][0:5] == '00100':
            if(k[j][9:16] not in var.keys()):
                var[k[j][9:16]] = '0'*16
            R[Reg[k[j][6:9]]] = var[k[j][9:16]]
        elif c=='st' and k[j][0:5]=='00101':
            var[k[j][9:16]] = R[Reg[k[j][6:9]]]
        reset_flags(Flags)
        reset_flags(flags_to_display)

    elif c in O_E:
        if c=='jmp':
            pc_update = int(k[j][9:16],2)
            pc_jmp.append(pc_update)
        
        elif c=='jlt' and  Flags['L']==1:
            flags_to_display['L'] = 1
            pc_update = int(k[j][9:16],2)
            pc_jmp.append(pc_update)
        elif c=='jgt' and  Flags['G']==1:
            flags_to_display['G'] = 1
            pc_update = int(k[j][9:16],2)
            pc_jmp.append(pc_update)


        elif c=='je' and  Flags['E']==1:
            flags_to_display['E']=1
            pc_update = int(k[j][9:16],2) 
            pc_jmp.append(pc_update)
        reset_flags(flags_to_display)
        reset_flags(Flags)

    elif c in O_F:
        
        final[w] = str('{0:07b}'.format(j))+7*" " + " " + R["R0"]+ " " +R["R1"]+" " +R["R2"]+ " " +R["R3"]+" " +R["R4"]+" " +R["R5"] + " " +R["R6"] + ' ' + '0'*12 + str(flags_to_display['V']) + str(flags_to_display['L']) + str(flags_to_display["G"]) + str(flags_to_display['E'])
        break        
    final[w] = str('{0:07b}'.format(j)) + 7*" " + " " + R["R0"]+ " " +R["R1"]+" " +R["R2"]+ " " +R["R3"]+" " +R["R4"]+" " +R["R5"] + " " +R["R6"]+ ' ' + '0'*12 + str(flags_to_display['V']) +str(flags_to_display['L']) + str(flags_to_display["G"]) + str(flags_to_display['E'])
    if(len(pc_jmp)!=0):
        j = pc_jmp.pop()
        
        w+=1
    else:
        j+=1
        w+=1
count = 0
o = open(file_out,'w+')
for i in final:
    o.write(final[i])
    o.write('\n')
for i in k:
    o.write(k[i])
    o.write("\n")
for i in var:
    o.write(var[i])
    count+=1
    o.write("\n")
for i in range(127-m-count):
    o.write(16*"0")
    o.write("\n")
o.seek(0)
for i in o:
    print(i)
o.close()
os.remove(file_in)
os.remove(file_out)