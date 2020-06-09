INT = "int"
ADD =  "+"
MINUS =  "-"
MULTI =  "*"
DIVID =  "/"
EQU = "=="
NEQ = "!="
BIGR = ">"
SMLR = "<"
ASN = "="
IF  = "if"
ELSE = "else"
WHILE = "while"
BREAK = "break"
BRACKET_L = "["
BRACKET_R = "]"
BRACE_L = "{"
BRACE_R = "}"
PARENT_L = "("
PARENT_R = ")"
SEMI_COLON = ";"
MAIN = "main"

COLON = ":"
SPACE = " "
LINE_BREAK = "\n"
SYMBOL = "symbol"
DIGIT = "digit"

TypeDeclExp =  0
TypeAsgnExp =  1
TypeIfExp =    2
TypeElseExp =  3
TypeWhileExp = 4
TypeBreakExp = 5
TypeMathExp =  6


CMD_LDA = "LDA"
CMD_STO = "STO"
CMD_ADD = "ADD"
CMD_SUB = "SUB"
CMD_JMP = "JMP"
CMD_JGE = "JGE"
CMD_JNE = "JNE"
CMD_STP = "STP"


ASM_IF_START_SYMBOL_POOL =  ("if_1_start", "if_2_start","if_3_start","if_4_start","if_5_start","if_6_start","if_7_start","if_8_start")
ASM_IF_END_SYMBOL_POOL =    ("if_1_end", "if_2_end","if_3_end","if_4_end","if_5_end","if_6_end","if_7_end","if_8_end")

ASM_ELSE_START_SYMBOL_POOL =  ("else_1_start", "else_2_start", "else_3_start", "else_4_start", "else_5_start", "else_6_start", "else_7_start", "else_8_start")
ASM_ELSE_END_SYMBOL_POOL =    ("else_1_end", "else_2_end", "else_3_end", "else_4_end", "else_5_end", "else_6_end", "else_7_end", "else_8_end")

ASM_WHILE_START_SYMBOL_POOL =  ("while_1_start", "while_2_start", "while_3_start", "while_4_start", "while_5_start", "while_6_start", "while_7_start", "while_8_start")
ASM_WHILE_END_SYMBOL_POOL =    ("while_1_end", "while_2_end", "while_3_end", "while_4_end", "while_5_end", "while_6_end", "while_7_end", "while_8_end")

ASM_WHILE_LOOP_SYMBOL_POOL = ("while_1_loop", "while_2_loop", "while_3_loop", "while_4_loop", "while_5_loop", "while_6_loop", "while_7_loop", "while_8_loop")


MATH_OPT = (ADD, MINUS, MULTI, DIVID)
COMP_OPT = (EQU, NEQ, BIGR, SMLR)
LANGUAGE_SYMBOLS = (INT, ADD, MINUS, MULTI, DIVID, EQU, NEQ, BIGR, SMLR, ASN, IF, ELSE, WHILE, BREAK, BRACKET_L, BRACKET_R, BRACE_L, BRACE_R, PARENT_L, PARENT_R, MAIN, SEMI_COLON)

class ExpList:
    def __init__(self):
        self.exp_list = []
    def print(self,indent):
        for exp in self.exp_list:
            exp.print(indent)

class AsgnExp:
    def __init__(self):
        self.type = TypeAsgnExp
        self.symbol = None
        self.math_exp = None
    def print(self,indent):
        print(" "*indent*4, end="")
        print("=")
        print(" "*(indent+1)*4, end="")
        print(self.symbol)
        self.math_exp.print(indent+1)

class DeclExp:
    def __init__(self):
        self.type = TypeDeclExp
        self.symbol = None
        self.math_exp = None
    def print(self, indent):
        print(" "*indent*4, end="")
        print("int")
        print(" "*(indent+1)*4, end="")
        print("=")
        print(" "*(indent+2)*4, end="")
        print(self.symbol)
        self.math_exp.print(indent+2)

class CompExp:
    def __init__(self):
        self.opt = None
        self.math_exp_l = None
        self.math_exp_r = None
    def print(self,indent):
        print(" "*indent*4, end="")
        print(self.opt)
        self.math_exp_l.print(1+indent)
        self.math_exp_r.print(1+indent)

class IfExp:
    def __init__(self):
        self.type = TypeIfExp
        self.has_else = False
        self.comp_exp = None
        self.exp_list = None
    def print(self,indent):
        print(" "*indent*4, end="")
        print("if")
        self.comp_exp.print(1+indent)
        self.exp_list.print(1+indent)

class ElseExp:
    def __init__(self):
        self.type = TypeElseExp
        self.exp_list = None
    def print(self,indent):
        print(" "*indent*4, end="")
        print("else")
        self.exp_list.print(1+indent)

class WhileExp:
    def __init__(self):
        self.type = TypeWhileExp
        self.comp_exp = None
        self.exp_list = None
    def print(self,indent):
        print(" "*indent*4, end="")
        print("while")
        self.comp_exp.print(1+indent)
        self.exp_list.print(1+indent)

class BreakExp:
    def __init__(self):
        self.type = TypeBreakExp
    def print(self,indent):
        print(" "*indent*4, end="")
        print("break")

class MathExp:
    def __init__(self):
        self.type = TypeMathExp
        self.lex = None
        self.opt = None
        self.root = None
        self.left_leaf = None
        self.right_leaf = None
    def print(self,indent):
        if self.left_leaf != None:
            print(" "*indent*4, end="")
            print(self.opt)

        if self.left_leaf == None:
            print(" "*indent*4, end="")
            print(self.lex[0].name,":",self.lex[0].type)
        else:   
            _indent = indent + 1         
            self.left_leaf.print(_indent)
            self.right_leaf.print(_indent)
