#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  output: 
#'  - ids: "{wbPD_P}/ids.txt"
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/050_PythonCode/020_CreateIDs.R")

ids = c('col1','col2','col3')
write.table(ids,snakemake@output[['ids']])

