#!/usr/bin/python3

from Lexer import lex
from Define import *
from ExpList import gram_exp_list


def gen_tree(src_file_path):
    _lex = lex(src_file_path)
    return gram_exp_list(_lex[1:])


if __name__ == '__main__':
    gen_tree("test.c")
