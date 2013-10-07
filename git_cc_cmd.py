#!/usr/bin/python3

import re
import subprocess
import sys

# compile regexes
re_from = re.compile(r'From\s([a-f0-9]+)')
re_source = re.compile(r'---\sa/(\S+)')
re_diff = re.compile(r'@@\s-([0-9]+),([0-9]+)')

authors = []


def parse_blame(f):
    for line in f:
        print(line)

for filename in sys.argv[1:]:
    with open(filename) as f:
        ma_source = None
        cmd = ['git', 'blame', '--porcelain', '-L', '', '', None]
        for line in f:
            if not cmd[-1]:
                m = re_from.match(line)
                if m:
                    cmd[-1] = m.group(1)
                continue

            # "cmd[-1]" is automatically not None at this point
            m = re_source.match(line)
            if m:
                cmd[-2] = m.group(1)
            elif cmd[-2]:
                m = re_diff.match(line)
                if m:
                    cmd[-3] = ''.join([m.group(1), ',+', m.group(2)])
                    proc_blame = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    parse_blame(proc_blame.stdout)
