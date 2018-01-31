import fnmatch
import os
import yaml
import yaml.scanner
import yaml.parser
import yaml.error
import operator
from functools import reduce
import wbuild.cli

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def checkFilename(filename):
    """
    :param filename: to check
    :return: has appropriate name?
    :raises: ValueError if the name is inappropriate
    """
    if " " in filename:
        raise ValueError("Spaces are not allowed in the filenames. File: {0}",filename)
    if "-" in os.path.basename(filename):
        raise ValueError("- are not allowed in the filenames. File: {0}", filename)
    return True

def findFilesRecursive(startingPath, patterns):
    """
    :param startingPath: root path of the search
    :param patterns: patterns to search file names for
    :return: paths to files matching the patterns
    """
    matchedFilepaths = []
    for root, dirnames, filenames in os.walk(startingPath):
        dirnames[:] = [d for d in dirnames if not d[0] == '_']
        dirnames[:] = [d for d in dirnames if not d[0] == '.']
        for file in reduce(operator.add, (fnmatch.filter(filenames, p) for p in patterns)):
            checkFilename(file)
            absFilepath = os.path.join(root, file)
            if not absFilepath in matchedFilepaths:
                matchedFilepaths.append(absFilepath)
    sortedMatchedFilepaths = sorted(matchedFilepaths)
    print("Found files in scope of wBuild: ", sortedMatchedFilepaths)
    return sortedMatchedFilepaths


def parseYAMLHeader(filepath):
    """

    :param filepath: path to the file
    :return: String representation of the YAML header in the file, including inter-document framing ("---")
    """
    yamlHeader = []
    for i, line in enumerate(open(filepath).readlines()):
        # process
        yamlHeader.append(line.strip()[2:])

        # terminate if that's already "#'---" (=end of YAML-designated area)
        if i != 0 and line.startswith("#'---"):
            break

    result = '\n'.join(yamlHeader)
    print("Got ", result, "as a result of parsing YAML header from ", filepath, ".")
    return result


def hasYAMLHeader(filepath):
    """
    :param filepath: path to the file
    :return: file contains YAML header?
    """
    with open(filepath, "r") as f:
        lines = f.readlines()
    line = lines[0]
    if(line.startswith("#'---")):
        return True
    print("The file" + filepath + "doesn't contain YAML header at the very beginning of the document and so was ignored.")
    return False


def parseWBInfosFromRFiles(script_dir="Scripts", htmlPath="Output/html"):
    """

    :param script_dir: Relative path to the Scripts directory
    :param htmlPath: Relative path to the html output path
    :return: a list of dictionaries with fields:
      - file - what is the input R file
      - outputFile - there to put the output html file
      - param - parsed yaml params
    """
    parsedInfos = []
    #errorOccured = False
    for filename in findFilesRecursive(script_dir, ['*.r', '*.R']):
        if not hasYAMLHeader(filename):
            # Ignore files without YAML infos
            continue
        header = parseYAMLHeader(filename)
        # run all the synthax checks - will raise an error if it fails
        yamlParamsDict = parseYamlParams(header, filename)
        if yamlParamsDict == None: #parsing error occured
            errorOccured = True
            continue #go on parsing next file


        if type(yamlParamsDict) is str: #allow parsing one tag without double points as string; put it in a dict and check later on
            yamlParamsDict = {yamlParamsDict: None}

        if('wb' in yamlParamsDict):# the header contains wb informations
            outFile = htmlPath + "/" + os.path.splitext(filename)[0].replace('/', '_') + ".html"
            parsedInfos.append({'file': filename, 'outputFile': outFile, 'param': yamlParamsDict})

    print("Parsed informations from R files: ", str(parsedInfos))
    #if errorOccured:
    #    raise ValueError("Errors occured in parsing the R files. Please fix them.") TODO really raise a ValueError?
    return parsedInfos



def parseMDFiles(script_dir="Scripts", htmlPath="Output/html"):
    """

    :param script_dir: Relative path to the Scripts directory
    :param htmlPath: Relative path to the html output path
    :return: a list of dictionaries with fields:
      - file - what is the input .md file
      - outputFile - there to put the output html file
      - param - parsed yaml header - always an empty list
    """
    print("Finding .md files:\n")
    foundMDFiles = []
    for f in findFilesRecursive(script_dir, ['*.md']):
        outFile = htmlPath + "/" + os.path.splitext(f)[0].replace('\\', '/') + ".html"
        print("Found ", outFile, ".\n")
        f = f.replace('\\', '/')
        foundMDFiles.append({'file': f, 'outputFile': outFile, 'param': []})
    print(".md files search finished\n\n")
    return foundMDFiles


def getYamlParam(r, paramName):
    if 'wb' in r['param'] and type(r['param']['wb']) is dict and paramName in r['param']['wb']:
        foundParam = r['param']['wb'][paramName]
        print("Got YAML param: ", foundParam)
        return foundParam
    return None

def parseYamlParams(header, f):
    """
    :param header: String form of YAML header
    :param f: Filename of a file from where the header was parsed
    :return: Parameters dictionary parsed from the header; None if parsing errors occured
    """
    try:
        param = next(yaml.load_all(header))
    except (yaml.scanner.ScannerError, yaml.parser.ParserError, yaml.error.YAMLError, yaml.error.MarkedYAMLError) as e:
        if hasattr(e, 'problem_mark'):
            if e.context != None:
                print('Error while parsing YAML area in the file ' + f + ':\n' + str(e.problem_mark) + '\n  ' +
                      str(e.problem) + ' ' + str(e.context) +
                      '\nPlease correct the header and retry.')
            else:
                print('Error while parsing YAML area in the file ' + f + ':\n' + str(e.problem_mark) + '\n  ' +
                      str(e.problem) + '\nPlease correct the header and retry.')
        else:
            print("YAMLError parsing yaml file.")

        return None
    except Exception as e:
        print(bcolors.FAIL + bcolors.BOLD + 'Could not parse', f,
              '. Include valid yaml header. Not showing any further errors. \n',
              'Errors {0}'.format(e) + bcolors.ENDC)
        return None

    print("Parsed params: ", str(param))
    return param

def pathsepsToUnderscore(systemPath):
    """Convert all system path separators to underscores. Product is used as a unique ID for rules in scanFiles.py"""
    return systemPath.replace('.', '_').replace('/', '_').replace('\\', '_')
