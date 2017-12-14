# wBuild

Automatic build tool for R Reports

## Features


* Enables reproducible research by appending every R-markdown script to the global analysis pipeline written in snakemake
* All R scripts using R-markdown get compiled via Rmarkdown and rendered in a navigable web-page
* This is achieved by writing the snakemake rules directly in the header of your R scripts
  * Headers allow the same flexibility (i.e. usage of python) as in the traditional Snakefile

## Installation

- `pip install wBuild`

Within the Gagneurlab, load python version /opt/modules/i12g/anaconda/3-4.1.1/ using module system..

## Getting started
  
* Navigate to an empty directory
* Run `wbuild demo`. This will create a wBuild demo project with various examples.
* Explore the files in `Scripts/`
* View the compiled version of the demo project: <https://i12g-gagneurweb.in.tum.de/project/wBuild/>
* Run `snakemake` to compile the projects
* Open `Output/html/index.html` in your web browser.

## Usage

* Navigate to the root of your project (new or existing)
* Run `wbuild init`
* Run `snakemake`
  
## Documentation

- Run `wbuild --help` or `wbuild <command> --help` to learn more about available wBuild commands.
- See the documentation/demo page at <https://i12g-gagneurweb.in.tum.de/project/wBuild/>


## Credits

Leonhard Wachutka
