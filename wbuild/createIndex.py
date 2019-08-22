import os
import sys
import pathlib
import shutil
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
    
    print("Hello from writeSubMenu with top: ", top, "wbData", wbData, "level", level)
    menuString = ''
    temp = []
    newWb = []
    for r in wbData:
        temptemp = pathlib.PurePath(r['file']).parts[level - 1]
        if (pathlib.PurePath(r['file']).parts[level - 1] == top):
            # Is it a file
            print(len(pathlib.PurePath(r['file']).parts))
            if(len(pathlib.PurePath(r['file']).parts) == (level + 1)):
                if getYamlParam(r, 'type') != 'script' and getYamlParam(r, 'type') != 'noindex':
                    menuString += ('<li><a href="javascript:navigate(\'' +
                            pathlib.PurePath(r['outputFile']).name + '\');">' +
                            pathlib.PurePath(r['file']).parts[level] + '</a></li>\n')
                continue
            print(pathlib.PurePath(r['file']).parts)
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
    rFiles = rFiles[:10]

    # open recent Files in new tab 
    menuString = ""
    for f in rFiles:
        fo = pathlib.PurePath(f).name
        menuString += ('<p><a href="javascript:navigate(\'' +
                fo + '\');">' + fo.replace('_', ' ').replace('.html', '') +
                'target="_blank" </a></p>\n')
    return menuString


def writeIndexHTMLMenu():
    """
    Scan for files involved in the current HTML rendering and fill the HTML quick access toolbar correspondingly
    """
    print("[INFO] Hello from writeIndexHTMLMenu")
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
        print("Start with top",top)
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
        print("Done with top",top)

    #fill the HTML template with the constructed tag structure
    template = open('.wBuild/template.html').read()
    template = Template(template).substitute(menu=menuString, title=pageTitle, rf=getRecentMenu())  # snakewbuild.yaml['projectTitle'] , 

    try:
        filename_index = conf.get("htmlIndex")
    except AttributeError as e:
        filename_index = "index.html"
    
    try: 
        indexWithFolderName = conf.get("indexWithFolderName")
    except:
        indexWithFolderName = False
    
    if indexWithFolderName:
        print("Set index with foldername in createIndex")
        abs_path = str(os.path.abspath(scriptsPath))
        print("AbsolutePath", abs_path)
        name = abs_path.split("/")[-2]
        filename_index = name + "_" + filename_index
    
    print("[INFO from createIndex] Index filename", filename_index)
    f = open(htmlOutputPath + '/' + filename_index, 'w')
    print(htmlOutputPath + '/' + filename_index)
    f.write(template)
    f.close()
    print("Done")

def ci():
    writeIndexHTMLMenu()

    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    libDir = htmlOutputPath + "/lib"

    if os.path.exists(libDir):
        shutil.rmtree(libDir)
    shutil.copytree('.wBuild/lib', libDir)
