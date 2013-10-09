#!/usr/bin/python3

from subprocess import Popen as Proc, PIPE as pipe
import re
import sys

# compile regexes
re_hash = re.compile(r'From ([a-f0-9]+)')
re_file = re.compile(r'--- a/(\S+)\n$')
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
        parenthash, srcfile = None, None
        for line in f:
            if not parenthash:
                m = re_hash.match(line)
                if m:
                    parenthash = m.group(1) + '^'
                continue

            # parenthash is automatically not None at this point
            m = re_file.match(line)
            if m:
                srcfile = m.group(1)
            elif line.startswith('--- '):
                srcfile = None
            elif srcfile:
                m = re_diff.match(line)
                if m:
                    lines = m.group(1) + ',+' + m.group(2)
                    blame = Proc(['git', 'blame', '--porcelain', '-L', lines,
                                  parenthash, '--', srcfile],
                                 stdout=pipe, universal_newlines=True)
                    parse_blame(blame.stdout)

for (mail, name) in authors.items():
    print(''.join(['"', name, '" <', mail, '>']))
