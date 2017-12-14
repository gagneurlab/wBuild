#'---
#' title: Report 1
#' author: Leonhard Wachutka
#' wb:
#'  py:
#'  - test = [1,4]
#'  output: 
#'  - out: "Data/data.RDS"
#'  - outl: "`sm expand('Data/{dataset}.A.txt', dataset=test)`" 
#'  type: script
#'  threads: 8
#' output:
#'  knitrBootstrap::bootstrap_document
#'---

message('Threads: ', snakemake@threads)
message('input: ',str(snakemake@input))
message('output: ',str(snakemake@output),'\n')

message(snakemake@output[['out']])
message(snakemake@output[['outl']])

parallel::mclapply(1:10, function(x) mean(rnorm(1e7)), mc.cores = snakemake@threads)
saveRDS(1:13,"Data/data.RDS")

saveRDS(1:13,snakemake@output[['outl']][1])
saveRDS(1:13,snakemake@output[['outl']][2])

