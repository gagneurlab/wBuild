import sys
import wbuild
import wbuild.scanFiles
import wbuild.autolink

htmlOutputPath = config["htmlOutputPath"] if config["htmlOutputPath"] != None else "Output/html"

if not '--dag' in sys.argv and not any("snakemake-bash-completion" in s for s in sys.argv):
    wbuild.scanFiles.writeDependencyFile()

include: "../.wBuild.depend"

rule show:
    input: htmlOutputPath + "/all.done"
    shell: "google-chrome Output/html/index.html &"

rule mapScripts:
    input: "scriptMapping.wb"
    output: touch(htmlOutputPath + "../scriptMapping.done")
    run:
        wbuild.autolink.autolink("scriptMapping.wb")

rule graph:
    shell: "snakemake --dag | dot -Tsvg -Grankdir=LR > " + htmlOutputPath + "/dep.svg"

rule clean:
    shell: "rm -R "+ htmlOutputPath+ "* || true && rm .wBuild.depend || true && rm -R .wBuild/__pycache__ || true "

rule publish:
    input: htmlOutputPath + "../all.done"
    shell: "rsync -Ort " + htmlOutputPath + " {config[webDir]}"

rule markdown:
    input: "{file}.md"
    output: htmlOutputPath + "/{file}.html"
    shell: "pandoc --from markdown --to html --css .wBuild/lib/github.css --toc --self-contained -s -o {output} {input}"

