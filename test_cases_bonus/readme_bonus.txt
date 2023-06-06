Bonus part implementation.
OPCODE      INSTRUCTION     SEMANTICS                             SYNTAX          TYPE
10111       addition       R1 = R1 + $10 (adds imm to reg.        addi R1 $imm     B
10100       nop            does nothing                           nop               F
10011       reset         values of all registers = 0             reset             F
10101       inc           inc R1 , increments R1 by 1             inc R1            new
10110       dec           dec R1, decrements R1 by 1              dec R1            new
