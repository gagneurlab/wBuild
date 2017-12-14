#'---
#' title: Basic Input Output Demo
#' author: Leonhard Wachutka
#' wb:
#'  input: 
#'  - pca: "{wbPD_P}/pca.RDS"
#'---

source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/020_InputOutput/030_VisualizePCA.R")

##' ## Load pca data and visualize the first two principle components
pca <- wbReadRDS("pca")
plot(pca[, 1], pca[, 2], col = pca$Species)
