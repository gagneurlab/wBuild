Basic Yaml Header

```
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
```

wBuild requires users to define information of the scripts in Rmarkdon yaml header. Besides standard Rmarkdown header, wBuild reads "rules" from `wb` block. Important tags for this block are `input` and `output`. wBuild reads inputs and outputs, and build dependence graph. By default, the script will be excuted by taking the inputs and produce outputs (if any), and rendered the script into a html format. 

For instance, in the demo `020_BacicInput.R`, we define `iris` data from `Data/{wbP}/iris.RDS` as input. In the body of the script, the input/output data will be refered by name. It is of course also possible ot use absolute path, but using the pre-defined place-holders like `wbP` (explained bellow) gives flexibility for resuing existing code. 

# Refer input or output variable by name
`wbReadRDS`  is a readRDS command that aware of inputs by referring to their names. For instance, `iris` will be refered to `Data/{wbP}/iris.RDS` in this case. One can alternatively refer input or output by name using `snakemake@input[[input_variable_name]]` or `snakemake@output[[output_variable_name]]` correspondingly. 

# wBuild place-holder dictionary

wbPD: [output directory for processed data] `Output/ProcessedData`

wbP: [current project] `Analysis1` 

wbPP: [subfolder name] `020_InputOutput`

wbPD_P: [output directory for processed data]/[current project] `Output/ProcessedData/Analysis1`

wbPD_PP: [output directory for processed data]/[current project]/[subfolder name] `Output/ProcessedData/Analysis1/020_InputOutput`
