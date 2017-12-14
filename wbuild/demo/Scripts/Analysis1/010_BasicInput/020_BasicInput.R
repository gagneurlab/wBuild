#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - iris: "Data/{wbP}/iris.RDS"
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/010_BasicInput/020_BasicInput.R")

# wbReadRDS is a readRDS command that aware of inputs by referring to their names 
wbReadRDS('iris')
plot(iris)
#' #show some markdown features here.
