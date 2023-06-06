<pre>
This is the CO project work done in python language.

assembler.py is the main assembler file.
simulator.py is the main simulator file.
--------------------------------------------------------------------------------------------------------------
To run the automated testing , follow the steps:-
clone the repository using     git clone https://github.com/hn-iiitd/CO_project     command.

Step1] - go to automatedTesting folder and open it in terminal
Step2] - type  ./run   command in the terminal, it will show the test results.
If the Terminal says "Permission Denied" error , 
then go to automatedTesting folder -> right click on "run" -> click on "Properties" -> Permissions -> check box "Allow as executing File", 
do the same in Simple Assembler Folder and Simple Simulator too. Now it will work fine. This error is due to "run" file permissions.
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

Individual Contributions for assembler:-
Roll No.     Name                       Contributions
2022190    Guneet Pal Singh       Error Handling, code for conversion of Type- B to Binary and implemented bonus part for assembler.
2022199    Harsh Nangia           Error Handling , code for conversion of Type- A to Binary
2022220    Idhant Arora           Conversion of Type C and E to Binary
2022280    Manveet Singh          Conversion of Type D and F to Binary

Individual Contributions for Simulatorr:-
Roll No.     Name                       Contributions
2022190    Guneet Pal Singh       simulation of Type_B , Floating point.
2022199    Harsh Nangia           simulation of Type- A , Bonus part of simulator , floating point.
2022220    Idhant Arora           simulation of Type C and E, floating point.
2022280    Manveet Singh          simulation of Type D and F,floating point.
---------------------------------------------------------------------------------------------------------------
Bonus part implementation.
OPCODE      INSTRUCTION     SEMANTICS                             SYNTAX          TYPE
10111       addition       R1 = R1 + $10 (adds imm to reg.        addi R1 $imm     B
10100       nop            does nothing                           nop               F
10011       reset         values of all registers = 0             reset             F
10101       inc           inc R1 , increments R1 by 1             inc R1            new
10110       dec           dec R1, decrements R1 by 1              dec R1            new
<pre/>
