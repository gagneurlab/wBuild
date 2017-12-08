import os, sys
import pathlib
import re
#from matplotlib.cbook import iterable
import code
sys.path.insert(0, os.getcwd()+"/.wBuild")
from wbuild.wBUtils import *
htmlPath = "Output/html"

WB_FIELDS = {"type"}
# SNAKEMAKE  = ["input", "output", "threads"]
SNAKEMAKE_FIELDS = ["input",
                    "output",
                    "params",
                    "threads",
                    "resources",
                    "priority",
                    "version",
                    "log",
                    "message",
                    "run",
                    "shell",
                    "script"]

def writeDependencyFile():
    print("Updating dependencies...")
    wbData = getWBData()
    mdData = getMDData()
    with open('.wBuild.depend', 'w') as f:
        f.write('######\n')
        f.write('#This is a autogenerated snakemake file by wBuild\n')
        f.write('#wBuild by Leonhard Wachutka\n')
        f.write('######\n')

        # write rules
        for r in wbData:
            writeRule(r, f)
        # write md rules
        for r in mdData:
            writeMdRule(r, f)
                
        #write build index rule
        writeIndexRule(wbData,mdData, f)
    print("Done.\n")

def joinEmpty(string_list):
    # filter empty string list
    return ", ".join([x for x in string_list if x.strip() != ''])

def escapeSMString(item):
    if type(item) is dict:
        return str(list(item.keys())[0]) + ' = ' + escapeSMString(str(list(item.values())[0]))
    
    elif type(item) is str:
        if item.startswith("`sm ") and item.endswith("`"):
            return item[4:-1]
        return "'" + item + "'"
    return ''
def ensureString(elem):
    if elem is None:
        return ''
    elif type(elem) is list:
        if len(elem) == 0:
            return ''
        else:
            # make sure each element is a character
            elem = [escapeSMString(item) for item in elem]
            elem = [x for x in elem if str(x).strip() != '']
            
            return ", ".join(elem)
    elif type(elem) is str:
        if "," not in elem:
            return "'" + elem + "'"
        else:
            return elem
    else:
        raise TypeError("Don't know how to handle type: " + str(type(string_list)))

def dumpSMRule(dumpDic, file, sFile):
    if 'py' in dumpDic:
        code = dumpDic['py']
        if type(code) is str:
            file.write(insertPlaceholders(code,sFile))
        elif type(code) is list:
            [file.write(insertPlaceholders(line,sFile)+'\n') for line in code]
                
    file.write('rule ' + dumpDic['rule'] + ':\n')
    for field in SNAKEMAKE_FIELDS:
        if field in dumpDic:
            file.write('    ' + field +': '+str(dumpDic[field]) + '\n')
    
def insertPlaceholders(s, file):
    path = pathlib.Path(file)
    PD = pathlib.Path('Output/ProcessedData')
    
    PP = path.parts[-2]
    s = s.replace("{wbPD}",str(PD))
    s = s.replace("{wbPP}",str(PP))
    
    if len(path.parts) <= 2 and bool(re.search('{wbP(D_P*)?}', file)):
        print("If using placeholders please make sure you have the right",
        " directory structure.")
    
    if len(path.parts) > 2:
        P = path.parts[-3]
        s = s.replace("{wbPD_P}",str(PD/P))
        s = s.replace("{wbPD_PP}",str(PD/P/PP))
        s = s.replace("{wbP}",str(P))
    
    return s
    
        
def writeRule(r, file):
    # file needs wb to write to Snakefile
    if "wb" not in r["param"] or type(r["param"]['wb']) is not dict:
        return
    elem = r["param"]["wb"]

    # extract rule
    #rule = r['file'].replace('.','_').replace('/','_')

    # determine input, output and script
    elem["input"] = insertPlaceholders(joinEmpty([ensureString(elem.get("input")), "RScript = '" + r['file'] + "'"]), r['file'])
    if elem.get("type") == 'script':
        elem["output"] = insertPlaceholders(ensureString(elem.get("output")), r['file'])
        elem["script"] = '\'' + r['file'] + '\''  
    elif elem.get("type") == 'noindex':
        elem["output"] = insertPlaceholders(ensureString(elem.get("output")), r['file'])
        elem["script"] = "'.wBuild/wBRender.R'"
    else:
        elem["output"] = insertPlaceholders(joinEmpty([ensureString(elem.get("output")), "wBhtml = '" + r['outputFile'] + "'"]),r['file'])
        elem["script"] = "'.wBuild/wBRender.R'"
        
    # remove wb related elements
    #elem = {key: elem[key] for key in elem if key not in WB_FIELDS}
    #if not set(elem.keys()).issubset(SNAKEMAKE_FIELDS):
    #    Warning("File: {0}. The following fields don't correspond to any snakemake or wBuild tag: {1}"
    #            .format(r['file'], ",".join(set(elem.keys()).difference(SNAKEMAKE_FIELDS))))

    # remove fields not in SNAKEMAKE_FIELDS
    #elem = {key: elem[key] for key in elem if key in SNAKEMAKE_FIELDS}
    elem['rule'] = r['file'].replace('.','_').replace('/','_')
    # write to file
    file.write('\n')
    #dumpDict = {'rule ' + rule: elem}
    #file.write(yaml.dump(dumpDict, default_flow_style = False, indent=4).replace("\'\'\'", "'").replace("\'\'", "'"))
    dumpSMRule(elem,file,r['file'])
    file.write('\n')

def writeMdRule(r,file):
    file.write('\n')
    file.write('rule '+ r['file'].replace('.','_').replace('/','_') + ':\n')
    file.write('    input: "' + r['file'] +'"\n')
    file.write('    output: "' + r['outputFile'] +'"\n')
    file.write('    shell: "pandoc --from markdown --to html --toc --self-contained -s -o {output} {input}"\n')
    
    file.write('\n')
    
def writeIndexRule(rows,mdrows, file):
    inputFiles = []
    for r in rows:
        if getYamlParam(r,'type') == 'script' or getYamlParam(r,'type') == 'noindex':
            continue
        inputFiles.append(r['outputFile'])
    
    for r in mdrows:
        inputFiles.append(r['outputFile'])
     
    file.write('\n')
    file.write('rule Index:\n')
    file.write('    input: \n        "' + '",\n        "'.join(inputFiles)+ '"\n')
    file.write('    output: "' + htmlPath + '/index.html"\n')
    #file.write('    script: ".wBuild/createIndex.py"\n')
    file.write('    run:\n')
    file.write('        import wbuild.createIndex\n')
    file.write('        wbuild.createIndex.ci()\n')

    file.write('\n')

if __name__ == "__main__":
    writeDependencyFile()
