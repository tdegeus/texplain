import subprocess
import os
import filecmp

# support function
# ----------------

def run(cmd):
    out = list(filter(None, subprocess.check_output(cmd,shell=True).decode('utf-8').split('\n')))
    return [i.rstrip() for i in out]

# run test
# --------

dirname = os.path.dirname(os.path.realpath(__file__))

run("texplain {0:s} test1".format(os.path.join(dirname, 'input1', 'example.tex')))

a = open(os.path.join(dirname, 'output1', 'example.tex'), 'r').read()
b = open(os.path.join('test1', 'example.tex'), 'r').read()

import difflib

print('---')

lines1 = a.splitlines()
lines2 = b.splitlines()

for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
    print line

print('---')

lines1 = a.strip().splitlines()
lines2 = b.strip().splitlines()

for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
    print line

print('---')

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'example.tex'),
    os.path.join('test1', 'example.tex')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'library.bib'),
    os.path.join('test1', 'library.bib')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'figure_1.pdf'),
    os.path.join('test1', 'figure_1.pdf')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'figure_2.pdf'),
    os.path.join('test1', 'figure_2.pdf')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'apalike.bst'),
    os.path.join('test1', 'apalike.bst')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'unsrtnat.bst'),
    os.path.join('test1', 'unsrtnat.bst')))

assert(filecmp.cmp(
    os.path.join(dirname, 'output1', 'goose-article.cls'),
    os.path.join('test1', 'goose-article.cls')))

assert(filecmp.cmp(
    os.path.join(dirname, 'input1', 'figures', 'Sequential.pdf'),
    os.path.join('test1', 'figure_1.pdf')))

assert(filecmp.cmp(
    os.path.join(dirname, 'input1', 'figures', 'Diverging.pdf'),
    os.path.join('test1', 'figure_2.pdf')))

assert(filecmp.cmp(
    os.path.join(dirname, 'input1', 'apalike.bst'),
    os.path.join('test1', 'apalike.bst')))

assert(filecmp.cmp(
    os.path.join(dirname, 'input1', 'unsrtnat.bst'),
    os.path.join('test1', 'unsrtnat.bst')))

assert(filecmp.cmp(
    os.path.join(dirname, 'input1', 'goose-article.cls'),
    os.path.join('test1', 'goose-article.cls')))
