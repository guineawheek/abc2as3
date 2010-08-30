'''
Created on Aug 1, 2010

@author: Aaron Cooper
'''
from xml.dom import minidom, Node
import re
from as3.FlashSWF import FlashSWF
from as3.AS3File import AS3File
from as3.AS3Class import AS3Class

class ABCParser(object):
    '''
    classdocs
    '''

    def __init__(self, byteCode):
        '''
        Constructor
        '''
        if isinstance(byteCode, str):
            self.__abcXMLDoc = minidom.parseString(byteCode)
        else:
            self.__abcXMLDoc = byteCode
        
    def parse(self):
        '''
        Scan through the byte code doc looking for nodes labelled 'DoABC2'
        '''
        if self.__abcXMLDoc.documentElement.nodeName == "swf":
            self.__parseSWFData(self.__abcXMLDoc.documentElement)
            for abcNode in self.__abcXMLDoc.documentElement.childNodes:
                if abcNode.nodeType == Node.ELEMENT_NODE and abcNode.nodeName == "DoABC2":
                    self.__parseABCNode(abcNode)
        
    def __parseSWFData(self, swfNode):
        self.__swf = FlashSWF()
        for index in range(swfNode.attributes.length):
            
            attrNode = swfNode.attributes.item(index)
            if attrNode.nodeType == Node.ATTRIBUTE_NODE:
                if attrNode.name == "compressed":
                    self.__swf.compressed = bool(attrNode.nodeValue)
                elif attrNode.name == "xmlns":
                    self.__swf.xmlns = attrNode.nodeValue
                elif attrNode.name == "framerate":
                    self.__swf.framerate = int(attrNode.nodeValue)
                elif attrNode.name == "size":
                    self.__swf.size = attrNode.nodeValue
                elif attrNode.name == "version":
                    self.__swf.version = attrNode.nodeValue
    
    def __parseABCNode(self, abcNode):
        textNode = abcNode.firstChild
        
        if textNode.nodeType != Node.TEXT_NODE:
            return None
        
        abcTextLines = textNode.nodeValue.splitlines()
        
        versionRE = re.compile("[\s]*([\d]+) ([\d]+) ([\w]+) version")
        constantPoolRE = re.compile("[\s]*([\d]+) ([\w\s]+) Constant Pool Entries")
        entriesRE = re.compile("[\s]*([\d]+) ([\w]+) Entries")
        bodiesRE = re.compile("[\s]*([\d]+) ([\w]+) Bodies")
        as3File = AS3File()
        
        for index, line in enumerate(abcTextLines):
            match = versionRE.match(line)
            if match:
                self.__processVersion(as3File, match)
                continue
            match = constantPoolRE.match(line)
            if match:
                self.__processConstantPool(as3File, match, abcTextLines, index)
                continue
            match = entriesRE.match(line)
            if match:
                self.__processEntries(as3File, match, abcTextLines, index)
                continue
            match = bodiesRE.match(line)
            if match:
                self.__processBodies(as3File, match, abcTextLines, index)
                continue
                
        self.__swf.addFile(as3File)

    def __processVersion(self, file, match):
        if match.group(3) == "minor":
            file.minorVersion = int(match.group(1))
        else:
            file.majorVersion = int(match.group(1))
    
    def __processConstantPool(self, file, match, lines, startingLineNum):
        linesToProc = lines[startingLineNum + 1:startingLineNum + int(match.group(1))]
        
        if match.group(2).lower() == "string" and len(linesToProc) > 0:
            mainClass = AS3Class()
            splitStr = linesToProc[0].lstrip().split(':')
            mainClass.className = splitStr[-1]
            mainClass.package = ".".join(splitStr[0:-1])
        
            file.mainClass = mainClass
        
        i = 1
        while i < len(linesToProc):
            if linesToProc[i] == "\n":
                continue
                
            i += 1
    
    def __processEntries(self, file, match, lines, startingLineNum):
        return None
    
    def __processBodies(self, file, match, lines, startingLineNum):
        if match.group(2).lower() == "method":
            processing = False
            functionLines = []
            functionsFound = 0
            functionsToFind = int(match.group(1))
            
            functionStartRE = re.compile("^[\s]*function [\w\d:\(\)\$\s,]+$")
            functionEndRE = re.compile("^[\s]*[\d] Traits Entries$")
            
            lineNum = startingLineNum
            while functionsFound < functionsToFind:
                lineNum += 1
                if processing:
                    lineMatch = functionEndRE.match(lines[lineNum])
                    if lineMatch:
                        file.mainClass.addFunction(self.__parseFunction(functionLines))
                        functionLines = []
                        processing = False
                        functionsFound += 1
                    else:
                        functionLines.append(lines[lineNum].lstrip())
                    continue
                
                functionMatch = functionStartRE.match(lines[lineNum])
                if functionMatch:
                    processing = True
                    functionLines.append(lines[lineNum].lstrip())
                    functionLines.append(lines[lineNum + 1].lstrip())
                    lineNum += 2
                    continue
                
            
    def __parseFunction(self, lines):
        cinitFunctionStartRE = re.compile("^[\s]*function ([\w\d:]+)\$([\w\d]+)\(([\w\d:,]*)\):$")
        constructorFunctionStartRE = re.compile("^[\s]*function ([\w\d:]+):([\w\d]+)\(([\w\d:,]*)\):$")
        regularFunctionStartRE = re.compile("^[\s]*function ([\w\d:]+):::([\w\d]+)\(([\w\d:,]*)\)::([\w\d]+)$")
        getFunctionStartRE = re.compile("^[\s]*function get ([\w\d:]+):::([\w\d]+)\(([\w\d:,]*)\)::([\w\d]+)$")
        setFunctionStartRE = re.compile("^[\s]*function set ([\w\d:]+):::([\w\d]+)\(([\w\d:,]*)\)::([\w\d]+)$")
        
        return None
            
    def getswf(self):
        return self.__swf
    
    swf = property(getswf)