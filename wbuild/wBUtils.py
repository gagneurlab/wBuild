import fnmatch
import os
import yaml
import pathlib
import operator
from functools import reduce
#from datashape.coretypes import Null

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def findFiles(patterns):  
    matches = []
    for root, dirnames, filenames in os.walk('Scripts'):
        dirnames[:] = [d for d in dirnames if not d[0] == '_']
        dirnames[:] = [d for d in dirnames if not d[0] == '.']
        for filename in reduce(operator.add,(fnmatch.filter(filenames, p) for p in patterns)):
            matches.append(os.path.join(root, filename))
    return sorted(matches)

def findFilesPath(path, patterns):  
    matches = []
    for root, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if not d[0] == '_']
        dirnames[:] = [d for d in dirnames if not d[0] == '.']
        for filename in reduce(operator.add,(fnmatch.filter(filenames, p) for p in patterns)):
            matches.append(os.path.join(root, filename))
    return sorted(matches)

def getSpinYaml(file):
    yamlHeader = []
    for line in open(file):
        li=line.strip()
        if li.startswith("#'"):
             yamlHeader.append(li[2:])
    return '\n'.join(yamlHeader)

def checkYamlHeader(file):
    line = open(file).readline()
    if(line.startswith("#'---")):
        return True
    return False

def getWBData():
    out = []
    htmlPath = "Output/html"
    error = False
    for f in findFiles(['*.r','*.R']):
        
        try:
            if checkYamlHeader(f)== False:
                continue
            param = next(yaml.load_all(getSpinYaml(f)))
        except:
            # TODO - create more verbose output for parsing errors
            if error == False:
                print(bcolors.FAIL + bcolors.BOLD + 'Could not parse', f, '. Include valid yaml header. Omitting further errors of same kind.\n'+ bcolors.ENDC) 
                error = True
            continue
        if('wb' in param):
            outFile = htmlPath + "/" + os.path.splitext(f)[0].replace('/','_') +".html"
            out.append({'file': f, 'outputFile':outFile, 'param': param})        
    return out

def getMDData():
    out = []
    htmlPath = "Output/html"
    for f in findFiles(['*.md']):
        outFile = htmlPath + "/" + os.path.splitext(f)[0].replace('/','_') +".html"
        out.append({'file': f, 'outputFile':outFile, 'param':[]})
    return out

def getYamlParam(r,paramName):
    if 'wb' in r['param'] and type(r['param']['wb']) is dict and paramName in r['param']['wb']:
        return r['param']['wb'][paramName]
    return None
