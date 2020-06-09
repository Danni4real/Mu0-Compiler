# Mu0-Compiler
Compiler for mu0 cpu, implemented using python

Implement a simplified C language, features as below:

    1. only have "int" data type, which has 2 bytes;
    
    2. only support "+" and "-" arithmetic operators;
    
    3. only support "=" assignment operator;
    
    4. only support "if" and "else" decision making operators;
    
    5. only support "while" loop control;
    
    6. a declare expression must be initialed by a digital number;
    
    7. right part of a assignment expression can't have more than 2 symbols;
    
    8. a compare expression can't have more than 2 symbols;
    
    9. only declare expression can have digital number;
    
    
Output of compiler is a assemble source file, which can be processed to binary file using Mu0-Assembler.

Usage: ./Translate test.c out.asm
