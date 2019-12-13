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

run("texplain input1/example.tex test1")

assert(filecmp.cmp('output1/example.tex', 'test1/example.tex', shallow = False))
assert(filecmp.cmp('output1/library.bib', 'test1/library.bib', shallow = False))
assert(filecmp.cmp('output1/figure_1.pdf', 'test1/figure_1.pdf'))
assert(filecmp.cmp('output1/figure_2.pdf', 'test1/figure_2.pdf'))
assert(filecmp.cmp('output1/apalike.bst', 'test1/apalike.bst'))
assert(filecmp.cmp('output1/unsrtnat.bst', 'test1/unsrtnat.bst'))
assert(filecmp.cmp('output1/goose-article.cls', 'test1/goose-article.cls'))

assert(filecmp.cmp('input1/figures/Sequential.pdf', 'test1/figure_1.pdf'))
assert(filecmp.cmp('input1/figures/Diverging.pdf', 'test1/figure_2.pdf'))
assert(filecmp.cmp('input1/apalike.bst', 'test1/apalike.bst'))
assert(filecmp.cmp('input1/unsrtnat.bst', 'test1/unsrtnat.bst'))
assert(filecmp.cmp('input1/goose-article.cls', 'test1/goose-article.cls'))
