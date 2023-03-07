import argparse
import copy
import enum
import itertools
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings
from collections.abc import Callable
from copy import deepcopy
from shutil import copyfile

import numpy as np
import yaml
from numpy.typing import ArrayLike
from numpy.typing import NDArray

from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


def find_opening(
    text: str,
    opening: str,
    ignore_escaped: bool = True,
) -> list[int]:
    r"""
    Find opening 'bracket'.

    :param text: The string to consider.
    :param opening: The opening 'bracket' (e.g. "(", "[", "{", but also "%").
    :param ignore_escaped: Ignore escaped 'bracket' (e.g. "\(", "\[", "\{", "\%").
    :return: List of indices of opening 'brackets' (sorted by definition).
    """

    o = re.escape(opening)

    if ignore_escaped:
        o = r"(?<!\\)" + o

    return [i.span()[0] for i in re.finditer(o, text)]


def find_commented(text: str) -> list[list[int]]:
    """
    Find comments bits of text.
    The output is such that one can find the comments text as follows::

        for i, j in find_commented(text):
            print(text[i + 1 : j]) # i is the index of "%"

    :param text: The string to consider.
    :return: List of of indices of the beginning and end of the comments.
    """

    comments = np.array(find_opening(text, "%", ignore_escaped=True))
    newlines = np.array(find_opening(text, "\n", ignore_escaped=False) + [len(text)])

    ret = []

    for c in comments:
        j = np.argmax(newlines > c)
        ret.append([c, newlines[j]])
        newlines = newlines[j + 1 :]  # noqa: E203

    return ret


def is_commented(text: str) -> NDArray[bool]:
    """
    Return array that lists per character if it corresponds to commented text.

    :param text: The string to consider.
    :return: Array of booleans.
    """

    comments = find_commented(text)
    ret = np.zeros(len(text), dtype=bool)
    for i, j in comments:
        ret[i:j] = True
    return ret


def find_matching(
    text: str,
    opening: str,
    closing: str,
    ignore_escaped: bool = True,
    ignore_commented: bool = False,
    escape: bool = True,
    opening_match: int = 0,
    closing_match: int = 0,
    return_array: bool = False,
) -> dict:
    r"""
    Find matching 'brackets'.

    :param text: The string to consider.
    :param opening: The opening bracket (e.g. "(", "[", "{").
    :param closing: The closing bracket (e.g. ")", "]", "}").
    :param ignore_escaped: Ignore escaped bracket (e.g. "\(", "\[", "\{", "\)", "\]", "\}").
    :param ignore_commented: Ignore any text that is commented (e.g. "% ...").
    :param escape: If ``True``,  ``opening`` and ``closing`` are escaped.
    :param opening_match: Select index of begin (``0``) or end (``1``) of opening bracket match.
    :param closing_match: Select index of begin (``0``) or end (``1``) of closing bracket match.
    :param return_array: If ``True``, return array of indices instead of dictionary.
    :return: Dictionary with ``{index_opening: index_closing}``
    """

    if escape:
        opening = re.escape(opening)
        closing = re.escape(closing)

    if ignore_escaped:
        opening = r"(?<!\\)" + opening
        closing = r"(?<!\\)" + closing

    a = [i.span()[opening_match] for i in re.finditer(opening, text)]
    b = [-1 * i.span()[closing_match] for i in re.finditer(closing, text)]

    if len(a) == 0 and len(b) == 0:
        return {}

    if ignore_commented:
        is_comment = is_commented(text)
        a = np.array(a)
        b = -np.array(b)
        a = list(a[~is_comment[a]])
        b = list(-b[~is_comment[b]])

    if len(a) != len(b):
        raise OSError(f"Unmatching {opening}...{closing} found")

    brackets = sorted(a + b, key=lambda i: abs(i))

    ret = {}
    stack = []

    for i in brackets:
        if i >= 0:
            stack.append(i)
        else:
            if len(stack) == 0:
                raise IndexError(f"No closing {closing} at: {i:d}")
            j = stack.pop()
            ret[j] = -1 * i

    if len(stack) > 0:
        raise IndexError(f"No opening {opening} at {stack.pop():d}")

    if return_array:
        return _indices2array(ret)

    return ret


def _indices2array(indices: dict[int]):
    """
    Convert indices for :py:func:`find_matching` to array.

    :param indices: Dictionary of indices ``{a: b, ...}``
    :return: Array of indices ``[[a, b], ...]``
    """

    ret = np.zeros((len(indices), 2), dtype=int)
    for i, opening in enumerate(indices):
        ret[i, 0] = opening
        ret[i, 1] = indices[opening]
    return ret


def remove_comments(text: str) -> str:
    """
    Remove comments from a string.

    :param text: The string to consider.
    :return: The string without comments.
    """
    text = text.split("\n")
    for i in range(len(text)):
        text[i] = re.sub(r"([^%]*)(?<!\\)(%)(.*)$", r"\1", text[i])
    return "\n".join(text)


def environments(text: str) -> list[str]:
    r"""
    Return list with present environments (between ``\begin{...} ... \end{...}``).
    """

    ret = []
    curly_braces = find_matching(text, "{", "}", ignore_escaped=True)

    for i in re.finditer(r"\\begin{.*}", text):
        opening = i.span(0)[0] + 6
        closing = curly_braces[opening]
        i = opening + 1
        ret += [text[i:closing]]

    return list(set(ret))


class PlacholderType(enum.Enum):
    """
    Type of placeholder.
    """

    comment = enum.auto()
    inline_math = enum.auto()
    environment = enum.auto()
    command = enum.auto()
    noindent_block = enum.auto()
    special_indent = enum.auto()


class Placeholder:
    """
    Placeholder for text.
    This class stores the text to be replaced by a placeholder and the placeholder itself.
    In addition, it can store the whitespace before and after the placeholder.

    :param placeholder: The placeholder to use.
    :param content: The text replaced by the placeholder.
    :param space_front: The whitespace before the placeholder.
    :param space_back: The whitespace after the placeholder.
    :param ptype: The type of placeholder.
    """

    def __init__(
        self,
        placeholder: str,
        content: str,
        space_front: str = None,
        space_back: str = None,
        ptype: PlacholderType = None,
    ):
        self.placeholder = placeholder
        self.content = content
        self.space_front = space_front
        self.space_back = space_back
        self.ptype = ptype

    @classmethod
    def from_text(
        self, placeholder: str, text: str, start: int, end: int, ptype: PlacholderType = None
    ):
        """
        Replace text with placeholder.
        Save the content and the current whitespace before and after the placeholder.
        To restore the original text precisely::

            placeholder, text = Placeholder.from_text(placeholder, text, start, end)
            text = placeholder.to_text(text)

        :param placeholder: The placeholder to use.
        :param text: The text to consider.
        :param start: The start index of ``text`` to be replaced by the placeholder.
        :param end: The end index of ``text`` to be replaced by the placeholder.
        :param ptype: The type of placeholder.
        :return: ``(Placeholder, text)`` where in ``text`` the placeholder is inserted.
        """
        pre = text[:start][::-1]
        post = text[end:]
        front = re.search(r"\s*", pre).end()
        back = re.search(r"\s*", post).end()
        return (
            Placeholder(placeholder, text[start:end], pre[:front][::-1], post[:back], ptype),
            text[:start] + placeholder + text[end:],
        )

    def to_text(self, text: str, index: int = None) -> str:
        """
        Replace placeholder with content.
        If the whitespace before and after the placeholder is stored, it is restored.

        :param text: The string to consider.
        :param index: The index of the placeholder.
        """
        if index is None:
            index = text.find(self.placeholder)

        pre = text[:index][::-1]
        post = text[index + len(self.placeholder) :]  # noqa: E203

        if self.space_front is not None:
            front = re.search(r"\s*", pre).end()
            pre = pre[front:][::-1] + self.space_front

        if self.space_back is not None:
            back = re.search(r"\s*", post).end()
            post = self.space_back + post[back:]

        return pre + self.content + post

    def __repr__(self) -> str:
        return self.placeholder


class GeneratePlaceholder:
    """
    Class to generate a new placeholder.
    The following placeholder is generated every time the object is called::

        -{base}-{name}-{i:d}-

    For example::

        >>> gen = GeneratePlaceholder(base="foo", name="bar")
        >>> gen()
        '-foo-bar-1-'
        >>> gen()
        '-foo-bar-2-'

    :param base: The base of the placeholder.
    :param name: The name of the placeholder.
    """

    def __init__(self, base: str, name: str):
        self.i = 0
        self.base = base
        self.name = name

    def __call__(self):
        self.i += 1
        return f"-{self.base}-{self.name}-{self.i:d}-"


def _apply_placeholders(
    text: str,
    indices: ArrayLike,
    base: str,
    name: str,
    ptype: PlacholderType,
) -> tuple[str, list[Placeholder]]:
    """
    Replace text with placeholders.
    Note: nested placeholders are skipped.

    :param text: The text to consider.
    :param indices: A list of start and end indices of the text to be replaced by a placeholder.
    :param base: The base of the placeholder, see :py:class:`GeneratePlaceholder`.
    :param name: The name of the placeholder, see :py:class:`GeneratePlaceholder`.
    :param ptype: The type of placeholder, see :py:class:`PlacholderType`.
    :return:
        ``(text, placeholders)`` where:
        - ``text`` is the text with the placeholders.
        - ``placeholders`` is a list of the placeholders that includes their original content.
    """

    if indices is None:
        return text, []

    if len(indices) == 0:
        return text, []

    # filter nested
    i = np.argsort(indices[:, 0])
    indices = indices[i]
    keep = np.ones(len(indices), dtype=bool)
    i = 0
    while i < len(indices) - 2:
        while indices[i + 1, 0] < indices[i, 1]:
            keep[i + 1] = False
            i += 1
        i += 1
    indices = indices[keep]

    # replacement
    ret = []
    gen = GeneratePlaceholder(base, name)
    for i in range(indices.shape[0]):
        placeholder, text = Placeholder.from_text(gen(), text, indices[i, 0], indices[i, 1], ptype)
        ret += [placeholder]
        indices -= len(placeholder.content) - len(placeholder.placeholder)

    return text, ret


def text_to_placeholders(
    text: str, ptypes: list[PlacholderType], base: str = "TEXINDENT"
) -> tuple[str, list[Placeholder]]:
    r"""
    Replace text with placeholders.
    The following placeholders are supported:

    -   :py:class:`PlacholderType.noindent_block`:

        .. code-block:: latex

            % \begin{noindent}
            ...
            % \end{noindent}


    -   :py:class:`PlacholderType.comment`:

        .. code-block:: latex

            % ...

    -   :py:class:`PlacholderType.inline_math`:

        .. code-block:: latex

            $...$

    -   :py:class:`PlacholderType.environment`:

        .. code-block:: latex

            \begin{...}
            ...
            \end{...}

    -   :py:class:`PlacholderType.special_indent`:

        -   ``-PLACEHOLDER-)`` <- ``.)``, ``?)``, or ``!)``
        -   ``text-PLACEHOLDER-\n`` <- ``text:\n``
    """

    ret = []

    for ptype in ptypes:
        if ptype == PlacholderType.noindent_block:
            indices = find_matching(
                text,
                r"%\s*\\begin{noindent}",
                r"%\s*\\end{noindent}",
                escape=False,
                closing_match=1,
                return_array=True,
            )
            text, placeholders = _apply_placeholders(
                text, indices, base, "noindent".upper(), PlacholderType.noindent_block
            )
            ret += placeholders

        elif ptype == PlacholderType.comment:
            indices = np.array([i.span() for i in re.finditer(r"(?<!\\)(%)(.*)(\n)", text)])
            if len(indices) == 0:
                continue
            indices[:, 1] -= 1
            text, placeholders = _apply_placeholders(
                text, indices, base, "comment".upper(), PlacholderType.comment
            )
            ret += placeholders

        elif ptype == PlacholderType.environment:
            indices = find_matching(
                text, r"\\begin{.*}", r"\\end{.*}", escape=False, closing_match=1, return_array=True
            )
            text, placeholders = _apply_placeholders(
                text, indices, base, "environment".upper(), PlacholderType.environment
            )
            ret += placeholders

        elif ptype == PlacholderType.inline_math:
            pattern = r"(?<!\\)" + re.escape("$")  # ignore escaped dollar signs
            indices = []
            for i in re.finditer(pattern, text):
                indices.append(i.span()[0])
            indices = np.array(indices).reshape((-1, 2))
            indices[:, 1] += 1
            text, placeholders = _apply_placeholders(
                text, indices, base, "math".upper(), PlacholderType.inline_math
            )
            ret += placeholders

        elif ptype == PlacholderType.command:
            braces = find_matching(text, "{", "}", ignore_escaped=True)
            braces.update(find_matching(text, "[", "]", ignore_escaped=True))

            indices = {}
            last_stop = 0

            for match in re.finditer(r"(?<!\\)(\\)(\w*)", text):
                start, stop = match.span()

                # skip begin/end
                if text[start:stop] in ["\\begin", "\\end"]:
                    continue

                # skip nested command
                if start < last_stop:
                    continue

                # continue until there are no more following "{" or "[
                while True:
                    index = re.search(r"(\s*)([\{\[])", text[stop:])
                    if index is None:
                        break
                    if index.start() != 0:
                        break
                    stop = braces[index.end() + stop - 1] + 1

                indices[start] = stop
                last_stop = stop

            indices = _indices2array(indices)

            text, placeholders = _apply_placeholders(
                text, indices, base, "command".upper(), PlacholderType.command
            )
            ret += placeholders

        elif ptype == PlacholderType.special_indent:
            indices = np.array(
                [
                    [i.span()[0], i.span()[1] - 1]
                    for i in re.finditer(r"(?<!\\)([\?\!\.])(\))", text)
                ]
                + [[i.span()[0], i.span()[1] - 1] for i in re.finditer(r"(?<!\\)(\:)(\n)", text)]
            )

            text, placeholders = _apply_placeholders(
                text, indices, base, "subordinate".upper(), PlacholderType.special_indent
            )
            ret += placeholders

        else:
            raise ValueError(f"Unknown placeholder type: {ptype}")

    return text, ret


def text_from_placeholders(
    text: str,
    placeholders: list[Placeholder],
    default_naming: bool = True,
    prefix: str = "TEXINDENT",
) -> str:
    """
    Replace placeholders with original text.
    """

    if len(placeholders) == 0:
        return text

    if default_naming and len(placeholders) > 1:
        placeholders = {i.placeholder: i for i in placeholders}
        while True:
            indices = [
                (text[i.span()[0] : i.span()[1]], i.span()[0])  # noqa: E203
                for i in re.finditer("-" + prefix + r"-\w*-[0-9]*-", text)
            ]
            if len(indices) == 0:
                return text
            offset = 0
            for name, index in indices:
                placeholder = placeholders[name]
                n = len(text)
                text = placeholder.to_text(text, index + offset)
                offset += len(text) - n

    for placeholder in placeholders:
        n = len(text)
        text = placeholder.to_text(text)

    return text


class TeX:
    """
    Simple TeX file manipulations.

    :param text: LaTeX code.
    """

    def __init__(self, text: str):
        self.dirname = None
        self.filename = None

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

    @classmethod
    def from_file(cls, filename: str):
        """
        Read from file.

        :param filename: Path to the file to read.
        """

        file = pathlib.Path(filename)
        ret = cls(file.read_text())
        ret.dirname = file.parent
        ret.filename = file.name

        has_input = re.search(r"(.*)(\\input\{)(.*)(\})", ret.original, re.MULTILINE)
        has_include = re.search(r"(.*)(\\include\{)(.*)(\})", ret.original, re.MULTILINE)

        if has_input or has_include:
            raise OSError(r"TeX files with \input{...} or \include{...} not supported")

        return ret

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
        (keys in ``\cite{...}``, ``\citet{...}``, ``\citep{...}``).

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
        self.main = remove_comments(self.main)

    def _replace_command_impl(self, cmd: str, nargs: int, replace: str, ignore_commented: bool):
        """
        Implementation of command replacement.
        The replacement is recursive: if commands are nested this first replaces the outer
        command and then continues to replace the inner command.
        """

        if not re.search(re.escape(cmd) + "{", self.main):
            return

        n = len(cmd)
        curly_braces = find_matching(
            self.main, "{", "}", ignore_escaped=True, ignore_commented=ignore_commented
        )
        closing = sorted(curly_braces[i] for i in curly_braces)
        opening = np.array(sorted(i for i in curly_braces))
        next_opening = {}
        for i in closing:
            j = np.argmax(opening > i)
            next_opening[i] = opening[j]

        last = 0
        ret = ""

        if ignore_commented:
            comments = np.array(find_commented(self.main))
            if comments.size == 0:
                ignore_commented = False

        if ignore_commented:
            comments_start = comments[:, 0]
            comments_end = comments[:, 1]

        for match in re.finditer(re.escape(cmd) + "{", self.main):
            opening = match.span(0)[0] + n

            if opening < last:
                continue

            if ignore_commented:
                if np.any(np.logical_and(opening >= comments_start, opening < comments_end)):
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

        if ignore_commented:
            test = remove_comments(self.main)
        else:
            test = self.main

        if re.search(re.escape(cmd) + "{", test):
            return self._replace_command_impl(cmd, nargs, replace, ignore_commented)

    def replace_command(self, cmd: str, replace: str, ignore_commented: bool = False):
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

        :param ignore_commented:
            If ``True`` the command is not replaced if it is commented out.
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

        self._replace_command_impl(cmd, nargs, replace, ignore_commented=ignore_commented)

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

    def _reformat(self, label: str, key: str, prefix: str = None):
        """
        Reformat labels (and references) to f"{key}:{label}" (if needed).
        Suppose that the target is "fig:foo", this function also converts
        "FIG:foo", "fig-foo", "fig_foo", ...

        :param label: The label (with or without ``key:``).
        :param key: The 'keyword' to add/ensure.
        :param prefix: Add optional ``prefix`. E.g. ``key:prefix:...``.
        """

        ret = f"{key}"

        if prefix is not None:
            ret = f"{key}:{prefix}"

            for sep in [":", "-", "_"]:
                regex = re.compile(f"({key})({sep})({prefix})({sep})(.*)", re.IGNORECASE)
                if re.match(regex, label):
                    info = re.split(regex, label)[-2]
                    return f"{ret}:{info}"

        for sep in [":", "-", "_"]:
            regex = re.compile(f"({key})({sep})(.*)", re.IGNORECASE)
            if re.match(regex, label):
                info = re.split(regex, label)[-2]
                return f"{ret}:{info}"

        return f"{ret}:{label}"

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
        Return list with present environments (between ``\begin{...} ... \end{...}``).
        """
        return environments(self.main)

    def format_labels(self, prefix: str = None):
        """
        Format all labels as:

        *   ``sec:...``: Section labels.
        *   ``ch:...``: Chapter labels.
        *   ``fig:...``: Figure labels.
        *   ``tab:...``: Table labels.
        *   ``eq:...``: Math labels.

        :param prefix: Add optional ``prefix``. E.g. ``key:prefix:...``.
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
                    change[label] = self._reformat(label, key, prefix=prefix)
                    stop = True
                    break

            if stop:
                continue

            for h in headers:
                test = ilab > headers[h]
                if not np.any(test):
                    continue
                i = test.size - 1 if np.all(test) else np.argmin(test) - 1
                start = headers[h][i] + 1
                if re.match(r"([\s\n%]*)(\\label{)", self.main[start:]):
                    change[label] = self._reformat(label, iden[h], prefix=prefix)
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

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent(
            """\
            Apply some simple clean-up rules.
            Most of the options are fully self explanatory, except for:

            --replace-command
                It can replace a command by another command, or simply 'remove' it,
                keeping just a sequence of arguments.
                This option is very much like a LaTeX command, but applied to the source.
                For example::

                    --replace-command "{\\TG}[2]" "#1"

                Applied a change as follows::

                    >>> This is a \\TG{text}{test}.
                    <<< This is a test.

                Note that the number of arguments defaults to 1 (above ``[2]`` fixes 2 arguments).
                Finally, commented text is ignored.
            """
        ),
    )

    parser.add_argument(
        "-c",
        "--remove-commentlines",
        action="store_true",
        help="Remove all lines that have only comments (excluding preamble).",
    )

    parser.add_argument(
        "-C",
        "--remove-comments",
        action="store_true",
        help="Remove all comments (excluding preamble).",
    )

    parser.add_argument(
        "-r",
        "--replace-command",
        type=str,
        nargs=2,
        action="append",
        metavar=("cmd", "def"),
        help="Replace command (see above).",
    )

    parser.add_argument(
        "-l",
        "--change-label",
        type=str,
        nargs=2,
        action="append",
        metavar=("old", "new"),
        help="Rename a specific label.",
    )

    parser.add_argument(
        "-f",
        "--format-labels",
        action="store_true",
        help='Automatically prepend labels with "fig:", "eq:", "tab:", "sec:", "ch:" (if needed).',
    )

    parser.add_argument(
        "-F",
        "--prepend-format-labels",
        type=str,
        help='Automatically prepend labels with "fig:ARG", "eq:ARG", ...; see --format-labels.',
    )

    parser.add_argument(
        "-s",
        "--use-cleveref",
        action="store_true",
        help=r'Change "Fig.~\ref{...}" etc. to "\\cref{...}".',
    )

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
        tex = TeX.from_file(file)

        if args.remove_commentlines or args.remove_comments:
            tex.remove_commentlines()

        if args.remove_comments:
            tex.remove_comments()

        if args.replace_command:
            for i in args.replace_command:
                tex.replace_command(*i, ignore_commented=True)

        if args.change_label:
            for i in args.change_label:
                tex.change_label(*i)

        if args.format_labels:
            tex.format_labels()

        if args.prepend_format_labels:
            tex.format_labels(args.prepend_format_labels)

        if args.use_cleveref:
            tex.use_cleveref()

        if tex.changed():
            with open(file, "w") as file:
                file.write(tex.get())


def _texcleanup_cli():
    texcleanup(sys.argv[1:])


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

    old = TeX.from_file(args.input)
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


def _texplain_cli():
    texplain(sys.argv[1:])


def _texindent_latexindent(
    config: dict, text: str, tempdir: pathlib.Path, generate_filename: Callable
) -> str:
    """
    Run ``latexindent.pl`` on text.

    :param config: Configuration of ``latexindent.pl``.
    :param text: Text to format.
    :param tempdir: Temporary directory to write files to.
    :param generate_filename: Generator of filenames for temporary files ``tempdir / filename``.
    :return: Formatted text.
    """

    with open(tempdir / ".latexindent.yaml", "w") as f:
        yaml.dump(config, f)

    if generate_filename is not None:
        filename = generate_filename()
    else:
        filename = "main.tex"

    (tempdir / filename).write_text(text)

    subprocess.check_output(
        ["latexindent.pl", "-s", "-wd", "-l", "-m", "-r", filename], cwd=tempdir
    )

    return (tempdir / filename).read_text()


def _texindent_default(
    config: dict, text: str, tempdir: pathlib.Path, generate_filename: Callable
) -> str:
    """
    Run ``latexindent.pl`` with in addition to the user configuration the following settings:

    .. code-block:: yaml

        modifyLineBreaks:
            oneSentencePerLine:
                manipulateSentences: 0
                removeSentenceLineBreaks: 0

    :param config: Configuration of ``latexindent.pl``.
    :param text: Text to format.
    :param tempdir: Temporary directory to write files to.
    :param generate_filename: Generator of filenames for temporary files ``tempdir / filename``.
    :return: Formatted text.
    """

    rules = copy.deepcopy(config)

    if "modifyLineBreaks" in rules:
        if "oneSentencePerLine" in rules["modifyLineBreaks"]:
            rules["modifyLineBreaks"]["oneSentencePerLine"]["manipulateSentences"] = 0
            rules["modifyLineBreaks"]["oneSentencePerLine"]["removeSentenceLineBreaks"] = 0

    return _texindent_latexindent(rules, text, tempdir, generate_filename)


def _texindent_sentence(
    config: dict, text: str, tempdir: pathlib.Path, generate_filename: Callable
) -> str:
    """
    Run ``latexindent.pl`` if the following settings are present

    .. code-block:: yaml

        modifyLineBreaks:
            oneSentencePerLine:
                manipulateSentences: 0/1
                removeSentenceLineBreaks: 0/1

    Comments, math, environments, and commands are replaced with placeholders to make formatting
    a lot less aggressive.

    :param config: Configuration of ``latexindent.pl``.
    :param text: Text to format.
    :param tempdir: Temporary directory to write files to.
    :param generate_filename: Generator of filenames for temporary files ``tempdir / filename``.
    :return: Formatted text.
    """

    if "modifyLineBreaks" not in config:
        return text

    if "oneSentencePerLine" not in config["modifyLineBreaks"]:
        return text

    if (
        "manipulateSentences" not in config["modifyLineBreaks"]["oneSentencePerLine"]
        and "removeSentenceLineBreaks" not in config["modifyLineBreaks"]["oneSentencePerLine"]
    ):
        return text

    ret = TeX(text)

    format, placeholders = text_to_placeholders(
        ret.main,
        [
            PlacholderType.noindent_block,
            PlacholderType.comment,
            PlacholderType.inline_math,
            PlacholderType.special_indent,
            PlacholderType.command,
            PlacholderType.environment,
        ],
    )
    format = _texindent_latexindent(config, format, tempdir, generate_filename)

    for placeholder in placeholders:
        if placeholder.ptype == PlacholderType.command:
            if re.match(r"([^\{]*\{\n)(.*)", placeholder.content):
                if placeholder.content[-1] != "}":
                    continue
                content = re.split(
                    r"([^\{]*\{\n)(\s*)(.*)", placeholder.content[:-1].rstrip(), re.MULTILINE
                )
                command = content[1]
                indent = content[2]
                content = textwrap.dedent("".join(content[2:]))
                content, pl = text_to_placeholders(content, [PlacholderType.command], "SUBINDENT")
                content = _texindent_latexindent(config, content, tempdir, generate_filename)
                content = text_from_placeholders(
                    content, pl, default_naming=True, prefix="SUBINDENT"
                )
                if content[-1] != "\n":
                    content += "\n"
                placeholder.content = command + textwrap.indent(content + "}", indent)

    ret.main = "\n" + text_from_placeholders(format, placeholders)

    return ret.get()


def _detail_texindent(text: str, config: dict, tempdir: pathlib.Path, generate_filename: Callable):
    """
    See :py:func:`texindent`.
    """

    if generate_filename is not None:
        (tempdir / generate_filename()).write_text(text)

    # "latexindent.pl" formatting with configuration augmented by
    # - modifyLineBreaks/oneSentencePerLine/manipulateSentences = 0
    # - modifyLineBreaks/oneSentencePerLine/removeSentenceLineBreaks = 0
    text = _texindent_default(config, text, tempdir, generate_filename)

    # if set, formatting with
    # - modifyLineBreaks/oneSentencePerLine/manipulateSentences
    # - modifyLineBreaks/oneSentencePerLine/removeSentenceLineBreaks
    text = _texindent_sentence(config, text, tempdir, generate_filename)

    # "latexindent.pl" formatting with configuration augmented by
    # - modifyLineBreaks/oneSentencePerLine/manipulateSentences = 0
    # - modifyLineBreaks/oneSentencePerLine/removeSentenceLineBreaks = 0
    text = _texindent_default(config, text, tempdir, generate_filename)

    # remove trailing whitespaces
    text = "\n".join([line.rstrip() for line in text.splitlines()]) + "\n"

    return text


def texindent_default_config() -> dict:
    r"""
    Default configuration of ``latexindent.pl``.

    .. code-block:: yaml

        defaultIndent: '    '
        removeTrailingWhitespace: 1

        lookForAlignDelims:
            align:
                alignDoubleBackSlash: 0
            split:
                alignDoubleBackSlash: 0

        modifyLineBreaks:
            oneSentencePerLine:
                manipulateSentences: 1
                removeSentenceLineBreaks: 1
                multipleSpacesToSingle: 1
            items:
                ItemFinishesWithLineBreak: 1
            environments:
                BeginStartsOnOwnLine: 1
                BodyStartsOnOwnLine: 1
                EndStartsOnOwnLine: 1
                EndFinishesWithLineBreak: 1
                DBSFinishesWithLineBreak: 1

        indentRules:
            item: '    '

        fineTuning:
            namedGroupingBracesBrackets:
                # https://github.com/cmhughes/latexindent.pl/issues/330
                name: '[0-9\.a-zA-Z@\*><_]+?'
            arguments:
                # https://github.com/cmhughes/latexindent.pl/issues/416
                between: _|\^|\*|\|
    """

    text = texindent_default_config.__doc__
    text = textwrap.dedent(text.split(".. code-block:: yaml")[1])
    return yaml.load(text, Loader=yaml.FullLoader)


def texindent(
    text: str, config: dict, tempdir: pathlib.Path = None, generate_filename: Callable = None
) -> str:
    r"""
    Format text with ``latexindent.pl``.
    Augmented rules:

    -   A command and inline math inside a sentence is considered as a neutral placeholder.

    -   The whitespace before and after any command, environment, and comment are exactly preserved.

    -   The linebreaks of sentences inside commands are only changed if the command if formatted:

        .. code-block:: latex

            ... \mycommand{
                This is a
                sentence.
            }

        which is formatted to

        .. code-block:: latex

            ... \mycommand{
                This is a sentence.
            }

        Instead, the following formatting does not change the linebreaks inside the command:

        .. code-block:: latex

            ... \mycommand{This is a
                sentence.}

    :param text: Text to format.

    :param config: Configuration of ``latexindent.pl``, e.g. :py:func:`texindent_default_config`.

    :param tempdir:
        Temporary directory to write files to.
        If ``None`` a temporary directory is created, and removed after use.

    :param generate_filename:
        Generator of filenames for temporary files ``tempdir / filename``.
        If ```None`` a single filename is used.
        That file is overwritten on each call.

    :return: Formatted text.
    """

    if tempdir is None:
        assert generate_filename is None
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = pathlib.Path(tempdir)
            return _detail_texindent(text, config, tempdir, None)

    return _detail_texindent(text, config, tempdir, generate_filename)


def _texindent_parser():
    """
    Return parser for :py:func:`texindent`.
    """

    desc = "Wrapper around ``latexindent.pl`` with some additional rules. ``texplain.texindent``."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-c", "--config", type=str, help="Configuration file")
    parser.add_argument("-t", "--tempdir", type=str, help="Temporary directory")

    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("files", nargs="+", type=str, help="TeX file")

    return parser


def _detail_texindent_cli(
    filepath: str, config: dict, tempdir: pathlib.Path, generate_filename: Callable
):
    """
    See :py:func:`texindent_cli`.
    """

    filepath = pathlib.Path(filepath)
    orig = filepath.read_text()
    formatted = texindent(orig, config, tempdir, generate_filename)

    # copy back if modified
    if formatted != orig:
        filepath.write_text(formatted)


class _FilenameGenerator:
    """
    Class to generate filenames.
    """

    def __init__(self):
        self.i = 0

    def __call__(self):
        self.i += 1
        return f"texindent-stage-{self.i:03d}.tex"


def texindent_cli(args: list[str]):
    """
    Wrapper around latexindent.pl, see ``--help``.
    """

    parser = _texindent_parser()
    args = parser.parse_args(args)
    assert all([os.path.isfile(file) for file in args.files])

    if args.config is None:
        if os.path.isfile(".texindent.yaml"):
            args.config = ".texindent.yaml"
        elif os.path.isfile(".texindent.yml"):
            args.config = ".texindent.yml"
        elif os.path.isfile(".latexindent.yaml"):
            args.config = ".latexindent.yaml"
        elif os.path.isfile(".latexindent.yml"):
            args.config = ".latexindent.yml"
        else:
            config = texindent_default_config()
    else:
        assert os.path.isfile(args.config)

    if args.config is not None:
        with open(args.config) as file:
            config = yaml.load(file.read(), Loader=yaml.FullLoader)

    if args.tempdir is not None:
        assert len(args.files) == 1
        gen = _FilenameGenerator()
        return _detail_texindent_cli(args.files[0], config, pathlib.Path(args.tempdir), gen)

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        for filepath in args.files:
            _detail_texindent_cli(filepath, config, tempdir, None)


def _texindent_cli():
    texindent_cli(sys.argv[1:])


if __name__ == "__main__":
    pass
