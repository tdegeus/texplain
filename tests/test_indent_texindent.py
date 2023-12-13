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
