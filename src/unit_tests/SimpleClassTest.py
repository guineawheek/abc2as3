'''
Created on Aug 24, 2010

@author: Aaron Cooper
'''

import unittest
from as3 import ABCParser
from xml.dom import minidom

class SimpleABCTest(unittest.TestCase):
    
    def setUp(self):
        abcXMLDocument = minidom.parse("../test_files/simple.abc")
        abcParser = ABCParser.ABCParser(abcXMLDocument)
        abcParser.parse()
        self.__swf = abcParser.swf

    def testSwfBasicData(self):
        self.assertEqual(self.__swf.xmlns, "http://macromedia/2003/swfx")
        self.assertEqual(self.__swf.version, '10')
        self.assertEqual(self.__swf.framerate, 24)
        self.assertEqual(self.__swf.size, "10000x7500")
        self.assertEqual(self.__swf.compressed, True)
        
    
    def testSwfNumberOfFiles(self):
        self.assertEqual(len(self.__swf.files), 1)

    def testSwfFileVersions(self):
        self.assertEqual(self.__swf.files[0].minorVersion, 16)
        self.assertEqual(self.__swf.files[0].majorVersion, 46)
