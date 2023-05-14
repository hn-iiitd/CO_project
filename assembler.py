# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011",
     "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
O_A = {"add": "00000", "sub": "00001", "mul": "00110",
       "xor": "01010", "or": "01011", "and": "01100"}
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
            print(i)
    out.close()


l_result = []


def check_space(k):
    global counter
    if '' in k:
        print(f"Error: Extra space in line {counter}")
        exit()


def check_A(k):
    global counter
    if len(k) != 4:
        print(f"Error: Wrong instruction syntax for TYPE A register in line {counter}")
        exit()

    if (k[1] not in R or k[2] not in R or k[3] not in R):
        print(f"Error: Incorrect Register name in line {counter}")
        exit()

    if k[1] == "FLAGS" or k[2] == "FLAGS" or k[3] == "FLAGS":
        print(f"Incorrect use of FLAGS register in line {counter}")
        exit()


def check_mov(k):
    global counter
    if k[-1][0] == '$':
        if len(k) != 3:
            print(f"Error: Wrong instruction syntax for TYPE B register in line {counter}")
            exit()

        if k[1] == "FLAGS" or k[2] == "FLAGS":
            print(f"Incorrect use of FLAGS register in line {counter}")
            exit()

        if k[1] not in R:
            print(f"Error: Incorrect Register name in line {counter}")
            exit()

    else:
        if len(k) != 3:
            print(f"Error: Wrong instruction syntax for TYPE C register in line {counter}")
            exit()

        if k[1] == "FLAGS":
            print(f"Incorrect use of FLAGS register in line {counter}")
            exit()

        if k[1] not in R or k[2] not in R:
            print(f"Error: Incorrect Register name in line {counter}")
            exit()


def check_B(k):
    global counter
    if len(k) != 3:
        print(f"Error: Wrong instruction syntax for TYPE B register in line {counter}")
        exit()

    if (k[1] not in R or k[2] not in R or k[3] not in R):
        print(f"Error: Incorrect Register name in line {counter}")
        exit()

    if k[1] == "FLAGS":
        print(f"Incorrect use of FLAGS register in line {counter}")
        exit()


def check_C(k):
    global counter
    if len(k) != 3:
        print(f"Error: Wrong instruction syntax for TYPE C register in line {counter}")
        exit()

    if k[1] == "FLAGS" or k[2] == "FLAGS":
        print(f"Incorrect use of FLAGS register in line {counter}")
        exit()

    if k[1] not in R or k[2] not in R:
        print(f"Error: Incorrect Register name in line {counter}")
        exit()


def check_D(k):
    global counter
    if len(k) != 3:
        print(f"Error: Wrong instruction syntax for TYPE D register in line {counter}")
        exit()

    if k[1] == "FLAGS":
        print(f"Incorrect use of FLAGS register in line {counter}")
        exit()

    if k[1] not in R:
        print(f"Error: Incorrect Register name in line {counter}")
        exit()


def check_E(k):
    global counter
    if len(k) != 2:

        print(f"Error: Wrong instruction syntax for TYPE E register in line {counter}")
        exit()


def check_F(k):
    global counter
    if (len(k) != 1):

        print(f"Error: Wrong instruction syntax for TYPE F register in line {counter}")
        exit()


c_hlt = 0
counter = 0
flag = 0
check_hlt_after=0


def error_controller(k):
    global c_hlt
    global counter
    global flag
    global check_hlt_after
    if k[-1] == '\n':
        k = k[:-1]
    l = k.strip().split(" ")
    if l == ['']:
        return
    if (l[0] in O or l[0] == 'var' or l[0][-1] == ':'):

        counter += 1
        if flag == 1 and l[0] == 'var':
            print(f"Var statement used after instruction at line {counter}")
            exit()
        (check_space(l))

        if l[0] == "mov":
            flag = 1
            (check_mov(l))
        elif l[0] in O_A:
            flag = 1
            (check_A(l))
        elif l[0] in O_B:
            flag = 1
            (check_B(l))

        elif l[0] in O_C:
            flag = 1
            (check_C(l))
        elif l[0] in O_D:
            flag = 1
            (check_D(l))
        elif l[0] in O_E:
            flag = 1
            (check_E(l))
        elif l[0] in O_F:
            flag = 1
            c_hlt += 1
            if c_hlt == 1:
                check_hlt_after=counter
                (check_F(l))
            elif c_hlt > 1:
                print("hlt operation used more than once")
                exit()
    else:
        print("Incorrect operation")
print("d")


file = "test.txt"
f = open(file, 'r')

for line in f:
    error_controller(line)
file_work()
f.close()
