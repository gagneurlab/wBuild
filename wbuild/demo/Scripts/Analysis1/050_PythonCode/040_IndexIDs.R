#'---
#' wb:
#'  py:
#'  - | 
#'   with open('Data/ids.txt') as f:
#'    ids = f.read().splitlines()
#'  input:
#'  - idslist: "Data/ids.txt"
#'  - columns: "`sm expand('Output/html/030_AnalysisOfId_{id}.html', id=ids)`"
#'---

#py can be any valid python code. E.g. we explicitly state here the ids, instead of reading or get them from the config file
#`sm ...` is escape for snakemake syntax


# Ok now we need to show the ids
#' #Example of two links using markdown syntax
#' 
#' - [id1](030_AnalysisOfId_SepalLength.html)
#' - [id2](030_AnalysisOfId_SepalWidth.html)

#maybe also show how to read in the ids.txt and create the links programticaly
#I use for e.g.

#ig = fread(snakemake@input[['ids']],header=FALSE)
#tbl2 = data.table(ig)
#tbl2[,link:=href("030_AnalysisOfId_",V1,'.html',name=V1,blank=FALSE)]
#datatable(tbl2,escape=FALSE,filter = 'top')
