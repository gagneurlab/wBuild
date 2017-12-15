#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - iris: "Data/{wbP}/iris.RDS"
#'  output:
#'  - wBhtml: "Output/html/030_AnalysisOfId_{id}.html"
#'  type: noindex
#' output:
#'  html_document:
#'   code_folding: show
#'   code_download: TRUE
#'---

#important :Output has to be called wBhtml
#type: noindex
# id='SepalLength'
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/050_PythonCode/030_AnalysisTemplate.R")

id = snakemake@wildcards[["id"]]
iris_df = wbReadRDS('iris')
colnames(iris_df) = gsub('\\.','',colnames(iris_df))

hist(iris_df[[id]],main=id)
