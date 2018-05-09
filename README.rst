======
wBuild
======

.. _user-overview:

Overview
--------
wBuild is all about making your day easier resolving, updating and cascading various dependencies, pipeline rules and
code structs. Why bother clicking various files and directories in your project one-by-one? Instead of that, wBuild lets you
specify all the needed information in a YAML header right in your code and let the automated :code:`Snakemake` processes do the rest!

You can learn more about the features that wBuild provides either taking a look at the :ref:`features list <features>`
or :ref:`looking at the HTML output of the demo project <running-demo>`. Another interesting thing to take a look at could be
the :ref:`installation requirements & procedure <installation>` and, in particular, :ref:`wBuild project tree structure <project-structure>`.

You can find functionality overview of wBuild and its relationship with Snakemake :ref:`here <overview-of-functionality>`.

Example
-------

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

Running :bash:`snakemake` (provided you've already :ref:`initiated wbuild <wbuild-init>` in your project using :bash:`wbuild init`) will now automatically
parse the parameter out of the header and create an HTML output showing the results of our petal analysis - found in :code:`./Output/html`
by default along with a nice navigable HTML structure.

**Note** that snakemake is configured to run only if the :code:`all.done` file is **not** placed in the :code:`{wbPD}/..`.
Therefore, remove it manually first if you want to run the whole pipeline again without modifying files!


.. image:: /res/images/HTML_output_demo.png
   :scale: 70%
   :align: left

|
|

You can read more about publishing the output HTML to your common server (link!) or try launching demonstration yourself as follows:

.. _running-demo:

Running demo
~~~~~~~~~~~~
* Install wBuild. You can learn more about the installation process :ref:`here <installation>`.
* Navigate to an empty directory
* Run :bash:`wbuild demo`. This will create a wBuild demo project with various examples.
* Explore the files in :bash:`Scripts/`
* Run :bash:`snakemake` to let Snakemake do its thing and compile the project. You can learn why snakemake is so important under `Functionality`_.
* Open :code:`Output/html/index.html` in your web browser. From there, you can browse through sites showing and describing :ref:`basic features <features>` of wBuild on an example analysis.

.. _overview-of-functionality:

Functionality
-------------
wBuild is bound to make the day of writing and publishing analysis scripts and their output easier. It is, however, *not really
a standalone application*, much more **a plugin and "code generator" for the later use of Snakemake**, which is *inevitable* part
of a workflow involving wBuild. Following diagram represents general functional relationship between Snakemake and wBuild:


.. image:: /res/images/snakemake_wbuild_diag.jpg
   :scale: 80%

|
|

As you see Snakemake actually takes the **main** role in a typical wBuild workflow, so every user is *very much encouraged* to
learn more about Snakemake. You can learn more about Snakemake `in its official documentation <http://snakemake.readthedocs.io/en/stable/>`_.
You are also welcome to take a look at the more :ref:`technial features <features>` that wBuild provides.
So be sure to delete it each time you want to restart the pipeline once again!

|

* Enables reproducible research by appending every R-markdown script to the global analysis pipeline written in snakemake
* All R scripts using R-markdown get compiled via Rmarkdown and rendered in a navigable web-page
* This is achieved by writing the snakemake rules directly in the header of your R scripts
* Headers allow the same flexibility (i.e. usage of python) as in the traditional Snakefile
