import pytest

import texplain


def test_sentence_simple():
    text = r"""
This is
a text.
% \begin{texindent}{sentence=False}
This is a
long sentence.
% \end{texindent}
And
some
more text.
"""

    formatted = r"""
This is a text.
% \begin{texindent}{sentence=False}
This is a
long sentence.
% \end{texindent}
And some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_sentence_squash():
    text = r"""
This is
a text.



% \begin{texindent}{sentence=False}
This is a
long sentence.
% \end{texindent}



And
some
more text.
"""

    formatted = r"""
This is a text.

% \begin{texindent}{sentence=False}
This is a
long sentence.
% \end{texindent}

And some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_arguments():
    text = r"""
\hypersetup{
    pdftitle=\@title,
    citecolor=NavyBlue,
    filecolor=NavyBlue,
    linkcolor=NavyBlue,
    urlcolor=NavyBlue,
breaklinks,bookmarksopen=true,
}
"""

    formatted = r"""
\hypersetup{
    pdftitle=\@title,
    citecolor=NavyBlue,
    filecolor=NavyBlue,
    linkcolor=NavyBlue,
    urlcolor=NavyBlue,
    breaklinks,
    bookmarksopen=true,
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


@pytest.mark.skip(reason="TODO: decide how to handle this case.")
def test_arguments_comment():
    text = r"""
\hypersetup{%
    pdftitle=\@title,
    citecolor=NavyBlue,
    filecolor=NavyBlue,
    linkcolor=NavyBlue,
    urlcolor=NavyBlue,
breaklinks,bookmarksopen=true,
}
"""

    formatted = r"""
\hypersetup{%
    pdftitle=\@title,
    citecolor=NavyBlue,
    filecolor=NavyBlue,
    linkcolor=NavyBlue,
    urlcolor=NavyBlue,
    breaklinks,
    bookmarksopen=true,
}
"""
    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_arguments_nargs_below():
    text = r"""
\hypersetup{
    pdftitle=\@title,citecolor=NavyBlue}
"""

    formatted = r"""
\hypersetup{
    pdftitle=\@title,
    citecolor=NavyBlue
}
"""
    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_arguments_nargs_above():
    text = r"""
\hypersetup{
    pdftitle=\@title,citecolor=NavyBlue,bookmarksopen=true}
"""

    formatted = r"""
\hypersetup{
    pdftitle=\@title,
    citecolor=NavyBlue,
    bookmarksopen=true
}
"""
    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_arguments_false_detection():
    text = r"""
\footnote{
    This is a text: A = B, C = D, E = F.
}.
"""
    formatted = text
    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()
