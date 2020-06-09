#!/usr/bin/python3

from Lexer import lex
from Define import *

LineIndex = 0

MathExpList = []


def err_handler(msg):
    print("Error: Line:", LineIndex)
    print(msg)
    exit(1)

def strip_semicolon(lex):
    if lex[-1].type == SEMI_COLON:
        return lex[:-1]
    return lex

def strip_parent(lex):
    if lex[0].type == PARENT_L and lex[-1].type == PARENT_R:
        return lex[1:-1]
    elif lex[0].type == PARENT_L:
        balance = 0
        for item in lex:
            if item.type == PARENT_L:
                balance += 1
            if item.type == PARENT_R:
                balance -= 1
        if balance == 0:
            return lex
        else:
            err_handler("Error: parentheses not in pair!")
    elif lex[-1].type == PARENT_R:
        err_handler("Error: parentheses not in pair!")
    return lex

def isLeaf(lex):
    if len(lex) == 1:
        if lex[0].type == SYMBOL or lex[0].type == DIGIT:
            return True
        err_handler("Error: math expression leaf must be symbol or digit!")
    return False

def extract_opt(lex):
    balance = 0
    for item in lex:
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if item.type in MATH_OPT and balance == 0:
            return item.type
    err_handler("Error: lack math operation symbol in this math expression!")    
   
def extract_left_leaf(lex): 
    balance = 0
    count = 0
    if len(lex) == 0:
        err_handler("Error: math grammer error")
    if lex[0].type != PARENT_L and lex[0].type != SYMBOL and lex[0].type != DIGIT:
        err_handler("Error: math expression must starts with ( or symbol or digit!")
    for item in lex:
        count += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return lex[:count]    

def extract_right_leaf(lex): 
    balance = 0
    count = 0
    for item in lex:
        count += 1
        if item.type == PARENT_L:
            balance += 1
        if item.type == PARENT_R:
            balance -= 1
        if balance == 0:
            return extract_left_leaf(lex[count+1:])          
            
def resolve_math_exp(lex, root):
    exp = MathExp()
    exp.lex = strip_parent(lex)   
    exp.root = root
    if not isLeaf(exp.lex):
        exp.opt = extract_opt(exp.lex)
        exp.left_leaf = resolve_math_exp(extract_left_leaf(exp.lex), exp)
        exp.right_leaf = resolve_math_exp(extract_right_leaf(exp.lex), exp)
    return exp

def gram_math_exp(math_lex):
    global LineIndex
    LineIndex = math_lex[0].line
    lex = strip_semicolon(math_lex)
    exp = resolve_math_exp(lex, None)
    MathExpList.append(exp)
    #exp.print(0)
    return exp

if __name__ == '__main__':
    math_lex = lex("test_grammer.c")
    gram_math_exp(math_lex)




