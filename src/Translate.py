#!/usr/bin/python3

from Define import *
from GenTree import gen_tree
from CheckTree import check_tree

SymbolList = []
IfSymbolIndex = 0
ElseSymbolIndex = 0
WhileSymbolIndex = 0
CurrentWhileLevel = 0


class AsmCmd:
    def __init__(self):
        self.cmd = None
        self.symbol = None
    def print(self):
        print("cmd:",self.cmd)
        print("symbol:",self.symbol)

class AsmBlock:
    def __init__(self):
        self.list = []
    def print(self):
        for l in self.list:
            l.print()

class Symbol:
    def __init__(self):
        self.name = ""
        self.value = 0
    def print(self):
        print("symbol name: ",self.name)
        print("symbol value:",self.value)

AsmList = AsmBlock()

def err_handler(msg, line):
    print("Error: Line:", line)
    print(msg)
    exit(1)

def find_symbol(tree):
    global SymbolList
    for exp in tree.exp_list:
        if exp.type == TypeDeclExp:
            s = Symbol()
            s.name = exp.symbol
            if exp.math_exp.left_leaf == None and exp.math_exp.lex[0].type == DIGIT:
                s.value = int(exp.math_exp.lex[0].name)
            SymbolList.append(s)
        if exp.type == TypeIfExp or exp.type == TypeWhileExp:
            find_symbol(exp.exp_list)



def TransMathExp(exp):
    global AsmList
    if exp.left_leaf != None:
        cmd = AsmCmd()
        cmd.cmd = CMD_LDA
        cmd.symbol = exp.left_leaf.lex[0].name
        AsmList.list.append(cmd)
        cmd = AsmCmd()
        if exp.opt == ADD:       
            cmd.cmd = CMD_ADD
        if exp.opt == MINUS:       
            cmd.cmd = CMD_SUB
        cmd.symbol = exp.right_leaf.lex[0].name
        AsmList.list.append(cmd)
    else:
        cmd = AsmCmd()
        cmd.cmd = CMD_LDA
        cmd.symbol = exp.lex[0].name
        AsmList.list.append(cmd)
    
def TransCompExp(exp, jmp_start_symbol, jmp_end_symbol):
    global AsmList
    if exp.opt != SMLR:
        cmd = AsmCmd()
        cmd.cmd = CMD_LDA
        cmd.symbol = exp.math_exp_r.lex[0].name
        AsmList.list.append(cmd)
        cmd = AsmCmd()
        cmd.cmd = CMD_SUB
        cmd.symbol = exp.math_exp_l.lex[0].name   
        AsmList.list.append(cmd)
    if exp.opt == SMLR:
        cmd = AsmCmd()
        cmd.cmd = CMD_LDA
        cmd.symbol = exp.math_exp_l.lex[0].name
        AsmList.list.append(cmd)
        cmd = AsmCmd()
        cmd.cmd = CMD_SUB
        cmd.symbol = exp.math_exp_r.lex[0].name   
        AsmList.list.append(cmd)
    if exp.opt == EQU:
        cmd = AsmCmd()
        cmd.cmd = CMD_JNE
        cmd.symbol = jmp_end_symbol
        AsmList.list.append(cmd)
    if exp.opt == NEQ:
        cmd = AsmCmd()
        cmd.cmd = CMD_JNE
        cmd.symbol = jmp_start_symbol
        AsmList.list.append(cmd)
        cmd = AsmCmd()
        cmd.cmd = CMD_JMP
        cmd.symbol = jmp_end_symbol
        AsmList.list.append(cmd)
        cmd = AsmCmd()
        cmd.symbol = jmp_start_symbol + COLON
        AsmList.list.append(cmd)
    if exp.opt == SMLR or exp.opt == BIGR:
        cmd = AsmCmd()
        cmd.cmd = CMD_JGE
        cmd.symbol = jmp_end_symbol
        AsmList.list.append(cmd)
    

def translate(tree):
    global IfSymbolIndex
    global ElseSymbolIndex
    global WhileSymbolIndex
    global CurrentWhileLevel
       
    for exp in tree.exp_list:
        if exp.type == TypeAsgnExp:
            TransMathExp(exp.math_exp)
            cmd = AsmCmd()
            cmd.cmd = CMD_STO
            cmd.symbol = exp.symbol
            AsmList.list.append(cmd)

        if exp.type == TypeIfExp:
            if_symbol_index = IfSymbolIndex
            else_symbol_index = ElseSymbolIndex
            if exp.has_else:
                TransCompExp(exp.comp_exp,ASM_IF_START_SYMBOL_POOL[if_symbol_index], ASM_ELSE_START_SYMBOL_POOL[else_symbol_index])
                ElseSymbolIndex += 1
            else:
                TransCompExp(exp.comp_exp,ASM_IF_START_SYMBOL_POOL[if_symbol_index], ASM_IF_END_SYMBOL_POOL[if_symbol_index])
            IfSymbolIndex += 1
            translate(exp.exp_list)
            cmd = AsmCmd()
            cmd.symbol = ASM_IF_END_SYMBOL_POOL[if_symbol_index] + COLON
            AsmList.list.append(cmd)

        if exp.type == TypeElseExp:
            cmd = AsmCmd()
            cmd.cmd = CMD_JMP
            cmd.symbol = ASM_ELSE_END_SYMBOL_POOL[else_symbol_index]
            AsmList.list.append(cmd)
            cmd = AsmCmd()
            cmd.symbol = ASM_ELSE_START_SYMBOL_POOL[else_symbol_index] + COLON
            AsmList.list.append(cmd)           
            translate(exp.exp_list)
            cmd = AsmCmd()
            cmd.symbol = ASM_ELSE_END_SYMBOL_POOL[else_symbol_index] + COLON
            AsmList.list.append(cmd)

        if exp.type == TypeWhileExp:
            while_symbol_index = WhileSymbolIndex
            cmd = AsmCmd()
            cmd.symbol = ASM_WHILE_LOOP_SYMBOL_POOL[while_symbol_index] + COLON
            AsmList.list.append(cmd)
            TransCompExp(exp.comp_exp,ASM_WHILE_START_SYMBOL_POOL[while_symbol_index], ASM_WHILE_END_SYMBOL_POOL[while_symbol_index])
            WhileSymbolIndex += 1
            translate(exp.exp_list)
            cmd = AsmCmd()
            cmd.cmd = CMD_JMP
            cmd.symbol = ASM_WHILE_LOOP_SYMBOL_POOL[while_symbol_index]
            AsmList.list.append(cmd)
            cmd = AsmCmd()
            cmd.symbol = ASM_WHILE_END_SYMBOL_POOL[while_symbol_index] + COLON
            AsmList.list.append(cmd)

def add_stp():
    cmd = AsmCmd()
    cmd.cmd = CMD_STP
    AsmList.list.append(cmd)


def gen_asm_text(asm_file_p,tree):
    translate(tree)
    add_stp()
    print(".text", file = asm_file_p)
    for c in AsmList.list:
        if c.cmd != None and c.symbol != None:
            print("        %s %s" % (c.cmd, c.symbol), file = asm_file_p)
        elif c.symbol == None:
            print("        %s" % (c.cmd), file = asm_file_p)
        else:
            print("    %s" % (c.symbol), file = asm_file_p)

def gen_asm_data(asm_file_p):
    print(".data", file = asm_file_p)
    for s in SymbolList:
        print("    %s:" % (s.name), file = asm_file_p)
        print("        %s" % (s.value), file = asm_file_p)


def c2asm(c_file_path, asm_file_path):
    tree = gen_tree(c_file_path)
    asm_file_p = open(asm_file_path,"w+")
    check_tree(tree)
    find_symbol(tree)
    gen_asm_text(asm_file_p,tree)
    gen_asm_data(asm_file_p)   

if __name__ == '__main__':
    c2asm("test.c", "out.asm")


























