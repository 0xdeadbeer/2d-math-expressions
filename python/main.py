#!/usr/bin/python3 

# importing libs 

import os 
import sys 
import math 
import random 
import re

# inserts 
sys.path.insert(0, ".")

# importing local files 
import tokens.tokens
import tokens.typetokens

# exceptions 
class InvalidExpression(Exception):
    pass

# classes

class ProgramSettings(): 

    numbers = {
        "1": {},
        "2": {},
        "3": {},
        "4": {},
        "5": {},
        "6": {},
        "7": {},
        "8": {},
        "9": {},
        "0": {},
    }

    vars = {
        "a": {},
        "b": {},
        "c": {},
        "d": {},
        "e": {},
        "f": {},
        "g": {},
        "h": {},
        "i": {},
        "j": {},
        "k": {},
        "l": {},
        "m": {},
        "n": {},
        "o": {},
        "p": {},
        "q": {},
        "r": {},
        "s": {},
        "t": {},
        "u": {},
        "v": {},
        "w": {},
        "x": {},
        "y": {},
        "z": {},
    }

    symbols = {
        "+": {
            "privilege": 3,
            "label": "operator"
        },
        "-": {
            "privilege": 3,
            "label": "operator"
        },
        "*": {
            "privilege": 2,
            "label": "operator"
        },
        "/": {
            "privilege": 2,
            "label": "operator"
        },
        "(": {
            "privilege": 5,
            "label": "privilege_operator"
        },
        ")": {
            "privilege": 5,
            "label": "privilege_operator"
        },
    }

    def __init__ (self): 
        pass 

    @staticmethod
    def check_expession(expression): 
        for char in expression: 
            
            # check if its a empty space 
            if (not char.strip()): 
                continue 

            # check if its a number 
            if (char in ProgramSettings.numbers): 
                continue 
            
            # check if its a var 
            if (char in ProgramSettings.vars):
                continue 
            
            # check if its a valid symbol 
            if (char in ProgramSettings.symbols): 
                continue 
            
            # its something unknown 
            return False
            
        return True 

    @staticmethod 
    def generate_tokens_array(expression): 
        tokens_array = []
        
        numbers = "".join(ProgramSettings.numbers.keys())
        vars = "".join(ProgramSettings.vars.keys())
        symbols = "".join(["\\" + symbol for symbol in ProgramSettings.symbols.keys()])

        regex = f"(?:[{numbers}]+)|(?:[{vars}]+)|(?:[{symbols}])"

        tokens_array = re.findall(regex, expression)

        return tokens_array

    @staticmethod
    def find_token_type(token): 
        if (token.isnumeric()):
            return "num"
        
        if (token in ProgramSettings.vars):
            return "var"
        
        if (token in ProgramSettings.symbols): 
            return "symbol"
        
        raise InvalidExpression(f"Invalid token type {str(token)}")

    @staticmethod 
    def generate_type_tokens_array(tokens_array): 
        type_tokens_array = [] 

        for token in tokens_array: 
            type_token = None
            if (token.isnumeric()):
                number = int(token)
                type_token = tokens.typetokens.Number(number, 1) 
            elif (token.isalpha() and token in ProgramSettings.vars):
                type_token = tokens.typetokens.Variable(token, 1)
            elif (token in ProgramSettings.symbols):
                privilege = ProgramSettings.symbols[token]["privilege"]
                label = ProgramSettings.symbols[token]["label"]
                type_token = tokens.typetokens.Symbol(token, label, privilege)

            type_tokens_array.append(type_token)

        return type_tokens_array 

    @staticmethod 
    def check_token_rules(tokens_array): 
        return True

    @staticmethod
    def scan_tokens(expression): 

        tokens_array = privileges_array = levels_array = []

        if (not ProgramSettings.check_expession(expression)): 
            raise InvalidExpression("Given expression is invalid")

        tokens_array = ProgramSettings.generate_tokens_array(expression)

        if (not len(tokens_array)):
            raise InvalidExpression("Expression does not follow the expression rules")

        tokens_array = ProgramSettings.generate_type_tokens_array(tokens_array) 

        if (not ProgramSettings.check_token_rules(tokens_array)):
            raise InvalidExpression("Given expression is invalid") 
        


        return [tokens_array, privileges_array, levels_array]

def main(): 
    expression = input("Enter expression: ")
    expression = str(expression).strip()
    
    try: 
        tokens, privileges, levels = ProgramSettings.scan_tokens(expression)
        
        print ("Tokens -> " + str(tokens)) 
        print ("Privileges -> " + str(privileges)) 
        print ("Levels -> " + str(levels))
    except Exception as e: 
        print (str(e))

if __name__ == "__main__":
    main() 