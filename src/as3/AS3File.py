'''
Created on Aug 1, 2010

@author: Aaron Cooper
'''

class AS3File(object):

    def __init__(self):
        self.fileName = ""
        self.mainClass = None
        self.package = ""
        self.__internalClasses = []
        self.minorVersion = 0
        self.majorVersion = 0
        
    def addInternalClass(self, as3Class):
        self.__internalClasses.append(as3Class)