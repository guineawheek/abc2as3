'''
Created on Aug 1, 2010

@author: Aaron Cooper
'''

class AS3Class(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.__functions = []
        self.className = ""
        self.package = ""
        
    def addFunction(self, function):
        self.__functions.append(function)
        