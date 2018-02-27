======
wBuild
======

wBuild is all about making your day easier resolving, updating and cascading various dependencies, pipeline rules and
code structs. Why bother clicking various files and directories in your project one-by-one? Instead of that, wBuild lets you
specify all the needed information in a YAML header right in your code and let the automated :code:`Snakemake` processes do the rest!
You can learn more about functionality overview of wBuild and its relationship with Snakemake here (link).

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

Running :bash:`snakemake` (provided you've already initiated wbuild in your project using :bash:`wbuild init` (link)) will now automatically
parse the parameter out of the header and create an HTML output showing the results of our petal analysis - found in ./Output/html by default along
with a nice navigable HTML structure.

.. image:: /res/images/HTML_output_demo.png
   :scale: 70%
   :align: left

|
|

You can read more about publishing the output HTML to your common server (link!) or try launching demonstration yourself as follows:

Running demo
------------
* Install wBuild. You can learn more about the installation process here (link).
* Navigate to an empty directory
* Run :bash:`wbuild demo`. This will create a wBuild demo project with various examples.
* Explore the files in :bash:`Scripts/`
* Run :bash:`snakemake` to let Snakemake do its thing and compile the project.
You can learn why snakemake is so important in the overview of functionality
* Open :code:`Output/html/index.html` in your web browser. From there, you can browse through many important files
showing and describing basic features of wBuild on an example analysis.

Overview of functionality
-------------------------
wBuild is bound to make the day of writing and publishing analysis scripts and their output easier. It is, however, *not really
a standalone application*, much more **a plugin and "code generator" for the later use of Snakemake**, which is *inevitable* part
of a workflow involving wBuild. Following diagram represents general functional relationship between Snakemake and wBuild:


.. image:: /res/images/snakemake_wbuild_diag.jpg
   :scale: 70%
   :align: left

|
|

As you see Snakemake actually takes the **main** role in a typical wBuild workflow, so every user is *very much encouraged* to
learn more about Snakemake. You can learn more about Snakemake `in its official documentation <http://snakemake.readthedocs.io/en/stable/>`_.
You are also welcome to take a look at the more technial features that wBuild provides.


* Enables reproducible research by appending every R-markdown script to the global analysis pipeline written in snakemake
* All R scripts using R-markdown get compiled via Rmarkdown and rendered in a navigable web-page
* This is achieved by writing the snakemake rules directly in the header of your R scripts
* Headers allow the same flexibility (i.e. usage of python) as in the traditional Snakefile
