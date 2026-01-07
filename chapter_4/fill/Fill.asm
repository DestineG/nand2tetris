// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
// 初始化：让 address 指向屏幕开头
    @SCREEN
    D=A
    @addr
    M=D

(LOOP)
    // 1. 监听键盘
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE    // 如果 D != 0 (按键了)，跳到处理按键的逻辑

(KEY_RELEASED)
    // 键盘没按：就变白，且指针后退
    
    @addr
    A=M
    M=0      // 变白
    
    // 指针后退 (但不能小于 SCREEN)
    @addr
    D=M
    @SCREEN
    D=D-A
    @LOOP
    D;JEQ    // 如果已经在开头，不减了
    @addr
    M=M-1
    @LOOP
    0;JMP

(KEY_PRESSED)
    // 键盘按了：就变黑，且指针前进

    @addr
    A=M
    M=-1     // 变黑
    
    // 指针前进 (但不能超过 24575)
    @addr
    D=M
    @24575
    D=D-A
    @LOOP
    D;JEQ    // 如果已经在末尾，不加了
    @addr
    M=M+1
    @LOOP
    0;JMP