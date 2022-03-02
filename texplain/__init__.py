"""texplain
    Create a clean output directory with only included files/citations.

Usage:
    texplain [options] <input.tex> <output-directory>

Options:
        --version   Show version.
    -h, --help      Show help.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/texplain
"""

import os
import re
import docopt
import numpy as np

from copy import deepcopy

from shutil import copyfile

from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


class TeX:
    """
    Simple TeX file manipulations.
    """

    def __init__(self, filename: str):

        if not os.path.isfile(filename):
            raise OSError(f'"{filename:s}" does not exist')

        with open(filename) as file:
            self.tex = file.read()

        self.dirname = os.path.dirname(filename)
        self.filename = os.path.split(filename)[1]

        if len(self.dirname) == 0:
            self.dirname = "."

        has_input = re.search(r"(.*)(\\input\{)(.*)(\})", self.tex, re.MULTILINE)
        has_include = re.search(r"(.*)(\\include\{)(.*)(\})", self.tex, re.MULTILINE)

        if has_input or has_include:
            raise OSError(r"TeX files with \input{...} or \include{...} not yet supported")

    def read_float(self, cmd: str = r"\includegraphics") -> list[tuple[str]]:
        r"""
        Extract the keys of 'float' commands
        (e.g. ``\includegraphics{...}``, ``\bibliography{...}``)
        and reconstruct their filenames.
        This operation is read-only.

        :param cmd: The command to look for.
        :return: A list ``[('key', 'filename')]`` in order of appearance.
        """

        # mimic the LaTeX behaviour where an extension is automatically added to a
        # file-name without any extension
        def filename(dirname, name):
            if os.path.isfile(os.path.join(dirname, name)):
                return os.path.relpath(os.path.join(dirname, name), dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".pdf"):
                return os.path.relpath(os.path.join(dirname, name) + ".pdf", dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".eps"):
                return os.path.relpath(os.path.join(dirname, name) + ".eps", dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".png"):
                return os.path.relpath(os.path.join(dirname, name) + ".png", dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".jpg"):
                return os.path.relpath(os.path.join(dirname, name) + ".jpg", dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".tex"):
                return os.path.relpath(os.path.join(dirname, name) + ".tex", dirname)
            if os.path.isfile(os.path.join(dirname, name) + ".bib"):
                return os.path.relpath(os.path.join(dirname, name) + ".bib", dirname)

            raise OSError(f"Cannot find {name:s}")

        # read the contents of the command
        # - "\includegraphics" accepts "\includegraphics[...]{...}"
        # - "\bibliography" rejects "\bibliographystyle{...}"
        include = []
        for i in self.tex.split(cmd)[1:]:
            if i[0] in ["[", "{"]:
                include += [i.split("{")[1].split("}")[0]]

        # extract the filename
        out = [(i, filename(self.dirname, i)) for i in include]

        # check for duplicates
        filenames = [i[1] for i in out]
        assert np.unique(np.array(filenames)).size == len(filenames)

        return out

    def rename_float(self, old: str, new: str, cmd: str = r"\includegraphics"):
        r"""
        Rename a key of a 'float' command
        (e.g. ``\includegraphics{...}``, ``\bibliography{...}``).
        This changes the TeX file.

        :param old: Old key.
        :param new: New key.
        :param cmd: The command to look for.
        """

        text = self.tex.split(cmd)

        for i in range(1, len(text)):
            pre, key = text[i].split("{", 1)
            key, post = key.split("}", 1)
            if key != old:
                continue
            if text[i][0] not in ["[", "{"]:
                continue
            text[i] = pre + "{" + new + "}" + post

        self.tex = cmd.join(text)

    def read_citation_keys(self) -> list[str]:
        r"""
        Read the citation keys in the TeX file
        (keys in ``\cite{...}``, ``\citet{...}``, ``\citep{...}```).

        :return: Unique list of keys in the order or appearance.
        """

        # extract keys from "cite"
        def extract(string):
            try:
                match = r"([pt])?(\[.*\]\[.*\])?(\{[a-zA-Z0-9\.\,\-\ \_]*\})"
                return list(re.split(match, string)[3][1:-1].split(","))
            except IndexError:
                if len(string) >= 100:
                    string = string[:100]
                raise OSError(f"Error in interpreting\n {string:s} ...")

        # read all keys in "cite", "citet", "citep" commands
        cite = [extract(i) for i in self.tex.split(r"\cite")[1:]]
        cite = list({item for sublist in cite for item in sublist})
        cite = [i.replace(" ", "") for i in cite]

        return cite

    def find_by_extension(self, ext: str) -> list[str]:
        r"""
        Find all files with a certain extensions in the directory of the TeX file.

        :param ext: File extension.
        :return: List of filenames.
        """

        filenames = os.listdir(self.dirname)
        return [i for i in filenames if os.path.splitext(i)[1] == ext]

    def read_config(self) -> list[str]:
        r"""
        Read configuration files in the directory of the TeX file.

        :return: List of filenames.

        .. todo::

            Check if the files are actually used or not.
        """

        ext = [".sty", ".cls", ".bst"]
        out = []

        for e in ext:
            out += self.find_by_extension(e)

        return out


def bib_select(text: str, keys: list[str]) -> str:
    r"""
    Limit a BibTeX file to a list of keys.

    :param test: The BibTeX file as string.
    :param keys: The list of keys to select.
    :return: The (reduced) BibTeX file, as string.
    """

    text = "\n" + text

    bib = list(filter(None, text.split("@")))[1:]

    out = []

    for i in bib:
        if re.match(r"(string\{)(.*)", i):
            continue
        if re.match(r"(Comment\ )(.*)", i, re.IGNORECASE):
            continue
        if re.match(r"(comment\{)(.*)", i, re.IGNORECASE):
            continue
        if re.split(r"(.*\{)(.*)(,\n.*)", i)[2] in keys:
            out += [i]

    out = "\n@" + "\n@".join(out)

    while "\n\n\n" in out:
        out = out.replace("\n\n\n", "\n\n")

    return out


def from_commandline():
    r"""
    Main function (see command-line help)
    """

    args = docopt.docopt(__doc__, version=version)
    newdir = args["<output-directory>"]

    if not os.path.isfile(args["<input.tex>"]):
        raise OSError('"{:s}" does not exist'.format(args["<input.tex>"]))

    if os.path.isdir(newdir):
        if os.listdir(newdir):
            raise OSError(f'"{newdir:s}" is not empty, please provide a new or empty directory')
    else:
        os.makedirs(newdir)

    old = TeX(args["<input.tex>"])
    new = deepcopy(old)
    new.dirname = newdir

    includegraphics = old.read_float(r"\includegraphics")
    bibfiles = old.read_float(r"\bibliography")
    bibkeys = old.read_citation_keys()
    config_files = old.read_config()

    # Copy configuration files

    for ofile in config_files:
        copyfile(os.path.join(old.dirname, ofile), os.path.join(new.dirname, ofile))

    # Copy/rename figures

    if len(includegraphics) > 0:

        new_includegraphics = []

        for i, (okey, ofile) in enumerate(includegraphics):
            nkey = f"figure_{i + 1:d}"
            ext = os.path.splitext(ofile)[1]
            nfile = ofile.replace(os.path.normpath(okey), nkey)
            if len(os.path.splitext(nfile)[1]) == 0:
                nfile += ext
            new_includegraphics += [(nkey, nfile)]

        for (okey, ofile), (nkey, nfile) in zip(includegraphics, new_includegraphics):
            new.rename_float(okey, nkey, r"\includegraphics")
            copyfile(os.path.join(old.dirname, ofile), os.path.join(new.dirname, nfile))

    # Copy/reduce BibTeX files

    if len(bibfiles) > 0:

        if len(bibfiles) > 1:
            raise OSError("texplain is only implemented for one BibTeX file")

        okey, ofile = bibfiles[0]

        nkey = "library"
        nfile = ofile.replace(os.path.normpath(okey), nkey)

        bib = bib_select(open(os.path.join(old.dirname, ofile)).read(), bibkeys)

        new.rename_float(okey, nkey, r"\bibliography")

        open(os.path.join(new.dirname, nfile), "w").write(bib)

    # Write modified TeX file

    output = os.path.join(new.dirname, "main.tex")

    if os.path.isfile(output):
        output = os.path.join(new.dirname, new.filename)

    open(output, "w").write(new.tex)


def main():

    try:

        from_commandline()

    except Exception as e:

        print(e)
        return 1
