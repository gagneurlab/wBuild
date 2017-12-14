import fnmatch
import os
import yaml
import operator
from functools import reduce
from wbuild.syntaxCheckers import checkHeaderSynthax


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def checkFileName(filename):
    """List of checks for the correct filename
    """
    if " " in filename:
        raise ValueError("Space not allowed in the filenames. File: {0}".filename)
    if "-" in os.path.basename(filename):
        raise ValueError("- not allowed in the filenames. File: {0}".filename)


def findFilesPath(path, patterns):
    """Recursively search for files following a certain pattern
    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if not d[0] == '_']
        dirnames[:] = [d for d in dirnames if not d[0] == '.']
        for filename in reduce(operator.add, (fnmatch.filter(filenames, p) for p in patterns)):
            checkFileName(filename)
            matches.append(os.path.join(root, filename))
    return sorted(matches)


def getSpinYaml(file):
    """Retrieves the yaml header (including)
    """
    yamlHeader = []
    for i, line in enumerate(open(file)):
        # first line has to start with #'---
        if i == 0 and not line.startswith("#'---"):
            raise ValueError("First line of the file should be equal to \"#'---\" ")

        # process
        li = line.strip()
        if li.startswith("#'"):
            yamlHeader.append(li[2:])

        # terminate on the second occurence of #'---
        if i != 0 and line.startswith("#'---"):
            break

    return '\n'.join(yamlHeader)


def checkYamlHeader(file):
    """Check the yaml header for synthax checks
    """
    with open(file, "r") as f:
        line = f.readline()
    if(line.startswith("#'---")):
        return True
    return False


def getWBData(script_dir="Scripts", htmlPath="Output/html"):
    """Parse all the R files

    Args:
      script_dir: Relative path to the Scripts directory
      htmlPath: Relative path to the html output path

    Returns:
      a list of dictionaries with fields:
      - file - what is the input R file
      - outputFile - there to put the output html file
      - param - parsed yaml header
    """
    out = []
    error = False
    for f in findFilesPath(script_dir, ['*.r', '*.R']):
        try:
            if not checkYamlHeader(f):
                # Ignore files not starting with
                continue
            header = getSpinYaml(f)
            # run all the synthax checks - will raise an error if it fails
            checkHeaderSynthax(header)
            param = next(yaml.load_all(header))
        except Exception as e:
            if not error:
                print(bcolors.FAIL + bcolors.BOLD + 'Could not parse', f,
                      '. Include valid yaml header. Not showing any further errors. \n',
                      'Errors {0}'.format(e) + bcolors.ENDC)
                error = True
            continue
        if('wb' in param):
            outFile = htmlPath + "/" + os.path.splitext(f)[0].replace('/', '_') + ".html"
            out.append({'file': f, 'outputFile': outFile, 'param': param})
    if error:
        raise ValueError("Errors occured in parsing the R files. Please fix them.")
    return out


def getMDData(script_dir="Scripts", htmlPath="Output/html"):
    """Parse all the .md files

    Args:
      script_dir: Relative path to the Scripts directory
      htmlPath: Relative path to the html output path

    Returns:
      a list of dictionaries with fields:
      - file - what is the input .md file
      - outputFile - there to put the output html file
      - param - parsed yaml header - always an empty list
    """
    out = []
    for f in findFilesPath(script_dir, ['*.md']):
        outFile = htmlPath + "/" + os.path.splitext(f)[0].replace('/', '_') + ".html"
        out.append({'file': f, 'outputFile': outFile, 'param': []})
    return out


def getYamlParam(r, paramName):
    if 'wb' in r['param'] and type(r['param']['wb']) is dict and paramName in r['param']['wb']:
        return r['param']['wb'][paramName]
    return None
