#'---
#' title: Basic Input Output Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - pca: "{wbPD_P}/pca.RDS"
#' output:
#'  html_document:
#'   code_folding: show
#'   code_download: TRUE
#'---

# The following two commands make it possible to run wbReadRDS or snakemake@inputs
# while running in the interactive R session (say in RStudio)
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/020_InputOutput/030_VisualizePCA.R")

##' ## Load pca data and visualize the first two principle components
pca <- wbReadRDS("pca") # shorthand for readRDS(snakemake@input[["pca"]])
plot(pca[, 1], pca[, 2], col = pca$Species)
