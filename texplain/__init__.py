'''texplain
    Create a clean output directory with only included files/citations.

Usage:
    texplain [options] <input.tex> <output-directory>

Options:
        --version   Show version.
    -h, --help      Show help.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/texplain
'''

__version__ = '0.3.3'

import os
import re
import sys
import docopt
import click

from copy import deepcopy

from shutil import copyfile
from shutil import rmtree


class TeX:


    def __init__(self, filename):

        if not os.path.isfile(filename):
            raise IOError('"{0:s}" does not exist'.format(filename))

        self.tex = open(filename, 'r').read()
        self.dirname = os.path.dirname(filename)
        self.filename = os.path.split(filename)[1]

        if len(self.dirname) == 0:
            self.dirname = '.'

        has_input = re.search(r'(.*)(\\input\{)(.*)(\})', self.tex, re.MULTILINE)
        has_include = re.search(r'(.*)(\\include\{)(.*)(\})', self.tex, re.MULTILINE)

        if has_input or has_include:
            raise IOError(r'TeX-files with \input{...} or \include{...} not yet supported')


    def read_float(self, cmd = r'\includegraphics'):
        r'''
Extract the keys of 'float' commands (e.g. "\includegraphics{...}", "\bibliography{...}") and
reconstruct their file-names.

:options:

    **cmd** ([``r'\includegraphics'``] | ``<str>``)
        The command to look for.

:returns:

    A list ``[('key', 'filename'), (...), ...]`` in order of appearance.
        '''

        import numpy as np

        # mimic the LaTeX behaviour where an extension is automatically added to a
        # file-name without any extension
        def filename(dirname, name):
            if os.path.isfile(os.path.join(dirname, name)):
                return os.path.relpath(os.path.join(dirname, name), dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.pdf'):
                return os.path.relpath(os.path.join(dirname, name) + '.pdf', dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.eps'):
                return os.path.relpath(os.path.join(dirname, name) + '.eps', dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.png'):
                return os.path.relpath(os.path.join(dirname, name) + '.png', dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.jpg'):
                return os.path.relpath(os.path.join(dirname, name) + '.jpg', dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.tex'):
                return os.path.relpath(os.path.join(dirname, name) + '.tex', dirname)
            if os.path.isfile(os.path.join(dirname, name) + '.bib'):
                return os.path.relpath(os.path.join(dirname, name) + '.bib', dirname)

            raise IOError('Cannot find {0:s}'.format(name))

        # read the contents of the command
        # - "\includegraphics" accepts "\includegraphics[...]{...}"
        # - "\bibliography" rejects "\bibliographystyle{...}"
        include = []
        for i in self.tex.split(cmd)[1:]:
            if i[0] in ['[', '{']:
                include += [i.split('{')[1].split('}')[0]]

        # extract the filename
        out = [(i, filename(self.dirname, i)) for i in include]

        # check for duplicates
        filenames = [i[1] for i in out]
        assert(np.unique(np.array(filenames)).size == len(filenames))

        return out


    def rename_float(self, old, new, cmd = r'\includegraphics'):
        r'''
Rename a key of a 'float' command (e.g. "\includegraphics{...}", "\bibliography{...}").

:arguments:

    **old, new** (``<str>``)
        The old and the new key.

:options:

    **cmd** ([``r'\includegraphics'``] | ``<str>``)
        The command to look for.
        '''

        text = self.tex.split(cmd)

        for i in range(1, len(text)):
            pre, key = text[i].split('{', 1)
            key, post = key.split('}', 1)
            if key != old:
                continue
            if text[i][0] not in ['[', '{']:
                continue
            text[i] = pre + '{' + new + '}' + post

        self.tex = cmd.join(text)


    def read_citation_keys(self):
        r'''
Read the citation keys in the TeX file (those keys in "\cite{...}", "\citet{...}", ...).
Note that the output is unique, in the order or appearance.
        '''

        # extract keys from "cite"
        def extract(string):
            try:
                return list(re.split(
                    r'([pt])?(\[.*\]\[.*\])?(\{[a-zA-Z0-9\,\-\ \_]*\})',
                    string)[3][1: -1].split(','))
            except:
                if len(string) >= 100:
                    string = string[:100]
                raise IOError('Error in interpreting\n {0:s} ...'.format(string))


        # read all keys in "cite", "citet", "citep" commands
        cite = [extract(i) for i in self.tex.split(r'\cite')[1:]]
        cite = list(set([item for sublist in cite for item in sublist]))
        cite = [i.replace(' ','') for i in cite]

        return cite


    def find_by_extension(self, ext):
        r'''
Find all files with a certain extensions in the directory of the TeX-file.
        '''

        filenames = os.listdir(self.dirname)
        return [i for i in filenames if os.path.splitext(i)[1] == ext]


    def read_config(self):
        r'''
Read configuration files in the directory of the TeX-file. A possible extension would be to look
if the files are actually used or not.
        '''

        ext = ['.sty', '.cls', '.bst']
        out = []

        for e in ext:
            out += self.find_by_extension(e)

        return out


def bib_select(text, keys):
    r'''
Limit a BibTeX file to a list of keys.

:arguments:

    **test** (``<str>``)
        The BibTeX file, opened and read.

    **keys** (``<list<str>>``)
        The list of keys to select.

:returns:

    The (reduced) BibTeX file, as string.
    '''

    text = '\n' + text

    bib = list(filter(None, text.split('@')))[1:]

    out = []

    for i in bib:
        if re.match(r'(string\{)(.*)', i):
            continue
        if re.match(r'(Comment\ )(.*)', i, re.IGNORECASE):
            continue
        if re.match(r'(comment\{)(.*)', i, re.IGNORECASE):
            continue
        if re.split(r'(.*\{)(.*)(,\n.*)', i)[2] in keys:
            out += [i]

    out = '\n@' + '\n@'.join(out)

    while '\n\n\n' in out:
        out = out.replace('\n\n\n', '\n\n')

    return out


def Error(message):

    print(message)
    sys.exit(1)


def main():
    r'''
Main function (see command-line help)
    '''

    args = docopt.docopt(__doc__, version=__version__)
    newdir = args['<output-directory>']

    if not os.path.isfile(args['<input.tex>']):
        Error('"{0:s}" does not exist'.format(args['<input.tex>']))

    if os.path.isdir(newdir):
        Error('"{0:s}" exists, please provide a new directory'.format(newdir))

    os.makedirs(newdir)

    old = TeX(args['<input.tex>'])
    new = deepcopy(old)
    new.dirname = newdir

    includegraphics = old.read_float(r'\includegraphics')
    bibfiles = old.read_float(r'\bibliography')
    bibkeys = old.read_citation_keys()
    config_files = old.read_config()

    # Copy configuration files

    for ofile in config_files:
        copyfile(
            os.path.join(old.dirname, ofile),
            os.path.join(new.dirname, ofile))

    # Copy/rename figures

    if len(includegraphics) > 0:

        new_includegraphics = []

        for i, (okey, ofile) in enumerate(includegraphics):
            nkey = 'figure_{0:d}'.format(i + 1)
            ext = os.path.splitext(ofile)[1]
            nfile = ofile.replace(os.path.normpath(okey), nkey)
            if len(os.path.splitext(nfile)[1]) == 0:
                nfile += ext
            new_includegraphics += [(nkey, nfile)]

        for (okey, ofile), (nkey, nfile) in zip(includegraphics, new_includegraphics):
            new.rename_float(
                okey,
                nkey,
                r'\includegraphics')
            copyfile(
                os.path.join(old.dirname, ofile),
                os.path.join(new.dirname, nfile))

    # Copy/reduce BibTeX files

    if len(bibfiles) > 0:

        if len(bibfiles) > 1:
            Error('texplain is only implemented for one BibTeX file')

        okey, ofile = bibfiles[0]

        nkey = 'library'
        nfile = ofile.replace(os.path.normpath(okey), nkey)

        bib = bib_select(
            open(os.path.join(old.dirname, ofile), 'r').read(),
            bibkeys)

        new.rename_float(
            okey,
            nkey,
            r'\bibliography')

        open(os.path.join(new.dirname, nfile), 'w').write(bib)

    # Write modified TeX file

    output = os.path.join(new.dirname, 'main.tex')

    if os.path.isfile(output):
        output = os.path.join(new.dirname, new.filename)

    open(output, 'w').write(new.tex)
