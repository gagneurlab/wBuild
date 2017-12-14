#'---
#'  py:
#'  - | 
#'   with open('{wbPD_P}/ids.txt') as f:
#'    ids = f.read().splitlines()
#'  input:
#'  - ids: "{wbPD_P}/ids.txt"
#'  - genes2: "`sm expand('Output/html/030_AnalysisOfId_{id}.html', id=ids)`"
#'---

#py can be any valid python code. E.g. we explicitly state here the ids, instead of reading or get them from the config file
#`sm ...` is escape for snakemake syntax


# Ok now we need to show the ids

#' -[id1](Output/html/030_AnalysisOfId_id1.html)
#' -[id2](Output/html/030_AnalysisOfId_id2.html)

#maybe also show how to read in the ids.txt and create the links programticaly
#I use for e.g.

#ig = fread(snakemake@input[['ids']],header=FALSE)
#tbl2 = data.table(ig)
#tbl2[,link:=href("030_AnalysisOfId_",V1,'.html',name=V1,blank=FALSE)]
#datatable(tbl2,escape=FALSE,filter = 'top')
