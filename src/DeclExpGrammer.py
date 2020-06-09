#!/usr/bin/python3

from MathExpGrammer import strip_semicolon
from MathExpGrammer import gram_math_exp
from Lexer import lex
from Define import *

LineIndex = 0



def err_handler(msg):
    print("Error: Line:", LineIndex)
    print(msg)
    exit(1)

def extract_symbol(lex):
    if lex[0].type == SYMBOL:
        return lex[0].name
    err_handler("Error: declare expression should have a symbol!")

def extract_math_exp(lex):
    return lex[2:]

def gram_decl_exp(decl_lex):
    global LineIndex
    LineIndex = decl_lex[0].line
    lex = strip_semicolon(decl_lex)[1:]
    exp = DeclExp()
    exp.symbol = extract_symbol(lex)
    exp.math_exp = gram_math_exp(extract_math_exp(lex))
    #exp.print(0)
    return exp

if __name__ == '__main__':
    decl_lex = lex("test_grammer_decl.c")
    gram_decl_exp(decl_lex)
