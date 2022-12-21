#!/usr/bin/python3 

# importing libs 

import os 
import sys 
import math 
import random 
import re
import pprint
from unittest import result
import uuid 

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

    symbols = {
        "+": {
            "privilege": 4,
            "label": "operator"
        },
        "-": {
            "privilege": 4,
            "label": "operator"
        },
        "*": {
            "privilege": 3,
            "label": "operator"
        },
        "/": {
            "privilege": 3,
            "label": "operator"
        },
        "^": {
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

    unnecessary_tokens = {
        "(": {}, 
        ")": {}
    }

    def __init__ (self): 
        pass 

    @staticmethod
    def check_expession(expression): 

        symbols = "".join(["\\" + symbol for symbol in ProgramSettings.symbols.keys()])
        regex_expression = f"^[a-z0-9{symbols}]+$"
        return re.match(regex_expression, expression)

    @staticmethod 
    def isolate_elements(expression): 
        tokens_array = []
        
        symbols = "".join(["\\" + symbol for symbol in ProgramSettings.symbols.keys()])

        regex = f"(?:[0-9]+)|(?:[a-z]+)|(?:[{symbols}])"

        tokens_array = re.findall(regex, expression)

        return tokens_array

    @staticmethod
    def return_token_type(token): 
        if (re.match(r"^[0-9]+$", token)):
            return "num"
        
        if (re.match(r"^[a-z]+$", token)):
            return "var"
        
        if (token in ProgramSettings.symbols): 
            return "symbol"
        
        raise InvalidExpression(f"Invalid token type {str(token)}")

    @staticmethod 
    def convert_to_type_tokens(tokens_array): 
        type_tokens_array = [] 

        for token in tokens_array: 
            type_token = None
            if (token.isnumeric()):
                number = int(token)
                type_token = tokens.typetokens.Number(number, 1) 
            elif (re.match(r"^[a-z]+$", token)):
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

        tokens_array = ProgramSettings.isolate_elements(expression)

        if (not len(tokens_array)):
            raise InvalidExpression("Expression does not follow the expression rules")

        tokens_array = ProgramSettings.convert_to_type_tokens(tokens_array) 

        if (not ProgramSettings.check_token_rules(tokens_array)):
            raise InvalidExpression("Given expression is invalid") 

        privileges_array = [ token.privilege for token in tokens_array ]

        levels_array = ProgramSettings.generate_levels_array(privileges_array, tokens_array)
        new_tokens_array = [] 
        new_privileges_array = [] 
        new_levels_array = [] 

        for index, token in enumerate(tokens_array): 
            token_value = str(token.value) 
            if (token_value not in ProgramSettings.unnecessary_tokens):
                new_privileges_array.append(privileges_array[index])
                new_tokens_array.append(tokens_array[index])
                new_levels_array.append(levels_array[index])

        return [new_tokens_array, new_privileges_array, new_levels_array]

    @staticmethod 
    def generate_data_tree(tokens, privileges, levels): 

        tree = {}
        index_dictionary = {} 

        for index, token in enumerate(tokens): 

            level = levels[index]
            privilege = privileges[index]

            if (level not in tree): 
                tree[level] = {"level": level, "privileges": {}}

            if privilege not in tree[level]["privileges"]: 
                tree[level]["privileges"][privilege] = {"privilege": privilege, "elements": []}

            token_id = str(uuid.uuid4()) 

            tree[level]["privileges"][privilege]["elements"].append({
                "index": index, 
                "value": token, 
                "id": token_id
            })

            index_dictionary[index] = token_id

        return [ tree, index_dictionary ]

    @staticmethod 
    def sync_element(dictionary, target_id, pointing_id): 
        while isinstance(dictionary[target_id], tokens.tokens.Pointer):
            target_id = dictionary[target_id].fetch_destination()
        
        dictionary[target_id] = tokens.tokens.Pointer(pointing_id)

    @staticmethod 
    def find_target(dictionary, target_id): 
        while isinstance(dictionary[target_id], tokens.tokens.Pointer):
            target_id = dictionary[target_id].fetch_destination()
                
        return dictionary[target_id] 
    
    @staticmethod
    def generate_result(tree, index_dictionary):
        
        result_array = {} 

        levels = list(tree.keys())
        levels.sort(reverse=True)

        for level in levels: 
            
            level = tree[level] 
            
            privileges = list(level["privileges"].keys())
            privileges.sort()

            for privilege in privileges: 
                
                privilege = level["privileges"][privilege]
                privilege_num = privilege["privilege"]

                for element in privilege["elements"]: 

                    index = element["index"] 
                    token = element["value"]
                    id = element["id"]

                    if (isinstance(token, tokens.typetokens.Number)):
                        token = tokens.tokens.Number(token.value)
                    elif (isinstance(token, tokens.typetokens.Variable)):
                        token = tokens.tokens.Variable(token.value)
                    elif (isinstance(token, tokens.typetokens.Symbol)):

                        left_index = index - 1
                        right_index = index + 1 
                        left_id = index_dictionary[left_index]
                        right_id = index_dictionary[right_index]


                        left = ProgramSettings.find_target(result_array, left_id) 
                        right = ProgramSettings.find_target(result_array, right_id) 

                        token = tokens.tokens.Operator(left, right, privilege_num, token.value)
    
                        ProgramSettings.sync_element(result_array, left_id, id)
                        ProgramSettings.sync_element(result_array, right_id, id)

                    else: 
                        
                        raise InvalidExpression("Program error..")

                    result_array[id] = token 
        return result_array 

def printTree(root, level=0):
    try:
        print("  " * level, root.label)
    except Exception: 
        print ("  " * level, root.value)
        return 
    
    printTree(root.left, level + 1)
    printTree(root.right, level + 1)


def help_page(): 
    print (" __   __                        _             ")
    print (" \ \ / /                       (_)            ")
    print ("  \ V / _ __  _ __ ___  ___ ___ _  ___  _ __  ")
    print ("   > < | '_ \| '__/ _ \/ __/ __| |/ _ \| '_ \ ")
    print ("  / . \| |_) | | |  __/\__ \__ \ | (_) | | | |")
    print (" /_/ \_\ .__/|_|  \___||___/___/_|\___/|_| |_|")
    print ("       | Coded by: https://github.com/osamu-kj")
    print ("       |_|                                    ")

    print ()
    print ("Usage: python3 main.py [math expression]")
    print ("Example: python3 main.py 1+2")

def main(): 
    if (len(sys.argv) == 1): 
        help_page()
        return 

    expression = sys.argv[1:]
    expression = "".join(expression)
    expression = str(expression).strip()

    tokens_ = privileges_ = levels_ = None 

    try: 
        tokens_, privileges_, levels_ = ProgramSettings.scan_tokens(expression)
    except Exception as e: 
        print (str(e))
        return 

    tree, index_dictionary  = ProgramSettings.generate_data_tree(tokens_, privileges_, levels_) 
    result_array = ProgramSettings.generate_result(tree, index_dictionary)

    for result in result_array: 
        if isinstance(result_array[result], tokens.tokens.Operator):
            printTree(result_array[result])

if __name__ == "__main__":
    main() 
