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
        cmd = ['git', 'blame', '--incremental', '-L', '', '', None]
        for line in f:
            m = re_from.match(line)
            if m:
                cmd[-1] = m.group(1)
                continue

            m = re_source.match(line)
            if m:
                cmd[-2] = m.group(1)
                continue

            m = re_diff.match(line)
            if m and cmd[-2] and cmd[-1]:
                cmd[-3] = ''.join([m.group(1), ',+', m.group(2)])
                proc_blame = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                parse_blame(proc_blame.stdout)
