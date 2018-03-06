import sys
import wbuild
import wbuild.scanFiles
import wbuild.autolink

if not '--dag' in sys.argv and not any("snakemake-bash-completion" in s for s in sys.argv):
    wbuild.scanFiles.writeDependencyFile()

include: "../.wBuild.depend"

rule show:
    input: "Output/all.done"
    shell: "google-chrome {config[htmlOutputPath]}/index.html &"

rule mapScripts:
    input: "scriptMapping.wb"
    output: touch("Output/scriptMapping.done")
    run:
        wbuild.autolink.autolink("scriptMapping.wb")

rule graph:
    shell: "snakemake --dag | dot -Tsvg -Grankdir=LR > {config[htmlOutputPath]}/dep.svg"

rule clean:
    shell: "rm -R {config[htmlOutputPath]}* || true && rm .wBuild.depend || true && rm -R .wBuild/__pycache__ || true "

rule publish:
    input: "Output/all.done"
    shell: "rsync -Ort {config[htmlOutputPath]} {config[webDir]}"

rule markdown:
    input: "{file}.md"
    output: expand("{htmlOutputPath}/{{file}}.html", htmlOutputPath = config["htmlOutputPath"])
    shell: "pandoc --from markdown --to html --css .wBuild/lib/github.css --toc --self-contained -s -o {output} {input}"

