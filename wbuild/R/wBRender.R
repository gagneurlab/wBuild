#
# wBuild render script
# 

#require(knitrBootstrap)
require(knitr)
require(rmarkdown)
# default for knitr and rmarkdown
opts_knit$set(root.dir=getwd())
opts_chunk$set(echo=TRUE, message=FALSE, 
		error=FALSE, warning=FALSE, cache=FALSE)

# TODO could be an option in the wbuild.yaml
options(width=120)
wBuildPath = snakemake@config[['wBuildPath']]
source(paste0(wBuildPath, "/R/render_child.R"))
source(paste0(wBuildPath, "/R/rmarkdown_show_hide_table.R"))

# create tmp folder and tmp output folder
intermediates_dir <- tempfile()
tmp_output_dir <- tempfile()
i <- dir.create(intermediates_dir, showWarnings=FALSE)
i <- dir.create(tmp_output_dir, showWarnings=FALSE)

# copy needed files over
file.copy(paste0(wBuildPath,"/html/lib"), file.path(tmp_output_dir), recursive=TRUE)

# get snakemake input
file_input <- snakemake@input[['RScript']]
file_output <- snakemake@output[['wBhtml']]


sFile <- tempfile()
spin_input <- readChar(file_input, file.info(file_input)$size)
write(spin(text=spin_input, knit=FALSE), sFile)
kProcessor <- default_output_format(sFile)

# add needed default based on the document type
if (kProcessor$name == "html_document"){
	libPath <- file.path(tmp_output_dir, "libR")
	
	kProcessor$options$code_folding = ifelse(
			is.language(kProcessor$options$code_folding), 
			"hide", kProcessor$options$code_folding)
	kProcessor$options$toc <- TRUE
	kProcessor$options$toc_float <- TRUE
	kProcessor$options$fig_retina <- NULL
	kProcessor$options$self_contained <- FALSE
	kProcessor$options$lib_dir <- libPath
	kProcessor$options$css <- c('lib/add_content_table.css', 'lib/leo_style.css')
    kProcessor$options$df_print <- 'tibble'
}else{
	require(knitrBootstrap)
}
format <- do.call(eval(parse(text=kProcessor$name)), kProcessor$options)

# render it to the tmp folder
render(file_input, output_dir=tmp_output_dir, clean=TRUE,
		intermediates_dir=intermediates_dir, output_file=basename(file_output),
		output_format=format)

# copy it to the output directory
file.copy(list.files(tmp_output_dir, full.names=TRUE),
		dirname(file_output), overwrite=TRUE, recursive=TRUE)


