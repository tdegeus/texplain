import argparse
import itertools
import os
import re
import sys
from copy import deepcopy
from shutil import copyfile

import numpy as np

from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


def _findenv(text):
    """
    Find the (most probable) current environment by looking backward.

    :param text: Text to consider.
    :return: Environment ("section", "chapter", "figure", "table", "equation", ...)
    """

    env = []
    pos = []
    patterns = [
        re.compile(r"(\\begin{)([^}]*)(})"),
        re.compile(r"(\\)(section)({)([^}]*)(})"),
        re.compile(r"(\\)(chapter)({)([^}]*)(})"),
    ]

    for pattern in patterns:
        env += [re.sub(pattern, r"\2", i[0]) for i in re.finditer(pattern, text)]
        pos += [i.span(0)[0] for i in re.finditer(pattern, text)]

    return env[np.argmax(pos)]


class TeX:
    """
    Simple TeX file manipulations.

    :param read_from_file: Read from file.
    :param text: Supply as text.
    """

    def __init__(self, read_from_file: str = None, text: str = None):

        if read_from_file is not None:

            if not os.path.isfile(read_from_file):
                raise OSError(f'"{read_from_file:s}" does not exist')

            self.dirname = os.path.dirname(read_from_file)
            self.filename = os.path.split(read_from_file)[1]

            if len(self.dirname) == 0:
                self.dirname = "."

        else:

            self.dirname = None
            self.filename = None

        if text is not None:
            self.tex = text
        else:
            assert read_from_file is not None
            with open(read_from_file) as file:
                self.tex = file.read()

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

        assert self.dirname is not None

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
        assert self.dirname is not None
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

    def remove_commentlines(self):
        """
        Remove lines that are entirely a comment.
        """

        tmp = self.tex.split("\n")
        tmp = list(itertools.filterfalse(re.compile(r"^\s*%.*$").match, tmp))
        self.tex = "\n".join(tmp)

    def change_label(self, old_label: str, new_label: str):
        r"""
        Change label in ``\label{...}`` and ``\ref{...}`` (-like) commands.

        :param old_label: Old label.
        :param new_label: New label.
        """

        old = re.escape(old_label)
        new = re.escape(new_label)

        # single labels

        self.tex = re.sub(
            r"(\\label{)(" + old + ")(})", r"\1" + new + r"\3", self.tex, re.MULTILINE
        )

        self.tex = re.sub(
            r"(\\)(\w*)(ref\*?{)(" + old + ")(})", r"\1\2\3" + new + r"\5", self.tex, re.MULTILINE
        )

        # grouped labels

        self.tex = re.sub(
            r"(\\cref\*?{)(" + old + ")(,[^}]*})", r"\1" + new + r"\3", self.tex, re.MULTILINE
        )

        self.tex = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(})", r"\1" + new + r"\3", self.tex, re.MULTILINE
        )

        self.tex = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(})", r"\1" + new + r"\3", self.tex, re.MULTILINE
        )

        self.tex = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(,[^}]*})", r"\1" + new + r"\3", self.tex, re.MULTILINE
        )

    def labels(self) -> list[str]:
        """
        Return list of labels (in order of appearance).
        """

        labels = []

        for i in re.findall(r"(.*)(\\label{)([^}]*)(})(.*)", self.tex, re.MULTILINE):
            labels.append(i[2])

        return labels

    def format_labels(self):
        """
        Format all labels as:
        *   ``sec:...``: Section labels.
        *   ``ch:...``: Chapter labels.
        *   ``fig:...``: Figure labels.
        *   ``tab:...``: Table labels.
        *   ``eq:...``: Math labels.
        """

        iden = dict(
            section="sec",
            chapter="ch",
            figure="fig",
            table="tab",
            equation="eq",
            align="eq",
            eqnarray="eq",
        )

        for label in self.labels():
            pre, post = self.tex.split(f"\\label{{{label}}}")
            key = iden[_findenv(pre)]
            if not re.match(key + ":.*", label, re.IGNORECASE):
                self.change_label(label, f"{key}:{label}")
            elif not re.match(key + ":.*", label):
                info = re.split(re.compile(f"({key}:)(.*)", re.IGNORECASE), label)[2]
                self.change_label(label, f"{key}:{info}")

    def use_cleveref(self):
        """
        Replace ``Eq.~\\eqref{...}``, ``Fig.~\ref{...}``, etc. for ``\\cref{...}``.
        """

        for key in ["Figure", "Fig.", "Table", "Tab.", "Chapter", "Ch.", "Section", "Sec."]:
            self.tex = re.sub(
                r"(" + key + r"~?\s?\\ref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.tex,
                re.MULTILINE,
                re.IGNORECASE,
            )

        for key in ["Equation", "Eq."]:
            self.tex = re.sub(
                r"(" + key + r"~?\s?\\ref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.tex,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.tex = re.sub(
                r"(" + key + r"~?\s?\\eqref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.tex,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.tex = re.sub(
                r"(" + key + r"~?\s?\(\\ref)(\*?{)([^}]*})(\))",
                r"\\cref\2\3",
                self.tex,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.tex = re.sub(
                r"(" + key + r"~?\s?\[\\ref)(\*?{)([^}]*})(\])",
                r"\\cref\2\3",
                self.tex,
                re.MULTILINE,
                re.IGNORECASE,
            )


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


def _texcleanup_parser():
    """
    Return parser for :py:func:`texcleanup`.
    """

    h = "Apply some simple clean-up rules."
    parser = argparse.ArgumentParser(description=h)

    h = 'Optionally add "fig:" etc to labels'
    parser.add_argument("--format-labels", action="store_store", help=h)

    h = "Remove lines that have only comments"
    parser.add_argument("--remove-commentlines", action="store_store", help=h)

    h = r'Change "Fig.~\ref{...}" etc. to "\cref{...}"'
    parser.add_argument("--use-cleveref", action="store_store", help=h)

    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("files", nargs="*", type=str, help="TeX file")

    return parser


def texcleanup(args: list[str]):
    """
    Command-line tool to copy to clean output directory, see ``--help``.
    """

    parser = _texcleanup_parser()
    args = parser.parse_args(args)
    assert all([os.path.isfile(file) for file in args.files])

    for file in args.files:

        tex = TeX(file)

        if args.remove_commentlines:
            tex.remove_commentlines()

        if args.format_labels:
            tex.format_labels()

        if args.use_cleveref:
            tex.use_cleveref()

        with open(file, "w") as file:
            file.write(tex.tex)


def _texcleanup_catch():
    try:
        texcleanup(sys.argv[1:])
    except Exception as e:
        print(e)
        return 1


def _texplain_parser():
    """
    Return parser for :py:func:`texplain`.
    """

    desc = "Create a clean output directory with only included files/citations."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("input", type=str, help="TeX file")
    parser.add_argument("outdir", type=str, help="Output directory")
    return parser


def texplain(args: list[str]):
    """
    Command-line tool to copy to clean output directory, see ``--help``.
    """

    parser = _texplain_parser()
    args = parser.parse_args(args)

    if not os.path.isfile(args.input):
        raise OSError(f'"{args.input:s}" does not exist')

    if os.path.isdir(args.outdir):
        if os.listdir(args.outdir):
            raise OSError(f'"{args.outdir:s}" is not empty, provide a new or empty directory')
    else:
        os.makedirs(args.outdir)

    old = TeX(args.input)
    new = deepcopy(old)
    new.dirname = args.outdir

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

    with open(output, "w") as file:
        file.write(new.tex)


def _texplain_catch():
    try:
        texplain(sys.argv[1:])
    except Exception as e:
        print(e)
        return 1
