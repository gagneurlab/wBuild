# Use of native snakemake rules

Native snakemake rules can be defined in Snakefile in the project root directory. 

Here, we show one example of using shell command to download `iris.data` from web, save into `Data/iris_downloaded.data`. This file will then be served as input for script `020_Snakefile.R`

`Snakefile`:

```yaml
configfile: "wbuild.yaml"
include: ".wBuild/wBuild.snakefile"

rule all:
	input: rules.Index.output, "Output/html/readme.html"
	output: touch("Output/all.done")

rule downloadIris:
	output: 'Data/iris_downloaded.data'
	shell: "wget http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data > {output}"

```

# Specify snakemake options in `wb` block

One can also specify any snakemake options like `threads` in `wb` block and refere to them in the script. For instance, in script `020_Snakefile.R`, we specify 10 threads:

```
#' wb:
#'  input: 
#'  - iris: "Data/iris_downloaded.data"
#'  threads: 10
```

The specified variables can then be refered by name in the script: `snakemake@threads`.
