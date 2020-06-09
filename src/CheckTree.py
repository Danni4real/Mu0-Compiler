#!/usr/bin/python3

from GenTree import gen_tree
from Define import *
SymbolList = []
InsideWhile = 0
def err_handler(msg, line):
    print("Error: Line:", line)
    print(msg)
    exit(1)

def check_symbol_math_exp(exp):
    if exp.left_leaf != None:
        check_symbol_math_exp(exp.left_leaf)
        check_symbol_math_exp(exp.right_leaf)
    else:
        if exp.lex[0].type == SYMBOL:
            if not exp.lex[0].name in SymbolList:
                err_handler("Error: symbol "+exp.lex[0].name+" not declared!", exp.lex[0].line)
                


def check_symbol(tree):
    global SymbolList
    for exp in tree.exp_list:
        if exp.type == TypeDeclExp:
            check_symbol_math_exp(exp.math_exp)
            if exp.symbol in SymbolList:
                err_handler("Error: symbol "+exp.symbol+" already declared!", exp.math_exp.lex[0].line)
            SymbolList.append(exp.symbol)
        if exp.type == TypeAsgnExp:
            if not exp.symbol in SymbolList:
                err_handler("Error: symbol "+exp.symbol+" not declared!", exp.math_exp.lex[0].line)
            check_symbol_math_exp(exp.math_exp)
        if exp.type == TypeIfExp or exp.type == TypeWhileExp:
            check_symbol_math_exp(exp.comp_exp.math_exp_l)
            check_symbol_math_exp(exp.comp_exp.math_exp_r)
            check_symbol(exp.exp_list)
        if exp.type == TypeElseExp:
            check_symbol(exp.exp_list)
        

def check_else(tree):
    index = 0
    for exp in tree.exp_list:
        if exp.type == TypeElseExp:
            if index == 0 or (tree.exp_list[index-1].type != TypeIfExp):
                err_handler("Error: else expression should below a if expression!",0)
            if index !=0 and tree.exp_list[index-1].type == TypeIfExp:
                tree.exp_list[index-1].has_else = True
        if exp.type == TypeIfExp or exp.type == TypeWhileExp:
            check_else(exp.exp_list)
        index += 1

def check_break(tree):
    global InsideWhile

    for exp in tree.exp_list:
        if exp.type == TypeBreakExp and InsideWhile == 0:
            err_handler("Error: break expression should be inside a while expression!",0)
        if exp.type == TypeWhileExp:
            InsideWhile += 1
            check_break(exp.exp_list)
            InsideWhile -= 1
        if exp.type == TypeIfExp:
            check_break(exp.exp_list)
            

def check_tree(tree):
    check_symbol(tree)
    check_else(tree)
    check_break(tree)
    return

if __name__ == '__main__':
    tree = gen_tree("test.c")
    tree.print(0)
    check_tree(tree)
