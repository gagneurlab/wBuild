==========================
Frequently asked questions
==========================

**Q: I've modified my project files and now I'm running snakemake, but it prints there's nothing to be done.**

A: Probably your pipeline is broken. Snakemake is configured to run only if :code:`all.done` file in the ProcessedData directory(:code:`{wbPD}/..`) is out of date and the whole pipline can be run.
Therefore, please remove it manually first if you want to run the whole pipeline again! You can also try to launch :code:`snakemake Index -f`
to force a recreation of the index page. Normally you will then be pointed to the place where your pipeline is broken.

**Q: I want to remove a file from the pipeline:**

A: Just move it into a folder starting with an underscore `_`.

**Q:Can I use my input/output variables defined in header in the code afterwards?**

A: Of course you can! See :ref:`tags section <specify-input>` for more information how.

**Q:Hey, but I don't run snakemake now, and still would like to have something to debug!**

A:You are not alone! See the bottom of :ref:`information about in-script headers <yaml-headers>` - there is a special callable for that!


**Q:All the time I push/pull from my VCS (e.g. git), the modification times of the files get updated. Why, and how to avoid it?**

A: (All) VCS work this way. Unluckily, there's a little we can do about it on our side, since algorithm of comparing timestamps in builds comes from Snakemake.
But you can take care about it yourself relatively easily, e.g. using :code:`touch -r` to restore the modification date of file(s).
See e.g. https://stackoverflow.com/questions/2458042/restore-a-files-modification-time-in-git for more information.
There is also an :ref:`in-built wBuild rule <restore-mod-date>` that does it recursively to all the project files.
