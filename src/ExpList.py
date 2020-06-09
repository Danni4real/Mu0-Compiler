#!/usr/bin/python3

from Lexer import lex
from Define import *

LineIndex = 0

def err_handler(msg):
    print("Error: Line:", LineIndex)
    print(msg)
    exit(1)

def strip_brace(lex):
    if lex[0].type == BRACE_L and lex[-1].type == BRACE_R:
        return lex[1:-1]
    else:
        err_handler("Error: brace not in pair!")
    return lex

def what_exp(lex):
    if lex[0].type == INT:
        return TypeDeclExp
    if lex[0].type == SYMBOL:
        return TypeAsgnExp
    if lex[0].type == IF:
        return TypeIfExp
    if lex[0].type == ELSE:
        return TypeElseExp
    if lex[0].type == WHILE:
        return TypeWhileExp
    if lex[0].type == BREAK:
        return TypeBreakExp

def chop_save_return_remain(exp_list, lex, exp_type):
    from AsgnExpGrammer import gram_asgn_exp
    from DeclExpGrammer import gram_decl_exp
    from IfElseWhileExpGrammer import gram_if_exp
    from IfElseWhileExpGrammer import gram_else_exp
    from IfElseWhileExpGrammer import gram_while_exp
    index = 0
    balance = -1
    if exp_type == TypeDeclExp:
        for item in lex:
            index += 1
            if item.type == SEMI_COLON:
                exp_list.append(gram_decl_exp(lex[:index])) 
                return lex[index:]
    if exp_type == TypeAsgnExp:
        for item in lex:
            index += 1
            if item.type == SEMI_COLON:
                exp_list.append(gram_asgn_exp(lex[:index])) 
                return lex[index:]
    if exp_type == TypeIfExp:
        for item in lex:
            index += 1
            if item.type == BRACE_L:
                if balance == -1:
                    balance = 1
                else:
                    balance += 1
            if item.type == BRACE_R:
                balance -= 1
            if balance == 0:
                exp_list.append(gram_if_exp(lex[:index])) 
                return lex[index:]
    if exp_type == TypeElseExp:
        for item in lex:
            index += 1
            if item.type == BRACE_L:
                if balance == -1:
                    balance = 1
                else:
                    balance += 1
            if item.type == BRACE_R:
                balance -= 1
            if balance == 0:
                exp_list.append(gram_else_exp(lex[:index])) 
                return lex[index:]
    if exp_type == TypeWhileExp:
        for item in lex:
            index += 1
            if item.type == BRACE_L:
                if balance == -1:
                    balance = 1
                else:
                    balance += 1
            if item.type == BRACE_R:
                balance -= 1
            if balance == 0:
                exp_list.append(gram_while_exp(lex[:index])) 
                return lex[index:]
    if exp_type == TypeBreakExp:
        break_exp = BreakExp()
        exp_list.append(break_exp)
        return lex[2:]
    

def extract_each_exp(lex, exp_list):
    if lex:
        extract_each_exp(chop_save_return_remain(exp_list,lex, what_exp(lex)), exp_list)


def gram_exp_list(lex_list):
    lex = strip_brace(lex_list)
    exp = ExpList()
    extract_each_exp(lex, exp.exp_list)
    #exp.print(0)
    return exp

if __name__ == '__main__':
    lex = lex("test_grammer_exp_list.c")
    gram_exp_list(lex)

