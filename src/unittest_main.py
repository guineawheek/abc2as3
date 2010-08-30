'''
Created on Aug 28, 2010

@author: Aaron Cooper
'''

import os
import unittest
import sys

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    files = os.listdir(path + "/unit_tests")
    
    runner = unittest.TextTestRunner();
    loader = unittest.TestLoader()
    
    for file in files:
        if file.lower().endswith('test.py'):
            moduleName = file.split('.')[0]
            mod = my_import('unit_tests.' + moduleName)
            suite = loader.loadTestsFromModule(mod)
            runner.run(suite)