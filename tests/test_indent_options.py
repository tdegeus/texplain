import texplain


def test_noindent_verbatim():
    text = r"""
Some text   \begin{verbatim} a = b \end{verbatim}    some more text.
"""

    formatted = r"""
Some text
\begin{verbatim}
    a = b
\end{verbatim}
some more text.
"""

    ret = texplain.indent(text, noindent=False)
    assert ret.strip() == formatted.strip()


def test_squash_spaces():
    text = r"""
This is  a long
sentence. With   some
spaces.
"""

    formatted = r"""
This is  a long sentence.
With   some spaces.
"""

    ret = texplain.indent(text, squashspaces=False)
    assert ret.strip() == formatted.strip()


def test_squash_lines():
    text = r"""
This is  a long
sentence. With   some
spaces.


And too many
white  lines.
"""

    formatted = r"""
This is a long sentence.
With some spaces.


And too many white lines.
"""

    ret = texplain.indent(text, squashlines=False)
    assert ret.strip() == formatted.strip()


def test_environment():
    text = r"""
This a text \begin{math} a = b \end{math} with \begin{equation} a = b \end{equation} some math.
"""

    formatted = r"""
This a text \begin{math} a = b \end{math} with \begin{equation} a = b \end{equation} some math.
"""

    ret = texplain.indent(text, environment=False, indentation=False)
    assert ret.strip() == formatted.strip()


def test_environment_inline():
    text = r"""
This a text \begin{math} a = b
\end{math} with \begin{equation} a = b \end{equation} some math.
"""

    formatted = r"""
This a text \begin{math} a = b
\end{math} with
\begin{equation}
a = b
\end{equation}
some math.
"""

    ret = texplain.indent(text, inlinemath=False, indentation=False)
    assert ret.strip() == formatted.strip()


def test_environment_linebreak():
    text = r"""
First \\ second \\ third.
"""

    formatted = r"""
First \\ second \\ third.
"""

    ret = texplain.indent(text, linebreak=False)
    assert ret.strip() == formatted.strip()


def test_sentence_multiline():
    text = r"""
This is a
long sentence.

And another
following sentence.
"""

    formatted = r"""
This is a
long sentence.

And another
following sentence.
"""

    ret = texplain.indent(text, sentence=False)
    assert ret.strip() == formatted.strip()


def test_argument_multiline():
    text = r"""
This is a \footenote{With a
footnote}
long sentence.

And another
following sentence.
"""

    formatted = r"""
This is a \footenote{
    With a
    footnote
}
long sentence.

And another
following sentence.
"""

    ret = texplain.indent(text, sentence=False, argument=True)
    assert ret.strip() == formatted.strip()

    formatted = r"""
This is a \footenote{
    With a footnote
}
long sentence.

And another following sentence.
"""

    ret = texplain.indent(text, sentence=True, argument=True)
    assert ret.strip() == formatted.strip()

    formatted = r"""
This is a \footenote{With a
footnote}
long sentence.

And another
following sentence.
"""

    ret = texplain.indent(text, sentence=False, argument=False)
    assert ret.strip() == formatted.strip()

    formatted = r"""
This is a \footenote{With a
footnote}
long sentence.

And another following sentence.
"""

    ret = texplain.indent(text, sentence=True, argument=False)
    assert ret.strip() == formatted.strip()
