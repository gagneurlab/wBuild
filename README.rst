======
wBuild
======

wBuild is all about making your day easier resolving, updating and cascading various dependencies, pipeline rules and
code structs. Why bother clicking various files and directories in your project one-by-one? Instead of that, wBuild lets you
specify all the needed information in a YAML header right in your code and let the automated Snakemake processes do the rest!

Usage example
-------------
We create a script in R and provide a YAML header with wBuild-supported tags (link to more) :

.. code-block:: R

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

    source('.wBuild/wBuildParser.R')
    parseWBHeader("Scripts/Analysis1/050_PythonCode/030_AnalysisTemplate.R")

    id = snakemake@wildcards[["id"]]
    iris_df = wbReadRDS('iris')
    colnames(iris_df) = gsub('\\.','',colnames(iris_df))
    hist(iris_df[[id]],main=id)

Running :bash:`snakemake` (provided you've already initiaded wbuild in your project using :bash:`wbuild init` (link)) will now automatically
parse the parameter out of the header and create an HTML output showing the results of our petal analysis - found in ./Output/html by default along
with a nice navigable HTML structure.

.. image:: /res/images/HTML_output_demo.png
   :scale: 70%
   :align: left

|

You can read more about publishing the output HTML to your common server (link!) or try launching demonstration yourself as follows:

Running demo
------------
* Navigate to an empty directory
* Run `wbuild demo`. This will create a wBuild demo project with various examples.
* Explore the files in `Scripts/`
* View the compiled version of the demo project: <https://i12g-gagneurweb.in.tum.de/project/wBuild/>
* Run `snakemake` to compile the projects
* Open `Output/html/index.html` in your web browser.

Features
--------

* Enables reproducible research by appending every R-markdown script to the global analysis pipeline written in snakemake
* All R scripts using R-markdown get compiled via Rmarkdown and rendered in a navigable web-page
* This is achieved by writing the snakemake rules directly in the header of your R scripts
  * Headers allow the same flexibility (i.e. usage of python) as in the traditional Snakefile


Getting started
---------------



Usage
-----

* Navigate to the root of your project (new or existing)
* Run `wbuild init`
* Run `snakemake`

Documentation
-------------

- Run `wbuild --help` or `wbuild <command> --help` to learn more about available wBuild commands.
- See the documentation/demo page at <https://i12g-gagneurweb.in.tum.de/project/wBuild/>


Credits
---------

Leonhard Wachutka
