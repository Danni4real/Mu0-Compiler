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
    err_handler("Error: asign expression should begin with a symbol!")

def extract_math_exp(lex):
    return lex[2:]

def gram_asgn_exp(asgn_lex):
    global LineIndex
    LineIndex = asgn_lex[0].line
    lex = strip_semicolon(asgn_lex)
    exp = AsgnExp()
    exp.symbol = extract_symbol(lex)
    exp.math_exp = gram_math_exp(extract_math_exp(lex))
    #exp.print(0)
    return exp

if __name__ == '__main__':
    asgn_lex = lex("test_grammer_asgn.c")
    gram_asgn_exp(asgn_lex)
