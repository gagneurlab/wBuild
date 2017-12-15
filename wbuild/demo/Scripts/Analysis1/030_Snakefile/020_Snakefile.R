#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka, Jun Cheng
#' wb:
#'  input: 
#'  - iris: "Data/iris_downloaded.data"
#'  threads: 10
#' output:
#'  html_document:
#'   code_folding: show
#'   code_download: TRUE
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/030_Snakefile/020_Snakefile.R")

read.csv(snakemake@input[['iris']])

message('We run on', snakemake@threads, 'threads')
