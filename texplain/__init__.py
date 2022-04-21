import argparse
import itertools
import os
import re
import sys
import textwrap
import warnings
from copy import deepcopy
from shutil import copyfile

import numpy as np

from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


def find_matching(
    text: str,
    opening: str,
    closing: str,
    ignore_escaped: bool = True,
) -> dict:
    r"""
    Find matching 'brackets'.

    :param text: The string to consider.
    :param opening: The opening bracket (e.g. "(", "[", "{").
    :param closing: The closing bracket (e.g. ")", "]", "}").
    :param ignore_escaped: Ignore escaped bracket (e.g. "\(", "\[", "\{", "\)", "\]", "\}").
    :return: Dictionary with ``{index_opening: index_closing}``
    """

    a = []
    b = []

    o = re.escape(opening)
    c = re.escape(closing)

    if ignore_escaped:
        o = r"(?<!\\)" + o
        c = r"(?<!\\)" + c

    for i in re.finditer(o, text):
        a.append(i.span()[0])

    for i in re.finditer(c, text):
        b.append(-1 * i.span()[0])

    if len(a) != len(b):
        raise OSError(f"No matching {opening}...{closing} found")

    brackets = sorted(a + b, key=lambda i: abs(i))

    ret = {}
    stack = []

    for i in brackets:
        if i > 0:
            stack.append(i)
        else:
            if len(stack) == 0:
                raise IndexError(f"No closing {closing} at: {i:d}")
            j = stack.pop()
            ret[j] = -1 * i

    if len(stack) > 0:
        raise IndexError(f"No opening {opening} at {stack.pop():d}")

    return ret


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

        if text is None:
            assert read_from_file is not None
            with open(read_from_file) as file:
                text = file.read()

        has_input = re.search(r"(.*)(\\input\{)(.*)(\})", text, re.MULTILINE)
        has_include = re.search(r"(.*)(\\include\{)(.*)(\})", text, re.MULTILINE)

        if has_input or has_include:
            raise OSError(r"TeX files with \input{...} or \include{...} not yet supported")

        a = r"\begin{document}"
        b = r"\end{document}"
        index = find_matching(text, a, b, ignore_escaped=False)

        if len(index) == 1:
            index = list(index.items())[0]
            self.preamble = text[: index[0]]
            self.start = a
            i = index[0] + len(a)
            j = index[1]
            self.main = text[i:j]
            self.postamble = text[j:]
        else:
            self.preamble = ""
            self.start = ""
            self.main = text
            self.postamble = ""

        self.original = text

    def get(self):
        """
        Return document.
        """
        return self.preamble + self.start + self.main + self.postamble

    def changed(self):
        """
        Check if the document has changed.
        """
        return self.original != self.get()

    def float_filenames(self, cmd: str = r"\includegraphics") -> list[tuple[str]]:
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

        tmp = self.main
        self.remove_commentlines()
        self.remove_comments()

        # read the contents of the command
        # - "\includegraphics" accepts "\includegraphics[...]{...}"
        # - "\bibliography" rejects "\bibliographystyle{...}"
        include = []
        for i in self.main.split(cmd)[1:]:
            if i[0] in ["[", "{"]:
                include += [i.split("{")[1].split("}")[0]]

        self.main = tmp

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

        text = self.main.split(cmd)

        for i in range(1, len(text)):
            pre, key = text[i].split("{", 1)
            key, post = key.split("}", 1)
            if key != old:
                continue
            if text[i][0] not in ["[", "{"]:
                continue
            text[i] = pre + "{" + new + "}" + post

        self.main = cmd.join(text)

    def citation_keys(self) -> list[str]:
        r"""
        Read the citation keys in the TeX file
        (keys in ``\cite{...}``, ``\citet{...}``, ``\citep{...}```).

        :return: Unique list of keys in the order or appearance.
        """

        curly_braces = find_matching(self.main, "{", "}", ignore_escaped=True)
        cite = []

        for i in re.finditer(r"(\\cite)([pt])?(\[.*\]\[.*\])?(\{)", self.main):
            o = i.span()[1]
            c = curly_braces[o - 1]
            cite += list(filter(None, self.main[o:c].replace("\n", " ").split(",")))

        return [i.replace(" ", "") for i in cite]

    def find_by_extension(self, ext: str) -> list[str]:
        r"""
        Find all files with a certain extensions in the directory of the TeX file.

        :param ext: File extension.
        :return: List of filenames.
        """
        assert self.dirname is not None
        filenames = os.listdir(self.dirname)
        return [i for i in filenames if os.path.splitext(i)[1] == ext]

    def config_files(self) -> list[str]:
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

        tmp = self.main.split("\n")
        tmp = list(itertools.filterfalse(re.compile(r"^\s*%.*$").match, tmp))
        self.main = "\n".join(tmp)

    def remove_comments(self):
        """
        Remove comments form the main text.
        """

        tmp = self.main.split("\n")
        for i in range(len(tmp)):
            tmp[i] = re.sub(r"([^%]*)(?<!\\)(%)(.*)$", r"\1", tmp[i])
        self.main = "\n".join(tmp)

    def _replace_command_impl(self, cmd: str, nargs: int, replace: str):
        """
        Implementation of command replacement.
        The replacement is recursive: if commands are nested this first replaces the outer
        command and then continues to replace the inner command.
        """

        if not re.search(re.escape(cmd) + "{", self.main):
            return

        n = len(cmd)
        curly_braces = find_matching(self.main, "{", "}", ignore_escaped=True)
        closing = sorted(curly_braces[i] for i in curly_braces)
        opening = np.array(sorted(i for i in curly_braces))
        next_opening = {}
        for i in closing:
            j = np.argmax(opening > i)
            next_opening[i] = opening[j]

        last = 0
        ret = ""

        for match in re.finditer(re.escape(cmd) + "{", self.main):
            opening = match.span(0)[0] + n
            if opening < last:
                continue

            parts = []
            for j in range(nargs):
                closing = curly_braces[opening]
                i = opening + 1
                parts += [self.main[i:closing]]
                if j == nargs - 1:
                    break
                opening = next_opening[closing]

            out = replace
            while True:
                m = re.search("#[0-9]*", out)
                if not m:
                    break
                i = int(m[0][1:])
                a, b = m.span(0)
                out = out[:a] + parts[i - 1] + out[b:]

            j = match.span(0)[0]
            ret = ret + self.main[last:j] + out
            last = closing + 1

        self.main = ret + self.main[last:]

        if re.search(re.escape(cmd) + "{", self.main):
            return self._replace_command_impl(cmd, nargs, replace)

    def replace_command(self, cmd: str, replace: str):
        r"""
        Replace command. For example:

        *   Remove the command::

                replace_command(r"{\TG}[1]", "")

                    >>> This is a \TG{I would replace this} text.
                    <<< This is a  text.

        *   Select a part of the command::

                replace_command(r"{\TG}[2]", "#1")

                    >>> This is a \TG{text}{test}.
                    <<< This is a test.

        *   Change the command::

                replace_command(r"{\TG}[2]", "\mycomment{#1}{#2}")

                    >>> This is a \TG{text}{test}.
                    <<< This is a \mycomment{text}{test}.

        :param cmd:
            The command's definition. Given ``\newcommand{cmd}[args]{def}`` you should specify
            ``{cmd}[args]``, or ``{cmd}`` (or even ``cmd``) which defaults to ``{cmd}[1]``

        :param replace:
            The ``def`` part (curly braces around are optional). As in LaTeX replacement is
            done on ``#1``, ``#2``, ...
        """

        if not re.match("{.*}", cmd):
            cmd = "{" + cmd + "}"
        if cmd[-1] != "]":
            cmd = cmd + "[1]"
        if not re.match("{.*}", replace):
            replace = "{" + replace + "}"

        scmd = re.split(r"({)(\\\w*)(})(\[)([0-9]*)(\])", cmd)
        sreplace = re.split(r"({)(.*)(})", replace)

        if len(scmd) != 8:
            raise OSError(f'Unknown cmd = "{cmd}"')

        if len(sreplace) != 5:
            raise OSError(f'Unknown replace = "{replace}"')

        cmd = scmd[2]
        replace = sreplace[2]
        nargs = int(scmd[5])

        self._replace_command_impl(cmd, nargs, replace)

    def change_label(self, old_label: str, new_label: str, overwrite: bool = False):
        r"""
        Change label in ``\label{...}`` and ``\ref{...}`` (-like) commands.

        :param old_label: Old label.
        :param new_label: New label.
        :param overwrite: Overwrite existing labels.
        """

        if old_label == new_label:
            return

        if not overwrite:
            if new_label in self.labels():
                raise OSError(f'Label "{new_label:s}" already exists')

        old = re.escape(old_label)
        new = new_label

        # single labels

        self.main = re.sub(
            r"(\\label{)(" + old + ")(})", r"\1" + new + r"\3", self.main, re.MULTILINE
        )

        self.main = re.sub(
            r"(\\)(\w*)(ref\*?{)(" + old + ")(})", r"\1\2\3" + new + r"\5", self.main, re.MULTILINE
        )

        # grouped labels

        self.main = re.sub(
            r"(\\cref\*?{)(" + old + ")(,[^}]*})", r"\1" + new + r"\3", self.main, re.MULTILINE
        )

        self.main = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(})", r"\1" + new + r"\3", self.main, re.MULTILINE
        )

        self.main = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(})", r"\1" + new + r"\3", self.main, re.MULTILINE
        )

        self.main = re.sub(
            r"(\\cref\*?{[^}]*,)(" + old + ")(,[^}]*})",
            r"\1" + new + r"\3",
            self.main,
            re.MULTILINE,
        )

    def labels(self) -> list[str]:
        """
        Return list of labels (in order of appearance).
        """

        labels = []

        for i in re.findall(r"(.*)(\\label{)([^}]*)(})(.*)", self.main, re.MULTILINE):
            labels.append(i[2])

        return labels

    def _reformat(self, label: str, key: str):
        """
        Reformat labels (and references) to f"{key}:{label}" (if needed).
        Suppose that the target is "fig:foo", this function also converts
        "FIG:foo", "fig-foo", "fig_foo", ...

        :param label: The label (with or without ``key:``).
        :param key: The 'keyword' to add/ensure.
        """

        if re.match(f"({key}:)(.*)", label, re.IGNORECASE):
            info = re.split(re.compile(f"({key}:)(.*)", re.IGNORECASE), label)[2]
            return f"{key}:{info}"

        if re.match(f"({key})(-)(.*)", label, re.IGNORECASE):
            info = re.split(re.compile(f"({key})(-)(.*)", re.IGNORECASE), label)[3]
            return f"{key}:{info}"

        if re.match(f"({key})(_)(.*)", label, re.IGNORECASE):
            info = re.split(re.compile(f"({key})(_)(.*)", re.IGNORECASE), label)[3]
            return f"{key}:{info}"

        if not re.match(key + ":.*", label, re.IGNORECASE):
            return f"{key}:{label}"

    def _environment_index(self, envs: list[str], iden: dict) -> dict:
        """
        Get the start and end index of every occurrence of a list of environments.

        :param envs: List of environments present in the main text.

        :param iden:
            Dictionary with identification "key" per environment.
            E.g. ``{"figure": "fig", "figure*": "fig"}``.

        :return:
            Dictionary with an array per "key" with per line the start and end index
            of each environment corresponding to that "key".
        """

        index = {}

        for env in envs:
            key = iden.get(env, "misc")
            a = rf"\begin{{{env}}}"
            b = rf"\end{{{env}}}"
            i = find_matching(self.main, a, b, ignore_escaped=False)
            if key not in index:
                index[key] = i
            else:
                index[key] = index[key] | i

        for key in index:
            index[key] = np.array(list(index[key].items()))

        return index

    def _header_index(self) -> dict:
        """
        Get the index of the closing "}" of all present headers.

        :return:
            A dictionary with for each present header a list with indices corresponding to the
            closing "}" of different occurrences of the headers.
        """

        ret = {"section": [], "subsection": [], "subsubsection": [], "chapter": [], "paragraph": []}
        curly_braces = find_matching(self.main, "{", "}", ignore_escaped=True)

        for key in ret:
            match = r"(\\)(" + key + r")({)([^}]*)(})"
            for i in re.finditer(match, self.main):
                opening = i.span(0)[0] + 1 + len(key)
                ret[key].append(curly_braces[opening])

        return {i: np.array(ret[i]) for i in ret if len(ret[i]) > 0}

    def environments(self) -> list[str]:
        r"""
        Return list with present environments (between \begin{...} ... \end{...}).
        """

        ret = []
        curly_braces = find_matching(self.main, "{", "}", ignore_escaped=True)

        for i in re.finditer(r"\\begin{.*}", self.main):
            opening = i.span(0)[0] + 6
            closing = curly_braces[opening]
            i = opening + 1
            ret += [self.main[i:closing]]

        return list(set(ret))

    def format_labels(self):
        """
        Format all labels as:
        *   ``sec:...``: Section labels.
        *   ``ch:...``: Chapter labels.
        *   ``fig:...``: Figure labels.
        *   ``tab:...``: Table labels.
        *   ``eq:...``: Math labels.
        """

        iden = {
            "section": "sec",
            "section*": "sec",
            "subsection": "sec",
            "subsection*": "sec",
            "subsubsection": "sec",
            "subsubsection*": "sec",
            "paragraph": "sec",
            "paragraph*": "sec",
            "chapter": "ch",
            "chapter*": "ch",
            "figure": "fig",
            "figure*": "fig",
            "table": "tab",
            "table*": "tab",
            "equation": "eq",
            "equation*": "eq",
            "align": "eq",
            "align*": "eq",
            "eqnarray": "eq",
            "eqnarray*": "eq",
        }

        environments = self.environments()
        change = {}
        envs = self._environment_index(environments, iden)
        headers = self._header_index()

        for label in self.labels():

            ilab = self.main.index(rf"\label{{{label}}}")
            stop = False

            for key in envs:
                c = np.logical_and(envs[key][:, 0] < ilab, envs[key][:, 1] > ilab)
                if np.any(c):
                    change[label] = self._reformat(label, key)
                    stop = True
                    break

            if stop:
                continue

            for h in headers:
                test = ilab > headers[h]
                i = test.size - 1 if np.all(test) else np.argmin(test) - 1
                start = headers[h][i] + 1
                if re.match(r"([\s\n%]*)(\\label{)", self.main[start:]):
                    change[label] = self._reformat(label, iden[h])
                    stop = True
                    break

            if stop:
                continue

            warnings.warn(f'Unrecognised label "{label}"')

        for label in change:
            self.change_label(label, change[label])

    def use_cleveref(self):
        """
        Replace::

            Eq.~\\eqref{...}
            Fig.~\\ref{...}
            ...

        By::

            \\cref{...}

        everywhere.
        """

        for key in ["Figure", "Fig.", "Table", "Tab.", "Chapter", "Ch.", "Section", "Sec."]:
            self.main = re.sub(
                r"(" + key + r"~?\s?\\ref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.main,
                re.MULTILINE,
                re.IGNORECASE,
            )

        for key in ["Equation", "Eq."]:
            self.main = re.sub(
                r"(" + key + r"~?\s?\\ref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.main,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.main = re.sub(
                r"(" + key + r"~?\s?\\eqref)(\*?{)([^}]*})",
                r"\\cref\2\3",
                self.main,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.main = re.sub(
                r"(" + key + r"~?\s?\(\\ref)(\*?{)([^}]*})(\))",
                r"\\cref\2\3",
                self.main,
                re.MULTILINE,
                re.IGNORECASE,
            )
            self.main = re.sub(
                r"(" + key + r"~?\s?\[\\ref)(\*?{)([^}]*})(\])",
                r"\\cref\2\3",
                self.main,
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

    h = textwrap.dedent(
        r"""Apply some simple clean-up rules.
        Most of the options are fully self explanatory. A word it need about "--replace-command":
        It can replace a command by another command, or simply 'remove' it, keeping just a sequence
        of arguments. This option is very much like a LaTeX command, but applied to the source.
        For example::

            --replace-command r"{\TG}[2]" "#1"

        Applied a change as follows::

            >>> This is a \TG{text}{test}.
            <<< This is a test.

        Note that the number of arguments, e.g. [2], defaults to one if not specified.
        """
    )
    parser = argparse.ArgumentParser(description=h)

    h = "Remove lines that have only comments"
    parser.add_argument("--remove-commentlines", action="store_true", help=h)

    h = "Remove all comments"
    parser.add_argument("--remove-comments", action="store_true", help=h)

    h = "Replace command (see above)"
    parser.add_argument(
        "--replace-command", type=str, nargs=2, action="append", metavar=("cmd", "def"), help=h
    )

    h = "Change label"
    parser.add_argument(
        "--change-label", type=str, nargs=2, action="append", metavar=("old", "new"), help=h
    )

    h = 'Add "fig:", "eq:", "tab:", "sec:", "ch:" to labels'
    parser.add_argument("--format-labels", action="store_true", help=h)

    h = r'Change "Fig.~\ref{...}" etc. to "\cref{...}"'
    parser.add_argument("--use-cleveref", action="store_true", help=h)

    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("files", nargs="+", type=str, help="TeX file")

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

        if args.remove_commentlines or args.remove_comments:
            tex.remove_commentlines()

        if args.remove_comments:
            tex.remove_comments()

        if args.replace_command:
            for i in args.replace_command:
                tex.replace_command(*i)

        if args.change_label:
            for i in args.change_label:
                tex.change_label(*i)

        if args.format_labels:
            tex.format_labels()

        if args.use_cleveref:
            tex.use_cleveref()

        if tex.changed():
            with open(file, "w") as file:
                file.write(tex.get())


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
    parser.add_argument("-c", "--keep-comments", action="store_true", help="Keep comments")
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

    if not args.keep_comments:
        new.remove_commentlines()
        new.remove_comments()

    includegraphics = old.float_filenames(r"\includegraphics")
    bibfiles = old.float_filenames(r"\bibliography")
    bibkeys = old.citation_keys()
    config_files = old.config_files()

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
        file.write(new.get())


def _texplain_catch():
    try:
        texplain(sys.argv[1:])
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    pass
