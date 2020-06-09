#!/usr/bin/python3

from CompExpGrammer import gram_comp_exp
from ExpList import gram_exp_list
from Lexer import lex
from Define import *

LineIndex = 0

def err_handler(msg):
    print("Error: Line:", LineIndex)
    print(msg)
    exit(1)

def strip_parent(lex):
    if lex[0].type == PARENT_L and lex[-1].type == PARENT_R:
        return lex[1:-1]
    else:
        err_handler("Error: parentheses not in pair!")
    return lex

def extract_exp_list(lex):
    balance = 0
    index = 0
    for item in lex:
        index += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return lex[index:]   

def extract_comp_exp(lex):
    balance = 0
    index = 0
    for item in lex:
        index += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return lex[:index] 

def gram_if_exp(if_lex):
    global LineIndex
    LineIndex = if_lex[0].line
    lex = if_lex[1:]
    exp = IfExp()
    exp.comp_exp = gram_comp_exp(strip_parent(extract_comp_exp(lex)))
    exp.exp_list = gram_exp_list(extract_exp_list(lex))
    #exp.print(0)
    return exp

def gram_else_exp(else_lex):
    global LineIndex
    LineIndex = else_lex[0].line
    exp = ElseExp()
    exp.exp_list = gram_exp_list(else_lex[1:])
    #exp.print(0)
    return exp

def gram_while_exp(while_lex):
    global LineIndex
    LineIndex = while_lex[0].line
    lex = while_lex[1:]
    exp = WhileExp()
    exp.comp_exp = gram_comp_exp(strip_parent(extract_comp_exp(lex)))
    exp.exp_list = gram_exp_list(extract_exp_list(lex))
    #exp.print(0)
    return exp

if __name__ == '__main__':
#    if_lex = lex("test_grammer_if.c")
#    gram_if_exp(if_lex)
    else_lex = lex("test_grammer_else.c")
    gram_else_exp(else_lex)
#    while_lex = lex("test_grammer_while.c")
#    gram_while_exp(while_lex)




