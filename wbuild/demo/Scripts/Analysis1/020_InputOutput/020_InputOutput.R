#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - iris: "Data/{wbP}/iris.RDS"
#'  output:
#'  - pca: " {wbPD_P}/pca.RDS"
#' type: script
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/020_InputOutput/020_InputOutput.R")

#state that script is optional. Only necessary if one does not want to create a hmtl of this file

wbReadRDS('iris')
#do pca of iris


#pca = pca(iris)
#wbSaveRDS(pca,'pca')

