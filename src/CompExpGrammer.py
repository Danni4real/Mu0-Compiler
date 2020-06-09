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

def extract_opt(lex):
    balance = 0
    for item in lex:
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if item.type in COMP_OPT and balance == 0:
            return item.type
    err_handler("Error: as a compare expression doesn't have a compare operation sign!")

def extract_math_exp_l(lex):
    balance = 0
    count = 0
    for item in lex:
        count += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return lex[:count]

def extract_math_exp_r(lex):
    balance = 0
    count = 0
    for item in lex:
        count += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return extract_math_exp_l(lex[count+1:])

def gram_comp_exp(comp_lex):
    global LineIndex
    LineIndex = comp_lex[0].line
    lex = strip_semicolon(comp_lex)
    exp = CompExp()
    exp.opt = extract_opt(lex)
    exp.math_exp_l = gram_math_exp(extract_math_exp_l(lex))
    exp.math_exp_r = gram_math_exp(extract_math_exp_r(lex))
    #exp.print(0)
    return exp

if __name__ == '__main__':
    comp_lex = lex("test_grammer_comp.c")
    gram_comp_exp(comp_lex)
