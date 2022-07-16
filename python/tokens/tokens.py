#!/usr/bin/python3 
# token objects that store their values, properties, privileges, etc. 

import os 
import sys

class Token(): 
    def __init__ (self): 
        pass

class Number(Token):
    def __init__ (self, value): 
        self.value = value 
    
    def __str__ (self): 
        return str(self.value)

class Variable(Token): 
    def __init__ (self, value): 
        self.value = value 
    
    def __str__ (self): 
        return self.value 

class Brackets(Token): 
    def __init__ (self, start, content, end): 
        self.start = start, 
        self.content = content,  
        self.end = end 
        self.privilege = 5 
    
    def __str__ (self): 
        return self.start + str(self.content) + self.end

class Operator(Token): 
    def __init__ (self, left, right, privilege, label): 
        self.left = left 
        self.right = right 
        self.privilege = privilege
        self.label = label 
    
    def __str__ (self, level=0): 
        return str(self.left) + self.label + str(self.right)
