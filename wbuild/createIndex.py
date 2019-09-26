import os
import sys
import pathlib
import shutil
import wbuild

from string import Template
from os import listdir
from os.path import isfile, join
from wbuild.utils import parseWBInfosFromRFiles, parseMDFiles, \
        getYamlParam, Config, removeFilePrefix

sys.path.insert(0, os.getcwd() + "/.wBuild")  # TODO - is this line required?

def writeSubMenu(top, wbData, level):
    """
    Recursive call to construct the dropdown list and hover-over side-menus in it adhereing to a "top" toolbar category.

    :param top: "top" toolbar directory to be appointed to
    :param wbData: wb relevant data of all scanned files
    :param level: deepness of the current submenu (first dropdown list, then hover-over side-menus in the html)
    :return: deeply constructed dropdown list of the top toolbar category as an HTML string
    """
    
    menuString = ''
    temp = []
    newWb = []
    for r in wbData:
        temptemp = pathlib.PurePath(r['file']).parts[level - 1]
        if (pathlib.PurePath(r['file']).parts[level - 1] == top):
            # Is it a file
            if(len(pathlib.PurePath(r['file']).parts) == (level + 1)):
                if getYamlParam(r, 'type') != 'script' and getYamlParam(r, 'type') != 'noindex':
                    menuString += ('<li><a href="javascript:navigate(\'' +
                            pathlib.PurePath(r['outputFile']).name + '\');">' +
                            pathlib.PurePath(r['file']).parts[level] + '</a></li>\n')
                continue
            temp.append(pathlib.PurePath(r['file']).parts[level])
            newWb.append(r)
    
    temp = sorted(set(temp))
    for top in temp:
        menuString += '<li class="dropdown-submenu">\n'
        menuString += '    <a tabindex="-1" href="#">' + top + '</a>\n'
        menuString += '    <ul class="dropdown-menu">\n'
        menuString += '    ' + writeSubMenu(top, newWb, level + 1)
        menuString += '    </ul>\n'
        menuString += '</li>\n'
    return menuString


def getRecentMenu():
    """
    Support recently edited files list to the HTML web output.

    :return: HTML string: "Recently viewed" menu contents
    """
    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    rFiles = sorted([join(htmlOutputPath, f) for f in listdir(htmlOutputPath)
        if isfile(join(htmlOutputPath, f))], key=os.path.getmtime, reverse=True)
        
    ## delete all files containing the word "index from html menu "
    rFiles = [f for f in rFiles if "index" not in f]
    rFiles = rFiles[:10]

    # open recent Files in new tab 
    menuString = ""
    for f in rFiles:
        fo = pathlib.PurePath(f).name
        
        # Open in a new tab
        #menuString += ('<p><a href='+ fo + ' target="_blank">' + fo.replace('_', ' ').replace('.html', '') +
        #        '</a></p>\n')
        
        # Open in same tab
        menuString += ('<p><a href="javascript:navigate(\'' +
                fo + '\');" >' + fo.replace('_', ' ').replace('.html', '') +
                '</a></p>\n')
    return menuString

def writeReadme():
    """ Extract readme file from readme path in config. 
    If not specified file containing <readme> in scriptsPath with be chosen"""
      
    conf = Config()
    scriptsPath = conf.get("scriptsPath")
    snakeroot = conf.snakeroot
    
    try:
        filename_readme = conf.get("readmePath") #### should be .md file
    except AttributeError as e:
        filename_readme = ""
        onlyfiles = [f for f in os.listdir(snakeroot) if os.path.isfile(os.path.join(snakeroot, f))]
        for f in onlyfiles:
            if ("readme" in f) and f.endswith(".md"):
                filename_readme = f
    
    filename_readme = filename_readme.replace(".md", ".html")
    readmeString = '<li><a href="javascript:navigate(' + " '{}'".format(filename_readme) + ');">Readme</a></li> '
    readmeIframeString = '<iframe id="Iframe" src="' + filename_readme + '" width=100% height=95% ></iframe> '
    readmeFilename = ' "{}" '.format(filename_readme)
    
    return readmeString, readmeIframeString, readmeFilename           
        
def writeDepSVG():
    """ Search for rule graph. If path not specified in config, take default dep.svg in snakeroot path"""
    conf = Config()
    scriptsPath = conf.get("scriptsPath")
    htmlOutputPath = conf.get("htmlOutputPath")
    snakeroot = conf.snakeroot
    foldername = snakeroot.split("/")[-1]
    
    try:
        filename_SVG = conf.get("ruleGraphPath") #### should be .md file
    except AttributeError as e:
        ### try with default name "dep.svg"
        if os.path.isfile(os.path.join(htmlOutputPath, "dep.svg")):
            filename_SVG = "dep.svg"  
        else:
            ### search for files containing "svg" and foldername 
            filename_SVG = ""
            onlyfiles = [f for f in os.listdir(htmlOutputPath) if os.path.isfile(os.path.join(htmlOutputPath, f))]
            for f in onlyfiles:
                if (foldername in f) and f.endswith(".svg"):
                    filename_SVG = f
 
    svgString = '<li><a href="javascript:navigate(' + "'{}'".format(filename_SVG) + ');">Dependency</a></li>' 
    return svgString

def writeIndexHTMLMenu():
    """
    Scan for files involved in the current HTML rendering and fill the HTML quick access toolbar correspondingly
    """
    conf = Config()
    
    htmlOutputPath = conf.get("htmlOutputPath")
    scriptsPath = conf.get("scriptsPath")
    pageTitle = conf.get("projectTitle")
    snakeroot = conf.snakeroot

    wbData = parseWBInfosFromRFiles(script_dir=scriptsPath, htmlPath=htmlOutputPath)
    mdData = parseMDFiles(script_dir=scriptsPath, htmlPath=htmlOutputPath)
    wbData += mdData
    temp = []
    
    # for all of the scanned files, collect their paths
    for r in wbData:
        # this is needed so the relative path to "../wbuild/Snakefile" is not
        # part of the html sub menu
        r['file'] = removeFilePrefix(r['file'], snakeroot)
        temp.append(pathlib.PurePath(r['file']).parts[1])

    menuString = ""
    for top in sorted(set(temp)):
        menuString += (
            '<li class="dropdown">\n' +
            #write the current directory's name to the main ("top") toolbar tab
            '   <a href="#" class="dropdown-toggle" data-toggle="dropdown" ' +
                    'role="button" aria-haspopup="true" aria-expanded="false">' +
                    top + '<span class="caret"></span></a>\n'
            '   <ul class="dropdown-menu multi-level" role="menu">\n' +
            #write sub-directories to the dropdown list of the "top" tabs
            writeSubMenu(top, wbData, 2) +
            '   </ul>\n' +
            '</li>\n')
            
    readmeString, readmeIframeString, readmeFilename = writeReadme()
    depSVGString = writeDepSVG()
    
    #fill the HTML template with the constructed tag structure
    wbuildPath = pathlib.Path(wbuild.__file__).parent
    
    template = open(str(wbuildPath / "template.html")).read()
    template = Template(template).substitute(menu=menuString, title=pageTitle, rf=getRecentMenu(),
                        readme=readmeString, readmeIframe=readmeIframeString, readmeFilename=readmeFilename
                        , depSVG=depSVGString)
                        
                        
    try:
        filename_index = conf.get("htmlIndex")
    except AttributeError as e:
        filename_index = "index.html"
    
    try: 
        indexWithFolderName = conf.get("indexWithFolderName")
    except:
        indexWithFolderName = False
    
    if indexWithFolderName:
        abs_path = str(os.path.abspath(scriptsPath))
        name = abs_path.split("/")[-2]
        filename_index = name + "_" + filename_index
    
    f = open(htmlOutputPath + '/' + filename_index, 'w')
    f.write(template)
    f.close()


def ci():
    writeIndexHTMLMenu()

    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    libDir = htmlOutputPath + "/lib"

    if os.path.exists(libDir):
        shutil.rmtree(libDir)
    shutil.copytree('.wBuild/lib', libDir)
