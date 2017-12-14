import os
import glob
from yaml import load
from os import link
from pathlib import Path


def autolink(config):
    S = Path('Scripts')
    tasks = load(open(config))

    for filename in glob.iglob('Scripts/**/*.ln.R', recursive=True):
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
