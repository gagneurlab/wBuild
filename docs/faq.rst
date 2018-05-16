==========================
Frequently asked questions
==========================

**Q: I've modified my project files and now I'm running snakemake, but it prints there's nothing to be done.**

A: Snakemake is configured to run only if there is no :code:`all.done` file in the ProcessedData directory(:code:`{wbPD}/..`).
Therefore, please remove it manually first if you want to run the whole pipeline again! You can also launch :code:`snakemake Index`
to solve this problem.

