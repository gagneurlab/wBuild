import sys
import wbuild
import wbuild.scanFiles
if not '--dag' in sys.argv and not any("snakemake-bash-completion" in s for s in sys.argv):
    wbuild.scanFiles.writeDependencyFile()    

include: "../.wBuild.depend"

rule show:
	input: "Output/all.done"
	shell: "google-chrome Output/html/index.html &"

rule graph:
	shell: "snakemake --dag | dot -Tsvg -Grankdir=LR > Output/html/dep.svg"

rule clean:
	shell: "rm -R Output/html/* || true && rm .wBuild.depend || true && rm -R .wBuild/__pycache__ || true "
	
rule publish:
	input: "Output/all.done"
	shell: "rsync -rt Output/html/ {config[webDir]}"

rule markdown:
	input: "{file}.md"
	output: "Output/html/{file}.html"
	shell: "pandoc --from markdown --to html --toc -s -o {output} {input}"
	
