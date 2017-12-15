# Use native python code in yaml header

## Example: apply a analysis template by ids

This section we demonstrate how to use native python code in yaml header.

Python code can be included in the yaml header in `py` block.

```
#'---
#' wb:
#'  py:
#'  - | 
#'   with open('Data/ids.txt') as f:
#'    ids = f.read().splitlines()
#'  input:
#'  - idslist: "Data/ids.txt"
#'  - columns: "`sm expand('Output/html/030_AnalysisOfId_{id}.html', id=ids)`"
#'---
```

`sm ...` is escape for snakemake syntax. 
In this example, what happens is as follows:
1. python code under `py` block is excuted. ids stored in `Data/ids.txt` file will be read into `ids` variable. 
2. `sm expand('Output/html/030_AnalysisOfId_{id}.html', id=ids)` will expand into `Output/html/030_AnalysisOfId_{id}.html` for `{id}` in `ids`. These files are listed as inputs (required) for the current script. 
3. snakemake will then look for the script that create these files, which will be `030_AnalysisTemplate.R`, as `Output/html/030_AnalysisOfId_{id}.html` is listed as output for `030_AnalysisTemplate.R`.
4. `Data/ids.txt` is listed as an input, so that everytime `Data/ids.txt` file changed, snakemake will reapply `030_AnalysisTemplate.R` script to all `ids`.
