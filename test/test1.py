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

assert(
    open(os.path.join(dirname, 'output1', 'main.tex'), 'r').read().strip().splitlines() ==
    open(os.path.join('test1', 'main.tex'), 'r').read().strip().splitlines())

assert(
    open(os.path.join(dirname, 'output1', 'library.bib'), 'r').read().strip().splitlines() ==
    open(os.path.join('test1', 'library.bib'), 'r').read().strip().splitlines())

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
