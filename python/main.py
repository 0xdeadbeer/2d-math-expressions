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
        "+": {},
        "-": {},
        "*": {},
        "/": {},
        "(": {},
        ")": {},
        " ": {},
    }

    def __init__ (self): 
        pass 

    @staticmethod
    def checkExpression(expression): 
        for char in expression: 
            
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
    def generateTokensArray(expression): 
        tokens_array = []

        tokens_array = re.split("([1234]+)|([6]+)", expression) 

        return tokens_array

    @staticmethod
    def scanTokens(expression): 

        tokens_array = privileges_array = levels_array = []

        if (not ProgramSettings.checkExpression(expression)): 
            raise InvalidExpression("Given expression is invalid")

        tokens_array = ProgramSettings.generateTokensArray(expression)

        if (not len(tokens_array)):
            raise InvalidExpression("Expression does not follow the expression rules")


        return [tokens_array, privileges_array, levels_array]

def main(): 
    expression = input("Enter expression: ")
    expression = str(expression).strip()
    
    try: 
        tokens, privileges, levels = ProgramSettings.scanTokens(expression)
        
        print ("Tokens -> " + str(tokens)) 
        print ("Privileges -> " + str(privileges)) 
        print ("Levels -> " + str(levels))
    except Exception as e: 
        print (str(e))

if __name__ == "__main__":
    main() 