import os
import glob
from yaml import load
from os import link
from pathlib import Path
from wbuild.utils import Config

def autolink(config):
    conf = Config()
    scriptsPath = conf.get("scriptsPath")
    S = Path(scriptsPath)
    tasks = load(open(config))

    for filename in glob.iglob(scriptsPath + '/**/*.ln.R', recursive=True):
        os.remove(filename)

    for task in tasks:
        print(task)
        if task['dst'] is None:
            continue

        if task['src'] is None:
            continue

        for dst in task['dst']:
            if dst is None:
                continue
            if not os.path.exists(str(S / dst)):
                os.makedirs(str(S / dst))
            for src in task['src']:
                if src is None:
                    continue

                link(str(S / Path(src)), str(S / Path(dst) / Path(src).stem) + '.ln.R')
