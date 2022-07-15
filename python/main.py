#!/usr/bin/python3 

# importing libs 

import os 
import sys 
import math 
import random 
import re
import pprint
from unittest import result

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
        return True # TODO

    @staticmethod 
    def generate_levels_array(privileges_array, tokens_array): 
        
        levels_array = [] 
        brackets_trace = [] 
        level = 0

        for index, privilege in enumerate(privileges_array): # TODO: implement function that checks whether it should count it in
            value = str(tokens_array[index].value)
            if (privilege != 5): 
                levels_array.append(level)
                continue

            if (value == "("):
                levels_array.append(level) 
                brackets_trace.append(1)
                
                level += 1 
            elif (value == ")"): 
                if (level <= 0 or len(brackets_trace) <= 0): 
                    raise InvalidExpression("Program error..")

                level -= 1
                levels_array.append(level)
                brackets_trace.pop()
            else: 
                raise InvalidExpression("Program error..")

        if (len(brackets_trace) > 0): 
            raise InvalidExpression("Program error..")

        return levels_array 

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
        
        privileges_array = [ token.privilege for token in tokens_array ]

        # find out the levels array
        levels_array = ProgramSettings.generate_levels_array(privileges_array, tokens_array)

        # remove the 5's 
        for index, privilege in enumerate(privileges_array): 
            if (privilege == 5):
                privileges_array.pop(index)
                tokens_array.pop(index)
                levels_array.pop(index)
        
        return [tokens_array, privileges_array, levels_array]

    @staticmethod 
    def generate_data_tree(tokens, privileges, levels): 

        tree = {}

        for index, token in enumerate(tokens): 

            level = levels[index]
            privilege = privileges[index]

            # blacklist the ones that we dont need 
            if (privilege == 5):
                continue 

            if (level not in tree): 
                tree[level] = {"level": level, "privileges": {}}

            if privilege not in tree[level]["privileges"]: 
                tree[level]["privileges"][privilege] = {"privilege": privilege, "elements": []}

            tree[level]["privileges"][privilege]["elements"].append({
                "index": index, 
                "value": token
            })

        return tree 

    @staticmethod 
    def update_elements(token, results_array, index, update_index, incrementer): 
        _index = index + update_index 
        if (len(results_array) > _index and _index >= 0):
            if (isinstance(results_array[_index], tokens.tokens.Operator)):
                ProgramSettings.update_elements(token, results_array, _index, update_index, incrementer)

            results_array[_index] = token 

    @staticmethod
    def generate_result(size, tree):
        
        result_array = [None] * size 

        levels = list(tree.keys())
        levels.sort(reverse=True)

        for level in levels: 
            
            level = tree[level] 
            
            privileges = list(level["privileges"].keys())
            privileges.sort()

            for privilege in privileges: 
                
                print (level["privileges"].keys())
                privilege = level["privileges"][privilege]
                privilege_num = privilege["privilege"]

                for element in privilege["elements"]: 

                    index = element["index"] 
                    token = element["value"]

                    if (isinstance(token, tokens.typetokens.Number)):
                        token = tokens.tokens.Number(token.value)
                    elif (isinstance(token, tokens.typetokens.Variable)):
                        token = tokens.tokens.Variable(token.value)
                    elif (isinstance(token, tokens.typetokens.Symbol)):

                        left_index = index - 1
                        right_index = index + 1 
                        left = result_array[left_index]
                        right = result_array[right_index]

                        token = tokens.tokens.Operator(left, right, privilege_num, token.value)
    
                        ProgramSettings.update_elements(token, result_array, index, 1, 1)
                        ProgramSettings.update_elements(token, result_array, index, -1, -1)

                    else: 
                        
                        raise InvalidExpression("Program error..")

                    result_array[index] = token 

        return result_array 

def printTree(root, level=0):
    try:
        print("  " * level, root.label)
    except Exception: 
        print ("  " * level, root.value)
        return 
    
    printTree(root.left, level + 1)
    printTree(root.right, level + 1)

def main(): 
    expression = input("Enter expression: ")
    expression = str(expression).strip()
    

    tokens = privileges = levels = None 

    try: 
        tokens, privileges, levels = ProgramSettings.scan_tokens(expression)
    except Exception as e: 
        print (str(e))
        return 

    tree = ProgramSettings.generate_data_tree(tokens, privileges, levels) 

    result_array = ProgramSettings.generate_result(len(tokens), tree)
    
    result = result_array[0]
    print ("Expression -> " + expression)
    print ("Result -> " + str(result))
    print ("Result tree -> ")
    printTree(result)

if __name__ == "__main__":
    main() 