import sys
import json
import wbuild
import wbuild.scanFiles
import wbuild.autolink

if not '--dag' in sys.argv and not any("snakemake-bash-completion" in s for s in sys.argv):
    depFile = wbuild.scanFiles.writeDependencyFile()

include: depFile

if "htmlIndex" not in config:
    config["htmlIndex"] = "index.html"
if "allDone" not in config:
    config["allDone"] = "Output/all.done"
htmlOutputPath = config["htmlOutputPath"]


rule show:
    input: config["allDone"]
    shell: "google-chrome {config[htmlOutputPath]}/{config[htmlIndex]} &"

rule mapScripts:
    input: "scriptMapping.wb"
    output: touch("Output/scriptMapping.done")
    run:
        wbuild.autolink.autolink("scriptMapping.wb")

def get_index_html(wildcards):
    filename = "_".join([wildcards.subindex, config["htmlIndex"]])
    return os.path.join(htmlOutputPath, filename)

# could remove?
rule graph_single:
    input: get_index_html
    output: htmlOutputPath + "/{subindex}_dep.{ext}"
    shell:
        """
        snakemake --rulegraph {input} | sed -ne '/digraph snakemake_dag/,/}}/p' | dot -T{wildcards.ext} -Grankdir=LR > {output}
        """

# obsolete
rule graph:
    input: config["htmlOutputPath"] + "/dep.svg"
    #shell: "snakemake --rulegraph | sed -ne '/digraph snakemake_dag/,/}}/p' | dot -Tsvg -Grankdir=LR > {output}"

rule clean:
    shell: "rm -Rf {config[htmlOutputPath]}* .wBuild/__pycache__"

rule publish:
    input: config["allDone"]
    shell: "rsync -Ort {config[htmlOutputPath]} {config[webDir]}"

rule markdown:
    input: "{file}.md"
    output: expand("{htmlOutputPath}/{{file}}.html", htmlOutputPath = config["htmlOutputPath"])
    shell: "pandoc --from markdown --to html --css {config[wBuildPath]}/html/lib/github.css --toc --self-contained -s -o {output} {input}"

rule restoreModDate:
    shell: "find -type f -exec touch -r {} +"
