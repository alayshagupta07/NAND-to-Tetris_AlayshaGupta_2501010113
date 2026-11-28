
// Nand2Tetris Capstone - Part C
// K = 13
// Starting row = 13
// Height = 20 rows
// Width = 32 pixels (2 words per row)

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE
    @CLEAR
    0;JMP

// DRAW BLACK BOX
(DRAW)
    @16800
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(DRAW_ROW)
    @2
    D=A
    @R15
    M=D

(DRAW_WORD)
    @R13
    A=M
    M=-1

    @R13
    M=M+1

    @R15
    MD=M-1
    @DRAW_WORD
    D;JGT

    @30
    D=A
    @R13
    M=D+M

    @R14
    MD=M-1
    @DRAW_ROW
    D;JGT

    @LOOP
    0;JMP

// CLEAR BOX
(CLEAR)
    @16800
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(CLEAR_ROW)
    @2
    D=A
    @R15
    M=D

(CLEAR_WORD)
    @R13
    A=M
    M=0

    @R13
    M=M+1

    @R15
    MD=M-1
    @CLEAR_WORD
    D;JGT

    @30
    D=A
    @R13
    M=D+M

    @R14
    MD=M-1
    @CLEAR_ROW
    D;JGT

    @LOOP
    0;JMP
