#!/usr/bin/python3 

import os 
import sys 

class TypeToken: 
    def __init__(self, value, privilege ): 
        self.value = value
        self.privilege = privilege
    
    def __str__ (self): 
        return str(self.value)
class Number (TypeToken): 
    pass 

class Variable (TypeToken): 
    pass 

class Symbol (TypeToken): 
    def __init__ (self, value, label, privilege): 
        self.value = value 
        self.label = label 
        self.privilege = privilege