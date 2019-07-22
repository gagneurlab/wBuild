library(stringr)
library(gsubfn)
parseWBHeader2 = function(file, wildcards = list(), debug = T)
{
	# Are we interactive or in real snakemake run?
	if(exists('snakemake')&&is.null(snakemake@config[['wbDump']]))
	{
		return (snakemake)
	}
	#' Create dependency file
	system2('python',c('.wBuild/wbParse.py',file))
	#' Replace wildcards if necessary
	if(length(wildcards)>0)
	{
		names(wildcards) = paste0('{',names(wildcards),'}')
		dependencyfile = readLines('.wBuild.depend')
		dependencyfile_wild  <- gsubfn('\\{[^\\}]+\\}', wildcards,dependencyfile)
		writeLines(dependencyfile_wild, con=".wBuild.depend")
	}
	#' Extract rule name (1st in file)
	dependencyfile = readLines('.wBuild.depend')
	rule_name = str_extract(dependencyfile,'(?<=rule )[A-z0-9_]*')
	rule_name = rule_name[!is.na(rule_name)][1]
	
	if(debug==T)
	{
		writeLines(dependencyfile)
	}
	#' Run snakemake to dump snakemake object, dumps some error yet
	system2('snakemake',c(rule_name,'--config','wbDump=T','--nolock','--latency-wait','0','-q','-F','--allowed-rules',rule_name,'--mode','2'))
	#' Read snakemake object in
	snakemake <<- readRDS('.wBuild/snakemake.dump')
}
#
#parseWBHeader2('Scripts/Analysis1/010_BasicInput/020_BasicInput.R',debug=F)
#parseWBHeader2(file ='Scripts/Analysis1/050_PythonCode/030_AnalysisTemplate.R',list(id='anton'))
#parseWBHeader2(file='Scripts/Analysis1/050_PythonCode/040_IndexIDs.R')

