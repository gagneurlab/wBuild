#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - iris: "Data/iris_downloaded.data"
#' 	threads: 10
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/030_Snakefile/020_Snakefile.R")


#shows how to preprocess data, e.g. wget
#readTable(snakemake@input[['iris']])

# you can also specify any snakemake options like threads and access them

message('We run on', snakemake@threads, 'threads')
#wbReadRDS('iris')
#plot(iris)
#' #show some markdown features here.

