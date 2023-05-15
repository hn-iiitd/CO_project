# Dictionaries for all types of instructions.
R = {'R0': "000", 'R1': "001", 'R2': "010", "R3": "011", "R4": "100",
     "R5": "101", "R6": "110", "FLAGS": "111"}  # Register numbers
O_A = {"add": "00000", "sub": "00001", "mul": "00110", "xor": "01010",
       "or": "01011", "and": "01100"}    # Labelling operations
O_B = {"mov": "00010", "rs": "01000", "ls": "01001"}
O_C = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}
O_D = {"ld": "00100", "st": "00101"}
O_E = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
O_F = {"hlt": "11010"}
O = ["add", "sub", "mul", "xor", "or", "and", "mov", "rs", "ls", "div",
     "not", "cmp", "ld", "st", "jmp", "jlt", "jgt", "je", "hlt", "FLAG"]
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

# Reading instructions from file and giving machine code in the output file
def file_work():
    file = "input_file.txt"
    f = open(file, 'r')
    out = open("output_file.txt", 'w+')
    for line in f:
        line = line.strip()
        # line = line.strip()
        k = line.split(":")
        if (len(k) > 1):
            line = k[1]
            line = line.strip()
        # l = line.split(" ")
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

    # return 0

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
        l_errors.append(
            f"Error in Line {counter}: {k[0]} must contain 2 parameters")

    else:
        if k[1] == "FLAGS" or k[2] == "FLAGS":
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
            l_errors.append(
                f"Error in Line {counter}: Register is not defined")

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

        f2.write(
            f"Error in Line {counter}: {k[0]} must contain 1 parameters\n")

        return 1
    return 0

# Check for errors in TYPE F statements
def check_F(k):
    global counter, f2
    if (len(k) != 1):

        f2.write(
            f"Error in Line {counter}: {k[0]} must contain no parameters\n")

        return 1
    return 0

def var(k):
    if k[-1] == '\n':
        k = k[:-1]

    l = k.strip().split(" ")
    l_cmd.append(l[0])
    if l == ['']:
        return
    if (l[0] in O or l[0] == 'var' or l[0][-1] == ':'):

        if l[0] == 'var':
            l_var_def.append(l[1])
        elif l[0][-1] == ':':
            l_var_def.append(l[0][:-1])

def check_var_def(k):
    global counter, f2
    if k[0] == "jmp" or k[0] == "jlt" or k[0] == "jgt" or k[0] == "je":

        if k[1] not in l_var_def:

            f2.write(
                f"Error on line {counter}:No Label/variable name {k[1]}\n")
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
    l = k.strip().split(" ")
    l_cmd.append(l[0])
    if l == ['']:
        return
    # print(l[0])
    if (l[0] in O or l[0] == 'var' or l[0][-1] == ':'):
        counter += 1
        if flag == 1 and l[0] == 'var':
            f2.write(
                f"Error in Line {counter}: Variables must be declared at the very beginning\n")
            l_result.append(1)

        l_result.append(check_space(l))
        if l[0] == "jmp" or l[0] == "jlt" or l[0] == "jgt" or l[0] == "je":
            l_result.append(check_var_def(l))
        elif l[0] == "ld" or l[0] == "st":
            l_result.append(check_var_def(l))

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
        exit()
        a.append(1)


file = "input_file.txt"
f = open(file, 'r')
f2 = open('output_file.txt', 'w')

# To make a list of all variables , labels and memory addresses
for line in f:
    var(line)

f.seek(0)
print(l_var_def)
# for error checking
for line in f:
    u = line.split(":")
    if (len(u) > 1):
        # print(u)
        line=u[1].strip()
    # print(line)
    a = error_controller(line)
check_hlt()
f2.close()

# will run this if there is no error
if 1 not in a:
    file_work()

f.close()
