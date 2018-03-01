# Input and Output, DAG

In this section, we show how to define input and output, to build [Snakemake DAG](http://snakemake.readthedocs.io/en/stable/tutorial/basics.html).

In file `020_InputOutput.R`, we define in the yaml header input as `iris` data, and output file name and path, refered as `pca`. `type:script` means wBuild will only excute the file if any of the output file is reqested, but do not render the file into a html format.

In file `030_VisualizePCA.R`, we are requesting the `pca` result that is computed from `020_InputOutput.R`, which means, file `030_VisualizePCA.R` is dependent on the result from `020_InputOutput.R`.
