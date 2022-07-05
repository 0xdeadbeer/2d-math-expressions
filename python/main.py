#!/usr/bin/python3 

# importing libs 

import os 
import sys 
import math 
import random 

# inserts 
sys.path.insert(1, './tokens')

# importing local files 
import tokens.tokens


# classes

class ProgramSettings(): 

    tokens = {
        "num": tokens.tokens.Number,
        "var": tokens.tokens.Variable,
        "()": tokens.tokens.Brackets,
        "+": tokens.tokens.Operator,
        "-": tokens.tokens.Operator,
        "*": tokens.tokens.Operator,
        "/": tokens.tokens.Operator,
    }

    def __init__ (): 
        pass 

    def find_token(self, token_array, token_position): 
        token = token_array[token_position]
        token_object = self.tokens[token]()

def main(): 
    expression = input("Enter expression: ")


if __name__ == "__main__":
    main() 