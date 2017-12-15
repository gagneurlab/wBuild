#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  output: 
#'  - ids: "{wbPD_P}/ids.txt"
#'  type: script
#' output:
#'  html_document:
#'   code_folding: show
#'   code_download: TRUE
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/050_PythonCode/020_CreateIDs.R")

ids = c('SepalLength','SepalWidth','PetalLength','PetalWidth')
write.table(ids,snakemake@output[['ids']],row.names=FALSE,col.names=FALSE,quote=FALSE)
