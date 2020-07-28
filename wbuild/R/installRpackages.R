options(repos=structure(c(CRAN="https://cloud.r-project.org")))

print(.libPaths())

packages <- c("data.table", "DT", "gsubfn", "knitr", "magrittr", "methods", "stringr", "yaml")
installed <- rownames(installed.packages())
for (pckg_name in packages) {
    if (pckg_name %in% installed)
        message(paste(pckg_name, "already installed"))
    else
        install.packages(pckg_name)
}
