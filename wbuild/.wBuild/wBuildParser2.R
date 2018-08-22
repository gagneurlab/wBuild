library(stringr)
parseWBHeader2 = function(file,wildcards, debug = T)
{
	system2('python',c('.wBuild/wbParse.py',file))
	dependencyfile = readLines('.wBuild.depend')
	rule_name = str_extract(dependencyfile,'(?<=rule )[A-z0-9_]*')
	rule_name = rule_name[!is.na(rule_name)][1]
	
	if(debug==T)
	{
		writeLines(dependencyfile)
	}
	system2('snakemake',c(rule_name,'--config','wbDump=T','--nolock','--latency-wait','0','-q','-F','--allowed-rules',rule_name,'--mode','2'))
	snakemake <<- readRDS('.wBuild/snakemake.dump')
	
}

parseWBHeader2('Scripts/Analysis1/010_BasicInput/020_BasicInput.R')
parseWBHeader2('Scripts/Analysis1/050_PythonCode/030_AnalysisTemplate.R')
parseWBHeader2(file='Scripts/Analysis1/050_PythonCode/040_IndexIDs.R')