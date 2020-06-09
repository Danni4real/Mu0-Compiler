#!/usr/bin/python3
import sys
import re
from Define import *


class LexElement:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.line = LineIndex

LineIndex = 0
CurrentLine = ""
LexElementList = []


def err_handler(msg):
    print("Error: line", LineIndex, ":")
    print(CurrentLine)
    print(msg)
    exit(1)

def chop_and_save(line):
    if not line:
        return True
    element = LexElement()
    for lang_symbol in LANGUAGE_SYMBOLS:
        if line.startswith(lang_symbol):
            element.name = lang_symbol
            element.type = lang_symbol
            LexElementList.append(element)
            chop_and_save(line[len(lang_symbol):])
            return True


    if list(line)[0].isalpha():
        for i in range(len(line)):
            if i > 10:
                err_handler("symbol too long!")
            if not list(line)[i].isalpha():
                element.name = line[0: i]
                element.type = SYMBOL
                LexElementList.append(element)
                chop_and_save(line[i:])
                return True

    if list(line)[0].isdigit():
        for i in range(len(line)):
            if i > 4:
                err_handler("digit too big!")
            if not list(line)[i].isdigit():
                element.name = line[0: i]
                element.type = DIGIT
                LexElementList.append(element)
                chop_and_save(line[i:])
                return True

    err_handler("lex error!")
    

def process_each_line(c_src_file_path):
    global LineIndex
    global CurrentLine
    f = open(c_src_file_path, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        LineIndex += 1
        CurrentLine = line.replace("\n", "").strip()
        line = line.replace("\n", "").strip().replace(" ", "")
        chop_and_save(line)

    #for l in LexElementList:
    #    print("name:",l.name)
    #    print("type:",l.type)

    f.close()

def lex(c_src_file_path):
    process_each_line(c_src_file_path)
    return LexElementList

if __name__ == '__main__':
    c_src_file_path = sys.argv[1]
    lex(c_src_file_path)




