#'---
#' wb:
#'  py:
#'  - | 
#'   with open('Data/ids.txt') as f:
#'    ids = f.read().splitlines()
#'  input:
#'  - idslist: "Data/ids.txt"
#'  - columns: "`sm expand('Output/html/030_AnalysisOfId_{id}.html', id=ids)`"
#' output:
#'  html_document:
#'   code_folding: show
#'   code_download: TRUE
#'---

#py can be any valid python code. E.g. we explicitly state here the ids, instead of reading or get them from the config file
#`sm ...` is escape for snakemake syntax
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/050_PythonCode/040_IndexIDs.R")


# Ok now we need to show the ids
#' #Example of two links using markdown syntax
#' 
#' - [id1](030_AnalysisOfId_SepalLength.html)
#' - [id2](030_AnalysisOfId_SepalWidth.html)
#' 
#' #Here we create a dynamic datatable containing the links.
#' Needs DT and data.table to run

if(require(DT) & require(data.table))
{
	library(DT)
	library(data.table)
	ids = fread(snakemake@input[['idslist']],header=FALSE)
	ids[,link:=paste0('<a href="', '030_AnalysisOfId_',V1,'.html">',V1,'</a>')]
	datatable(ids,escape=FALSE,filter = 'top')
}
