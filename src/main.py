'''
Created on Aug 1, 2010

@author: Aaron Cooper
'''

import sys
from as3 import ABCParser
from xml.dom import minidom

def main():
    if len(sys.argv) < 1:
        print("usage: file1 [file2 ...]")
        return 1;
    
    xml = minidom.parse("test_files\\simple.abc")
    parser = ABCParser.ABCParser(xml)
    parser.parse()
    
if __name__ == '__main__':
    main()
    