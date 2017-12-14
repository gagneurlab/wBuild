import os
import sys
import pathlib
import shutil
from string import Template
from os import listdir
from os.path import isfile, join
from wbuild.utils import getWBData, getMDData, getYamlParam

sys.path.insert(0, os.getcwd() + "/.wBuild")  # TODO - is this line required?


htmlPath = "Output/html"


def writeSubMenu(top, wbData, level):
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
    menuString = ""
    htmlPath = "Output/html"
    rFiles = sorted([join(htmlPath, f) for f in listdir(htmlPath) if isfile(join(htmlPath, f))], key=os.path.getmtime, reverse=True)[:10]
    for f in rFiles:
        fo = pathlib.PurePath(f).name
        menuString += '<p><a href="javascript:navigate(\'' + fo + '\');">' + fo.replace('_', ' ').replace('.html', '') + '</a></p>\n'
    return menuString


def writeMenu():
    wbData = getWBData()
    mdData = getMDData()
    wbData += mdData
    menuString = ""
    temp = []
    for r in wbData:
        temp.append(pathlib.PurePath(r['file']).parts[1])
    temp = sorted(set(temp))
    for top in temp:
        menuString += '<li class="dropdown">\n'
        menuString += '   <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">' + top + '<span class="caret"></span></a>\n'
        menuString += '   <ul class="dropdown-menu multi-level" role="menu">\n'
        menuString += writeSubMenu(top, wbData, 2)
        menuString += '   </ul>\n'
        menuString += '</li>\n'
    template = open('.wBuild/template.html').read()
    template = Template(template).substitute(menu=menuString, title='title', rf=getRecentMenu())  # snakemake.config['projectTitle']

    f = open('Output/html/index.html', 'w')
    f.write(template)
    f.close()


def ci():
    writeMenu()

    libDir = "Output/html/lib"

    if os.path.exists(libDir):
        shutil.rmtree(libDir)
    shutil.copytree('.wBuild/lib', libDir)
