'''
Created on Aug 1, 2010

@author: Aaron Cooper
'''

class FlashSWF(object):
    '''
    classdocs
    '''
    compressed = False
    xmlns = ""
    framerate = 0
    size = ""
    version = 0
    
    def __init__(self):
        self.__files = []
    
    def addFile(self, as3File):
        self.__files.append(as3File)
        
    def getfiles(self):
        return self.__files
    
    files = property(getfiles)