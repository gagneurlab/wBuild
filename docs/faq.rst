==========================
Frequently asked questions
==========================

**Q: I've modified my project files and now I'm running snakemake, but it prints there's nothing to be done.**

A: Probably your pipeline is broken. Snakemake is configured to run only if :code:`all.done` file in the ProcessedData directory(:code:`{wbPD}/..`) is out of date and the whole pipline can be run.
Therefore, please remove it manually first if you want to run the whole pipeline again! You can also try to launch :code:`snakemake Index -f`
to force a recreation of the index page. Normally you will then be pointed to the place where your pipeline is broken.

**Q: I want to remove a file from the pipeline:**
A: Just move it into a folder starting with an underscore `_`.
