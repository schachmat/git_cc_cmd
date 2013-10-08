#!/usr/bin/python3

import re
import subprocess
import sys

# compile regexes
re_hash = re.compile(r'From ([a-f0-9]+)')
re_file = re.compile(r'--- a/(\S+)')
re_diff = re.compile(r'@@ -([0-9]+),([0-9]+)')
re_auth = re.compile(r'author (.+)\n$')
re_mail = re.compile(r'author-mail <(.+)>\n$')

authors = {}


def parse_blame(f):
    author = None
    for line in f:
        if not author:
            m = re_auth.match(line)
            if m:
                author = m.group(1)
        else:
            m = re_mail.match(line)
            if m:
                authors[m.group(1)] = author
                author = None

for filename in sys.argv[1:]:
    with open(filename) as f:
        ma_source = None
        cmd = ['git', 'blame', '--porcelain', '-L', None, None, None]
        for line in f:
            if not cmd[-1]:
                m = re_hash.match(line)
                if m:
                    cmd[-1] = m.group(1)
                continue

            # "cmd[-1]" is automatically not None at this point
            m = re_file.match(line)
            if m:
                cmd[-2] = m.group(1)
            elif line == '--- /dev/null\n':
                cmd[-2] = None
            elif cmd[-2]:
                m = re_diff.match(line)
                if m:
                    cmd[-3] = m.group(1) + ',+' + m.group(2)
                    proc_blame = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                  universal_newlines=True)
                    parse_blame(proc_blame.stdout)

for (mail, name) in authors.items():
    print(''.join(['"', name, '" <', mail, '>']))
