#'---
#' title: Basic Input Demo
#' author: Leonhard Wachutka, Jun Cheng
#' wb:
#'  input: 
#'  - iris: "Data/{wbP}/iris.RDS"
#'  output:
#'  - pca: "{wbPD_P}/pca.RDS"
#' type: script
#'---
source('.wBuild/wBuildParser.R')
parseWBHeader("Scripts/Analysis1/020_InputOutput/020_InputOutput.R")

# state that script is optional. Only necessary if one does not want to create a hmtl of this file

iris_df <- wbReadRDS('iris')

##' ## PCA analysis of iris
# log transform 
log.ir <- log(iris_df[, 1:4])
ir.species <- iris_df[, 5]
 
# apply PCA - scale. = TRUE is highly 
# advisable, but default is FALSE. 
ir.pca <- prcomp(log.ir,
                 center = TRUE,
                 scale. = TRUE) 

pca <- as.matrix(log.ir) %*% ir.pca$rotation
pca <- as.data.frame(pca)
pca$Species <- iris_df$Species

wbSaveRDS(pca, 'pca')

