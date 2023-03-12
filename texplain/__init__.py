import argparse
import enum
import itertools
import os
import pathlib
import re
import sys
import textwrap
from copy import deepcopy
from shutil import copyfile

import numpy as np
from numpy.typing import ArrayLike
from numpy.typing import NDArray

from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


class PlaceholderType(enum.Enum):
    """
    Type of placeholder.
    """

    inline_comment = enum.auto()
    comment = enum.auto()
    tabular = enum.auto()
    math = enum.auto()
    inline_math = enum.auto()
    math_line = enum.auto()
    environment = enum.auto()
    command = enum.auto()
    command_component = enum.auto()
    noindent_block = enum.auto()
    verbatim = enum.auto()
    special_indent = enum.auto()


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
    TODO: change to list(ret.items())
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
        if return_array:
            return np.zeros((0, 2), dtype=int)
        return {}

    if ignore_commented:
        is_comment = is_commented(text)
        a = np.array(a)
        b = -np.array(b)
        a = list(a[~is_comment[a]])
        b = list(-b[~is_comment[b]])

    if len(a) != len(b):
        raise IndexError(f"Unmatching {opening}...{closing} found")

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

def _detail_find_option(text: str, index: int, braces: ArrayLike, ret: list[tuple[int]]) -> list[tuple[int]]:

    if len(braces) == 0:
        return ret

    if braces[0] < 0:
        return ret

    if len(text[index:braces[0]].strip()) > 0:
        return ret

    stack = []

    for i, trial in enumerate(braces):
        trial = braces[i]
        if trial >= 0:
            stack.append(trial)
        else:
            if len(stack) == 0:
                raise IndexError(f"No closing closing bracket at: {text[index:abs(trial)]}")
            open = stack.pop()
            if len(stack) == 0:
                closing = -1 * trial
                break

    return _detail_find_option(text, closing + 1, braces[i + 1 :], ret + [(open, closing + 1)])

def _find_option(text: str, index: int, opening: ArrayLike, closing: ArrayLike) -> list[int]:

    if len(opening) == 0:
        return []

    braces = np.concatenate((opening, -np.array(closing)))
    braces = braces[np.argsort(np.abs(braces))]
    return _detail_find_option(text, index, braces, [])


def find_command(text: str, name: str = None, escape: bool = True, ignore_commented: bool = True) -> list[list[tuple[int]]]:
    """
    Find indices of command, and their arguments.

    :param text: Text.
    :param name: Name of command without backslash (e.g. ``"textbf"``).
    :param escape: If ``True``, ``name`` is escaped.
    :return: List of indices of commands and their arguments:
        ``[[(name_start, name_end), (arg1_start, arg1_end), ...], ...]``
        Note the definition is such that one can find the command name as follows:
        ``text[cmd[i][0]:cmd[i][1]]``.
    """

    if name is not None:
        if escape:
            name = re.escape(name)
        name = r"(?<!\\)(\\)" + name
    else:
        name = r"(?<!\\)(\\)([a-zA-Z]+)(\*?)"

    cmd_start = []
    cmd_end = []

    for i in re.finditer(name, text):
        cmd_start.append(i.span()[0])
        cmd_end.append(i.span()[1])

    if len(cmd_start) == 0:
        return []

    square_open = np.array([i.span()[0] for i in re.finditer(r"(?<!\\)(\[)", text)])
    square_closing = np.array([i.span()[0] for i in re.finditer(r"(?<!\\)(\])", text)])
    curly_open = np.array([i.span()[0] for i in re.finditer(r"(?<!\\)(\{)", text)])
    curly_closing = np.array([i.span()[0] for i in re.finditer(r"(?<!\\)(\})", text)])

    if ignore_commented:
        is_comment = is_commented(text)
        is_comment = np.append(is_comment, is_comment[-1])
        cmd_start = np.array(cmd_start)
        cmd_end = np.array(cmd_end)
        cmd_start = cmd_start[~is_comment[cmd_start]]
        cmd_end = cmd_end[~is_comment[cmd_end]]
        if square_open.size > 0:
            square_open = square_open[~is_comment[square_open]]
        if square_closing.size > 0:
            square_closing = square_closing[~is_comment[square_closing]]
        if curly_open.size > 0:
            curly_open = curly_open[~is_comment[curly_open]]
        if curly_closing.size > 0:
            curly_closing = curly_closing[~is_comment[curly_closing]]

    cmd_square_open = np.searchsorted(cmd_end, square_open, side="right") - 1
    cmd_square_closing = np.searchsorted(cmd_end, square_closing, side="right") - 1
    cmd_curly_open = np.searchsorted(cmd_end, curly_open, side="right") - 1
    cmd_curly_closing = np.searchsorted(cmd_end, curly_closing, side="right") - 1

    ret = []

    for icmd in range(len(cmd_end)):
        index = cmd_end[icmd]
        item = [(cmd_start[icmd], cmd_end[icmd])]
        i_square_open = square_open[cmd_square_open >= icmd]
        i_square_closing = square_closing[cmd_square_closing >= icmd]
        i_curly_open = curly_open[cmd_curly_open >= icmd]
        i_curly_closing = curly_closing[cmd_curly_closing >= icmd]

        might_have_opt = True

        if len(i_square_open) == 0:
            might_have_opt = False
        else:
            if len(i_curly_open) > 0:
                if i_curly_open[0] < i_square_open[0]:
                    might_have_opt = False

        if might_have_opt:

            opts = _find_option(text, index, i_square_open, i_square_closing)

            if len(opts) > 0:
                index = opts[-1][1]
                item += opts
                i_curly_open = i_curly_open[i_curly_open >= index]
                i_curly_closing = i_curly_closing[i_curly_closing >= index]

        args = _find_option(text, index, i_curly_open, i_curly_closing)

        if len(args) > 0:
            item += args

        ret += [item]

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
    text = text.splitlines()
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


def _rstrip_lines(text: str) -> str:
    """
    ``.rstrip()`` for each line.

    :param text: Text.
    :return: Formatted text.
    """
    return "\n".join([line.rstrip() for line in text.splitlines()])


def _lstrip_lines(text: str) -> str:
    """
    ``.rstrip()`` for each line.

    :param text: Text.
    :return: Formatted text.
    """
    return "\n".join([line.lstrip() for line in text.splitlines()])


def _dedent(text: str, partial: list[PlaceholderType]) -> str:
    """
    Remove indentation.

    #TODO: optional use of latexindent.pl to format tables
    """

    text, placholders = text_to_placeholders(text, partial, base="TEXDEDENT")

    text = _lstrip_lines(text)

    # keep common indentation table
    # TODO: make more clever
    for placeholder in placholders:
        tmp = placeholder.content.splitlines()
        placeholder.content = (
            tmp[0].lstrip() + "\n" + textwrap.dedent("\n".join(tmp[1:-1])) + "\n" + tmp[-1].lstrip()
        )
        placeholder.space_front = "\n"

    text = text_from_placeholders(text, placholders)

    return text


def _squashspaces(text: str, skip: list[PlaceholderType]) -> str:
    """
    Squash spaces.

    :param text: Text.
    :param skip: List of :py:class:`PlaceholderType` to skip.
    :return: Formatted text.
    """

    text, placholders = text_to_placeholders(text, skip, base="TEXSQUASH")
    text = re.sub(r"(\ +)", r" ", text)
    text = text_from_placeholders(text, placholders)
    return text


def _begin_end_one_separate_line(text: str) -> str:
    r"""
    Put ``\begin{...}`` and ``\\end{...}``, and ``\[`` and ``\]`` on separate lines.

    :param text: Text.
    :return: Formatted text.
    """

    # begin all ``\begin{...}``and ``\end{...}`` on newline
    # text, placeholders_inline_math = text_to_placeholders(text, [PlaceholderType.inline_math])
    text = re.sub(r"(\n?\ *)(?<!\\)(\\begin\{)", r"\n\2", text)
    text = re.sub(r"(\n?\ *)(?<!\\)(\\end\{)", r"\n\2", text)
    # end all ``\end{...}`` on newline
    text = re.sub(r"(?<!\\)(\\end\{[^\s]*)(\ *\n?)", r"\1\n", text)
    # end all ``\begin{...}[...]{...}`` on newline
    # - math
    text, placeholders_math = text_to_placeholders(text, [PlaceholderType.math], base="TEXBEGINEND")
    for placeholder in placeholders_math:
        placeholder.content = re.sub(
            r"(?<!\\)(\\begin{[^}]*})(\ *\n?)", r"\1\n", placeholder.content
        )
    # - non-math
    for i in re.finditer(r"\\begin{[^}]*}.+", text):
        start = i.span()[0] + 6
        tmp = text[start:].split("\n", 1)[0]
        start += _find_arguments(tmp)
        if text[start] != "\n":
            text = text[:start] + "\n" + text[start:]
    # - replace math
    text = text_from_placeholders(text, placeholders_math)

    # place all ``\[`` and ``\]`` on a new line
    text = re.sub(r"(\ +)(\\\[)", r"\n\2", text)
    text = re.sub(r"(\w)(\\\[)", r"\1\n\2", text)
    text = re.sub(r"(\\\[)(\ +)", r"\1\n", text)
    text = re.sub(r"(\ +)(\\\])", r"\n\2", text)
    text = re.sub(r"(\w)(\\\])", r"\1\n\2", text)
    text = re.sub(r"(\\\])(\ +)", r"\1\n", text)

    return text


def indent(text: str, indent: str = "    ") -> str:
    """
    Indent text.

    :param text: The text to indent.
    :param indent: The indentation to use.
    :return: The indented text.
    """

    # known limitation
    if re.match(r"(?<!\\)(\$)(?<!\\)(\$)", text):
        raise NotImplementedError("Panic: don't know to deal with double dollar signs")

    # remove leading/trailing newlines, and trailing whitespace
    text = _rstrip_lines(text.strip())

    # "noindent" blocks are kept exactly as they are
    text, placeholders_noindent = text_to_placeholders(
        text, [PlaceholderType.noindent_block, PlaceholderType.verbatim]
    )

    # remove leading/trailing duplicate newlines
    for placeholder in placeholders_noindent:
        placeholder.space_front = re.sub(r"\n\n+\ *", r"\n\n", placeholder.space_front)
        placeholder.space_front = re.sub(r"\ +", r" ", placeholder.space_front)
        placeholder.space_back = re.sub(r"\n\n+\ *", r"\n\n", placeholder.space_back)
        placeholder.space_back = re.sub(r"\ +", r" ", placeholder.space_back)

    # comments: exclude from formatting
    text, placeholders_comment = text_to_placeholders(text, [PlaceholderType.comment])
    text, placeholders_inline_comment = text_to_placeholders(text, [PlaceholderType.inline_comment])

    # line comments: remove leading whitespace
    for placeholder in placeholders_comment:
        placeholder.space_front = "\n"

    # inline comments: remove duplicate spaces
    for placeholder in placeholders_inline_comment:
        placeholder.space_front = re.sub(r"\ +", r" ", placeholder.space_front)

    # remove multiple newlines, duplicate spaces, and any leading whitespace
    text = re.sub(r"(\n\n+)", r"\n\n", text)
    text = _dedent(text, partial=[PlaceholderType.tabular])
    text = _squashspaces(text, skip=[PlaceholderType.tabular])

    # fold inline math
    text, placeholders_inline_math = text_to_placeholders(text, [PlaceholderType.inline_math])
    # inline math: always on one line
    for placeholder in placeholders_inline_math:
        placeholder.content = placeholder.content.replace("\n", " ")
        placeholder.content = re.sub(r"(\ +)", r" ", placeholder.content)
        placeholder.space_front = None
        placeholder.space_back = None

    #TODO: use find_command to place on a new line:
    # - ``\begin{...}``/ ``\end{...}``
    # - ``\[`` / ``\]``
    # - ``{`` /  ``}`` separated by at least one a new line
    # - ``[`` / ``]`` that are command options separated by at least one a new line
    #TODO: the latter can be combined with folding the has to be done for ``_begin_end_one_separate_line`` anyway

    # put ``\begin{...}``/ ``\end{...}`` and ``\[`` / ``\]`` on a newline
    text = _begin_end_one_separate_line(text)

    # apply one sentence per line
    #TODO: use partial command placeholders to do the formatting inside the command
    # check if it should be touched should be very easy as ``{`` and ``[`` are the first character
    text = _one_sentence_per_line(
        text, fold=[PlaceholderType.math, PlaceholderType.tabular, PlaceholderType.command]
    )

    # place comment placeholders where they belong to do indentation
    text = text_from_placeholders(text, placeholders_comment + placeholders_inline_comment)
    text, placeholders_comment = text_to_placeholders(
        text, [PlaceholderType.comment, PlaceholderType.inline_comment]
    )

    # fold math lines to simplify implementation
    text, pl = text_to_placeholders(text, [PlaceholderType.math_line])
    placeholders_comment += pl

    # get line number of each character
    lineno = np.empty(len(text), dtype=int)
    i = 0
    line = 0
    for line, match in enumerate(re.finditer(r"\n", text)):
        lineno[i : match.span()[0]] = line
        i = match.span()[0]
        lineno[i] = line
        i += 1
    lineno[i:] = line + 1

    # initialize indentation level
    indent_level = np.zeros(lineno[-1] + 1, dtype=int)

    # add indentation to all lines between ``\begin{...}`` and ``\end{...}``
    for env in environments(text) + [PlaceholderType.math]:
        if env == PlaceholderType.math:
            opening = r"\\\["
            closing = r"\\\]"
        elif env == "document":
            continue
        else:
            opening = r"\\begin{" + env + r"}"
            closing = r"\\end{" + env + r"}"
        indices = find_matching(
            text,
            opening,
            closing,
            escape=False,
            opening_match=1,
            closing_match=0,
            ignore_escaped=True,
            return_array=True,
        )
        for opening, closing in indices:
            indent_level[np.unique(lineno[opening:closing])[1:]] += 1

    # add indentation to all lines between ``{`` and ``}`` containing at least one ``\n``
    indices = find_matching(text, "{", "}", ignore_escaped=True, return_array=True)
    for i in np.argwhere(lineno[indices[:, 0]] != lineno[indices[:, 1]]).ravel():
        indent_level[lineno[indices[i, 0]] + 1 : lineno[indices[i, 1]]] += 1

    # add indentation to all lines between ``[`` and ``]`` containing at least one ``\n``
    #TODO: use find_command to only consider ``[`` and ``]`` that are command options
    indices = find_matching(text, "[", "]", ignore_escaped=True, return_array=True)
    for i in np.argwhere(lineno[indices[:, 0]] != lineno[indices[:, 1]]).ravel():
        indent_level[lineno[indices[i, 0]] + 1 : lineno[indices[i, 1]]] += 1

    # apply indentation
    text = text_from_placeholders(text, placeholders_comment)
    text = text.splitlines()
    for i in range(len(text)):
        text[i] = indent_level[i] * indent + text[i]
    text = "\n".join(text)

    text = text_from_placeholders(text, placeholders_inline_math + placeholders_noindent)
    return _rstrip_lines(text)


def _detail_one_sentence_per_line(text: str) -> str:
    """
    ??
    TODO: optional split characters such as ``;`` and ``:``
    """

    text = re.split(r"(?<=[\.\!\?])\s+", text)

    for i in range(len(text)):
        text[i] = re.sub("(\n[\\ \t]*)([\\w\\$\\(\\[\\`])", r" \2", text[i])

    return "\n".join(text)


def _one_sentence_per_line(
    text: str,
    fold: list[PlaceholderType] = [
        PlaceholderType.math,
        PlaceholderType.tabular,
        PlaceholderType.inline_math,
        PlaceholderType.command,
    ],
    base: str = "TEXONEPERLINE",
) -> str:
    """
    ??

    TODO: Read and keep indentation level.

    TODO: Store indentation level in commands replaced with placeholders.
    Apply it to reformatting of multi-line commands.

    TODO: Format multi-line commands recursively.
    """

    text, placeholders = text_to_placeholders(text, fold, base=base)

    # format in blocks separated by blocks between ``(start, end)`` in ``skip``
    skip = []

    # \begin{...}
    skip += [i.span() for i in re.finditer(r"(?<!\\)(\\)(begin\{\w*\}\s*)", text)]

    # \end{...}
    skip += [i.span() for i in re.finditer(r"(?<!\\)(\\)(end\{\w*\}\s*)", text)]

    # multiple newlines
    skip += [i.span() for i in re.finditer(r"(\n\n+)", text)]

    if len(skip) == 0:
        ret = _detail_one_sentence_per_line(text)
    else:
        skip = np.array(skip)
        skip = _filter_nested(skip[skip[:, 0].argsort()])
        keep = np.ones(skip.shape[0], dtype=bool)
        for i in range(skip.shape[0] - 1):
            if skip[i, 1] == skip[i + 1, 0]:
                skip[i + 1, 0] = skip[i, 0]
                keep[i] = False
        skip = skip[keep]

        ret = ""
        start = 0
        for s, e in skip:
            ret += _detail_one_sentence_per_line(text[start:s])
            ret += text[s:e]
            start = e
        ret += _detail_one_sentence_per_line(text[start:])

    # apply one sentence per line to multi-line commands
    for placeholder in placeholders:
        if placeholder.ptype == PlaceholderType.command:
            if not re.match(r".*\n.*", placeholder.content):
                continue

            braces = find_matching(
                placeholder.content, "{", "}", ignore_escaped=True, return_array=True
            ).tolist()
            braces += find_matching(
                placeholder.content, "[", "]", ignore_escaped=True, return_array=True
            ).tolist()
            braces = _filter_nested(np.array(braces))
            braces[:, 1] += 1

            content = [placeholder.content[: braces[0, 0]]]
            for o, c in braces:
                content += [placeholder.content[o:c]]
            content += [placeholder.content[braces[-1, 1] :]]

            for i in range(1, len(content) - 1):
                if not re.match(r".*\n.*", content[i]):
                    continue
                body = content[i][1:-1].strip()
                body = _one_sentence_per_line(
                    body, [PlaceholderType.command], f"TEXONEPERLINENESTED{i}"
                )
                content[i] = content[i][0] + "\n" + body + "\n" + content[i][-1]

            placeholder.content = "".join(content)

    return text_from_placeholders(ret, placeholders)


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
    :param search_placeholder:
        The regex used to search for the placeholder
        (optional, but speeds up greatly for batch searches).
    """

    def __init__(
        self,
        placeholder: str,
        content: str,
        space_front: str = None,
        space_back: str = None,
        ptype: PlaceholderType = None,
        search_placeholder: str = None,
    ):
        self.placeholder = placeholder
        self.content = content
        self.space_front = space_front
        self.space_back = space_back
        self.ptype = ptype
        self.search_placeholder = search_placeholder

    @classmethod
    def from_text(
        self,
        placeholder: str,
        text: str,
        start: int,
        end: int,
        ptype: PlaceholderType = None,
        search_placeholder: str = None,
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
        :param search_placeholder: The regex used to search the placeholder.
        :return: ``(Placeholder, text)`` where in ``text`` the placeholder is inserted.
        """
        pre = text[:start][::-1]
        post = text[end:]
        front = re.search(r"\s*", pre).end()
        back = re.search(r"\ *\n?", post).end()
        return (
            Placeholder(
                placeholder,
                text[start:end],
                pre[:front][::-1],
                post[:back],
                ptype,
                search_placeholder,
            ),
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
        else:
            pre = pre[::-1]

        if self.space_back is not None:
            back = re.search(r"\ *\n?", post).end()
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

    @property
    def search_placeholder(self) -> str:
        """
        Return the regex that can be used to search for the placeholder.
        """
        return f"-{self.base}-{self.name}-\\d+-"


def _filter_nested(indices: ArrayLike) -> ArrayLike:
    indices = indices[np.argsort(indices[:, 0])]
    keep = np.ones(len(indices), dtype=bool)

    last = 0
    for i in range(len(indices)):
        if indices[i, 0] < last:
            keep[i] = False
        else:
            last = indices[i, 1]

    return indices[keep]


def _apply_placeholders(
    text: str,
    indices: ArrayLike,
    base: str,
    name: str,
    ptype: PlaceholderType,
    filter_nested: bool = True,
    contains_comments: bool = True,
) -> tuple[str, list[Placeholder]]:
    """
    Replace text with placeholders.
    Note: nested placeholders are skipped.

    :param text: The text to consider.
    :param indices: A list of start and end indices of the text to be replaced by a placeholder.
    :param base: The base of the placeholder, see :py:class:`GeneratePlaceholder`.
    :param name: The name of the placeholder, see :py:class:`GeneratePlaceholder`.
    :param ptype: The type of placeholder, see :py:class:`PlaceholderType`.
    :param filter_nested: If ``True``, nested placeholders are skipped.
    :param contains_comments: If ``False``, the use ensures that the text does not contain comments.
    :return:
        ``(text, placeholders)`` where:
        - ``text`` is the text with the placeholders.
        - ``placeholders`` is a list of the placeholders that includes their original content.
    """

    if indices is None:
        return text, []

    if len(indices) == 0:
        return text, []

    if filter_nested:
        indices = _filter_nested(indices)

    gen = GeneratePlaceholder(base, name)
    search_placeholder = gen.search_placeholder
    assert re.match(search_placeholder, text) is None

    ret = []
    for i in range(indices.shape[0]):
        placeholder, text = Placeholder.from_text(
            gen(), text, indices[i, 0], indices[i, 1], ptype, search_placeholder
        )
        ret += [placeholder]
        indices -= len(placeholder.content) - len(placeholder.placeholder)

    return text, ret


def _find_arguments(text: str, start: int = 0, braces: dict = None) -> tuple[int, int]:
    """
    Find the index at which there are no more optional or required arguments.

    :param start: Index to start searching.
    """

    if braces is None:
        braces = find_matching(text, "{", "}", ignore_escaped=True)
        braces.update(find_matching(text, "[", "]", ignore_escaped=True))

    while True:
        index = re.search(r"(\s*)([\{\[])", text[start:])
        if index is None:
            return start
        if index.start() != 0:
            return start
        start = braces[index.end() + start - 1] + 1


def _detail_text_to_placholders(
    text: str, ptype: PlaceholderType, base: str, contains_comments: bool
) -> tuple[str, list[Placeholder]]:
    """
    ??
    """

    if ptype == PlaceholderType.noindent_block:
        indices = find_matching(
            text,
            r"%\s*\\begin{noindent}",
            r"%\s*\\end{noindent}",
            escape=False,
            closing_match=1,
            return_array=True,
        )
        return _apply_placeholders(text, indices, base, "noindent".upper(), ptype)

    if ptype == PlaceholderType.verbatim:
        indices = find_matching(
            text,
            r"\\begin{verbatim}",
            r"\\end{verbatim}",
            escape=False,
            closing_match=1,
            return_array=True,
        )
        return _apply_placeholders(text, indices, base, "verbatim".upper(), ptype)

    if ptype == PlaceholderType.tabular:
        indices = find_matching(
            text,
            r"\\begin{tabular}",
            r"\\end{tabular}",
            escape=False,
            closing_match=1,
            return_array=True,
        )
        return _apply_placeholders(text, indices, base, "tabular".upper(), ptype)

    if ptype == PlaceholderType.inline_comment:
        indices = [i.span(2) for i in re.finditer(r"([^\ ][\ ]*)(?<!\\)(%.*)", text)]
        if len(indices) == 0:
            return text, []
        indices = np.array(indices)
        return _apply_placeholders(text, indices, base, "inline-comment".upper(), ptype, False)

    if ptype == PlaceholderType.comment:
        indices = [i.span(3) for i in re.finditer(r"(^|\n)(\ *)(?<!\\)(%.*)", text)]
        if len(indices) == 0:
            return text, []
        indices = np.array(indices)
        return _apply_placeholders(text, indices, base, "comment".upper(), ptype, False)

    if ptype == PlaceholderType.environment:
        indices = find_matching(
            text, r"\\begin{.*}", r"\\end{.*}", escape=False, closing_match=1, return_array=True
        )
        return _apply_placeholders(text, indices, base, "environment".upper(), ptype)

    if ptype == PlaceholderType.math or ptype == PlaceholderType.math_line:
        indices = []
        for env in ["equation", "equation*", "align", "align*"]:
            indices += find_matching(
                text,
                r"\\begin{" + env + "}",
                r"\\end{" + env + "}",
                escape=False,
                closing_match=1,
                return_array=True,
            ).tolist()
        indices += find_matching(
            text, r"\\\[", r"\\\]", escape=False, closing_match=1, return_array=True
        ).tolist()

        if ptype == PlaceholderType.math:
            indices = np.array(indices)
            return _apply_placeholders(text, indices, base, "math".upper(), ptype)

        all_indices = []
        for starting, closing in indices:
            lines = text[starting:closing].splitlines()
            starting += len(lines[0]) + 1
            for line in lines[1:-1]:
                skip = False
                if re.match(r"(?<!\\)(\\begin{)", line):
                    skip = True
                if re.match(r"(?<!\\)(\\end{)", line):
                    skip = True
                n = len(line)
                if not skip:
                    all_indices += [[starting, starting + n]]
                starting += n + 1
        indices = np.array(all_indices)
        return _apply_placeholders(text, indices, base, "math-line".upper(), ptype)

    if ptype == PlaceholderType.math_line:
        consider = []
        for env in ["equation", "equation*", "align", "align*"]:
            consider += find_matching(
                text,
                r"\\begin{" + env + "}",
                r"\\end{" + env + "}",
                escape=False,
                closing_match=1,
                return_array=True,
            ).tolist()
        consider += find_matching(
            text, r"\\\[", r"\\\]", escape=False, closing_match=1, return_array=True
        ).tolist()

        indices = np.array(indices)
        return _apply_placeholders(text, indices, base, "math".upper(), ptype, False)

    if ptype == PlaceholderType.inline_math:
        ret = []
        pattern = r"(?<!\\)(\$)"
        indices = []
        for i in re.finditer(pattern, text):
            indices.append(i.span()[0])
        indices = np.array(indices).reshape((-1, 2))
        indices[:, 1] += 1
        text, placeholders = _apply_placeholders(text, indices, base, "inlinemath".upper(), ptype)
        for placeholder in placeholders:
            placeholder.space_front = None
            placeholder.space_back = None
        ret += placeholders

        indices = find_matching(
            text, r"\\\(", r"\\\)", escape=False, closing_match=1, return_array=True
        )
        text, placeholders = _apply_placeholders(text, indices, base, "inlinemath".upper(), ptype)
        ret += placeholders

        indices = find_matching(
            text, r"\\begin{math}", r"\\end{math}", escape=False, closing_match=1, return_array=True
        )
        text, placeholders = _apply_placeholders(text, indices, base, "inlinemath".upper(), ptype)
        ret += placeholders

        return text, ret

    if ptype == PlaceholderType.command:
        components = find_command(text, ignore_commented=not contains_comments)
        indices = []

        for component in components:
            if text[component[0][0]:component[0][1]] in [r"\\begin", r"\\end"]:
                continue
            indices += [[component[0][0], component[-1][1]]]

        indices = np.array(indices)
        return _apply_placeholders(text, indices, base, "command".upper(), ptype)

    #TODO: add placeholder for partial commands

    raise ValueError(f"Unknown placeholder type: {ptype}")


def text_to_placeholders(
    text: str, ptypes: list[PlaceholderType], base: str = "TEXINDENT", contains_comments: bool = True
) -> tuple[str, list[Placeholder]]:
    r"""
    Replace text with placeholders.
    The following placeholders are supported:

    -   :py:class:`PlaceholderType.noindent_block`:

        .. code-block:: latex

            % \begin{noindent}
            ...
            % \end{noindent}

    -   :py:class:`PlaceholderType.verbatim`:

        .. code-block:: latex

            \begin{verbatim}
            ...
            \end{verbatim}

    -   :py:class:`PlaceholderType.comment`:

        .. code-block:: latex

            % ...

    -   :py:class:`PlaceholderType.inline_math`:

        .. code-block:: latex

            $...$

    -   :py:class:`PlaceholderType.environment`:

        .. code-block:: latex

            \begin{...}
            ...
            \end{...}


    :param contains_comments: If ``False`` the user ensures that the text does not contain comments.
    """

    ret = []

    for ptype in ptypes:
        text, placeholders = _detail_text_to_placholders(text, ptype, base, contains_comments)
        ret += placeholders

    return text, ret


def text_from_placeholders(
    text: str,
    placeholders: list[Placeholder],
) -> str:
    """
    Replace placeholders with original text.
    """

    if len(placeholders) == 0:
        return text

    search_placeholder = []

    if len(placeholders) > 1:
        search_placeholder = list({i.search_placeholder for i in placeholders})

    placeholders = {i.placeholder: i for i in placeholders}

    for search in search_placeholder:
        if search is None:
            continue
        indices = {text[i.span()[0] : i.span()[1]]: i.span()[0] for i in re.finditer(search, text)}
        offset = 0
        for key, index in indices.items():
            placeholder = placeholders.pop(key, None)
            if placeholder is None:
                continue
            n = len(text)
            text = placeholder.to_text(text, index + offset)
            offset += len(text) - n
            if len(placeholders) == 0:
                return text

    for key in placeholders:
        placeholder = placeholders[key]
        n = len(text)
        text = placeholder.to_text(text)

    return text


def _classify_for_label(text: str) -> tuple[list[str], NDArray[np.int_]]:
    """
    Classify characters to identify to which environment a label belongs.

    :param text: The text to classify.
    :return:
        ``(categories, classification)`` where ``categories`` is the list of label categories
        ``"eq"``, ``"fig"``, etc.) and ``classification`` is an array of the same length as ``text``
        where each element is the index of the category to which the character belongs.
    """

    categories = ["misc", "eq", "item", "note", "sec", "ch", "fig", "tab"]
    classification = np.zeros(len(text), dtype=int)
    braces = find_matching(text, "{", "}", ignore_escaped=True)

    # ---

    r = -1

    for match in re.finditer(r"(\s*\\label\s*\{)", text):
        i = match.span()[0]
        j = braces[match.span()[1] - 1]
        classification[i:j] = r
        r -= 1

    # ---

    r = categories.index("eq")

    index = find_matching(
        text,
        r"\\begin\{equation\*?\}",
        r"\\end\{equation\*?\}",
        escape=False,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    index = find_matching(
        text,
        r"\\begin\{align\*?\}",
        r"\\end\{align\*?\}",
        escape=False,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    index = find_matching(
        text,
        r"\\begin\{eqnarray\*?\}",
        r"\\end\{eqnarray\*?\}",
        escape=False,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    # ---

    r = categories.index("fig")

    index = find_matching(
        text,
        r"\begin{figure}",
        r"\end{figure}",
        escape=True,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    # ---

    r = categories.index("tab")

    index = find_matching(
        text,
        r"\begin{table}",
        r"\end{table}",
        escape=True,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    # ---

    r = categories.index("item")

    index = find_matching(
        text,
        r"\begin{itemize}",
        r"\end{itemize}",
        escape=True,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    index = find_matching(
        text,
        r"\begin{enumerate}",
        r"\end{enumerate}",
        escape=True,
        closing_match=1,
    )
    for i, j in index.items():
        classification[i:j] = r

    # ---

    r = categories.index("note")

    for match in re.finditer(r"(\\footnote\s*\{)", text):
        i = match.span()[0]
        j = braces[match.span()[1] - 1]
        classification[i:j] = r

    # ---

    r = categories.index("sec")

    for match in re.finditer(r"(\\)(sub)*(section\s*\{)", text):
        i = match.span()[0]
        j = braces[match.span()[1] - 1]
        classification[i:j] = r

        if classification[j + 1] < 0:
            classification[classification == classification[j + 1]] = r

    # ---

    r = categories.index("ch")

    for match in re.finditer(r"(\\)(chapter\s*\{)", text):
        i = match.span()[0]
        j = braces[match.span()[1] - 1]
        classification[i:j] = r

        if classification[j + 1] < 0:
            classification[classification == classification[j + 1]] = r

    return categories, classification


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
        #TODO: improve
        """
        tmp_start = self.start
        tmp_main = self.main

        if len(tmp_start) > 0:
            if tmp_start[-1] != "\n":
                tmp_start += "\n"

            if tmp_start[-2] != "\n":
                tmp_start += "\n"

        if len(self.postamble) > 0:
            if tmp_main[-1] != "\n":
                tmp_main += "\n"

            if tmp_main[-2] != "\n":
                tmp_main += "\n"

        return self.preamble + tmp_start + tmp_main + self.postamble

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

        tmp = self.main.splitlines()
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
        *   ``note:...``: Footnote.
        *   ``misc:...``: Anything else.

        :param prefix: Add optional ``prefix``. E.g. ``key:prefix:...``.
        """

        categories, classification = _classify_for_label(self.main)
        change = {}

        for label in self.labels():
            i = self.main.index(rf"\label{{{label}}}")
            c = self._reformat(label, categories[classification[i]], prefix=prefix)
            if c != label:
                change[label] = c

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


def _texindent_parser():
    """
    Return parser for :py:func:`texindent`.
    """

    desc = "Wrapper around ``latexindent.pl`` with some additional rules. ``texplain.texindent``."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("files", nargs="+", type=str, help="TeX file")

    return parser


def texindent_cli(args: list[str]):
    """
    Wrapper around latexindent.pl, see ``--help``.
    """

    parser = _texindent_parser()
    args = parser.parse_args(args)
    assert all([os.path.isfile(file) for file in args.files])

    for filepath in args.files:
        filepath = pathlib.Path(filepath)
        orig = filepath.read_text()

        tex = TeX(orig)
        tex.main = indent(tex.main)
        formatted = tex.get()

        if formatted != orig:
            filepath.write_text(formatted)


def _texindent_cli():
    texindent_cli(sys.argv[1:])


if __name__ == "__main__":
    pass
