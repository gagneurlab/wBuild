import os
import sys
import pathlib
import shutil
from string import Template
from os import listdir
from os.path import isfile, join
from wbuild.utils import parseWBInfosFromRFiles, parseMDFiles, getYamlParam, Config

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
        if (pathlib.PurePath(r['file']).parts[level - 1] == top):
            # Is it a file
            if(len(pathlib.PurePath(r['file']).parts) == (level + 1)):
                if getYamlParam(r, 'type') != 'script' and getYamlParam(r, 'type') != 'noindex':
                    menuString += '<li><a href="javascript:navigate(\'' + pathlib.PurePath(r['outputFile']).name + '\');">' + pathlib.PurePath(r['file']).parts[level] + '</a></li>\n'
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
    menuString = ""
    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    rFiles = sorted([join(htmlOutputPath, f) for f in listdir(htmlOutputPath) if isfile(join(htmlOutputPath, f))], key=os.path.getmtime, reverse=True)[:10]
    for f in rFiles:
        fo = pathlib.PurePath(f).name
        menuString += '<p><a href="javascript:navigate(\'' + fo + '\');">' + fo.replace('_', ' ').replace('.html', '') + '</a></p>\n'
    return menuString


def writeIndexHTMLMenu():
    """
    Scan for files involved in the current HTML rendering and fill the HTML quick access toolbar correspondingly
    """
    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    scriptsPath = conf.get("scriptsPath")
    wbData = parseWBInfosFromRFiles(script_dir= scriptsPath, htmlPath=htmlOutputPath)
    mdData = parseMDFiles(script_dir=scriptsPath, htmlPath=htmlOutputPath)
    wbData += mdData
    menuString = ""
    temp = []
    for r in wbData: #for all of the scanned files, collect their paths
        temp.append(pathlib.PurePath(r['file']).parts[1])
    temp = sorted(set(temp))
    for top in temp:
        menuString += '<li class="dropdown">\n'
        #write the current directory's name to the main ("top") toolbar tab
        menuString += '   <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">' + top + '<span class="caret"></span></a>\n'
        menuString += '   <ul class="dropdown-menu multi-level" role="menu">\n'
        #write sub-directories to the dropdown list of the "top" tabs
        menuString += writeSubMenu(top, wbData, 2)
        menuString += '   </ul>\n'
        menuString += '</li>\n'
    #fill the HTML template with the constructed tag structure
    template = open('.wBuild/template.html').read()
    template = Template(template).substitute(menu=menuString, title='title', rf=getRecentMenu())  # snakewbuild.yaml['projectTitle']

    f = open(htmlOutputPath + '/index.html', 'w')
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
