import texplain


def test_placeholders_select():
    """
    Implementation of :py:class:`texplain.Placeholder`.
    """
    text = r"foo \footnote{bar} baz"
    placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
    assert repl == "foo place baz"
    assert text == placeholder.to_text(repl)

    text = "foo\n\\footnote{bar} baz"
    placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
    assert placeholder.content == r"\footnote{bar}"
    assert repl == "foo\nplace baz"
    assert text == placeholder.to_text(repl)
    assert text == placeholder.to_text("foo place baz")
    assert text == placeholder.to_text("foo   place   baz")

    text = "foo\n\\footnote{bar}\nbaz"
    placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
    assert placeholder.content == r"\footnote{bar}"
    assert repl == "foo\nplace\nbaz"
    assert text == placeholder.to_text(repl)
    assert text == placeholder.to_text("foo place baz")
    assert text == placeholder.to_text("foo   place   baz")

    text = "foo\n    \\footnote{bar}\nbaz"
    placeholder, repl = texplain.Placeholder.from_text("place", text, 4 + 4, 18 + 4)
    assert placeholder.content == r"\footnote{bar}"
    assert repl == "foo\n    place\nbaz"
    assert text == placeholder.to_text(repl)
    assert text == placeholder.to_text("foo place baz")
    assert text == placeholder.to_text("foo   place   baz")


def test_placeholders_noindent():
    """
    Replace noindent with placeholders.
    """

    text = r"""
This is a text
%\begin{noindent}
should be ignored
%\end{noindent}
More text.

Bla bla bla.
% \begin{noindent}
should also be ignored
% \end{noindent}
A last sentence.
"""

    expect = r"""
This is a text
-TEXINDENT-NOINDENT-1-
More text.

Bla bla bla.
-TEXINDENT-NOINDENT-2-
A last sentence.
"""

    change_indent = r"""
This is a text -TEXINDENT-NOINDENT-1- More text.

Bla bla bla. -TEXINDENT-NOINDENT-2- A last sentence.
"""

    ret, placeholders = texplain.text_to_placeholders(
        text, [texplain.PlaceholderType.noindent_block]
    )
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)
    assert text == texplain.text_from_placeholders(change_indent, placeholders)
    assert expect == texplain.text_from_placeholders(change_indent, placeholders, True)


def test_placeholders_comments():
    """
    Replace comments with placeholders.
    """

    text = r"""
This is a text% with some inline comment
More text.
% A free comment
"""

    expect = r"""
This is a text-TEXINDENT-INLINE-COMMENT-1-
More text.
-TEXINDENT-COMMENT-1-
"""

    ret, placeholders = texplain.text_to_placeholders(
        text, [texplain.PlaceholderType.comment, texplain.PlaceholderType.inline_comment]
    )
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)


def test_placeholders_environment():
    """
    Replace environment with placeholders.
    """

    text = r"""
This is a text
\begin{equation}
    \begin{split}
        a = 10 \\
        a = 20.
    \end{split}
\end{equation}
More text.
Even more text.
\begin{equation}
    b = 20.
\end{equation}

Bla bla bla.
\begin{equation}
    c = 30.
\end{equation}
A last sentence.
"""

    expect = r"""
This is a text
-TEXINDENT-ENVIRONMENT-1-
More text.
Even more text.
-TEXINDENT-ENVIRONMENT-2-

Bla bla bla.
-TEXINDENT-ENVIRONMENT-3-
A last sentence.
"""

    ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlaceholderType.environment])
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)


def test_placeholders_math():
    text = r"""
This is a text
$a = 10\$$.
More text.
$a = 20$.
Even more text.
$b = 20$.
Bla bla bla.
$c = 30$.
A last sentence.
"""

    expect = r"""
This is a text
-TEXINDENT-INLINEMATH-1-.
More text.
-TEXINDENT-INLINEMATH-2-.
Even more text.
-TEXINDENT-INLINEMATH-3-.
Bla bla bla.
-TEXINDENT-INLINEMATH-4-.
A last sentence.
"""

    ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlaceholderType.inline_math])
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)


def test_placeholders_command():
    text = r"""
This is a text \command[foo]{arg1} {arg2} with
\foo

\bar

some \TG{\text{...}}
"""

    expect = r"""
This is a text -TEXINDENT-COMMAND-1- with
-TEXINDENT-COMMAND-2-

-TEXINDENT-COMMAND-3-

some -TEXINDENT-COMMAND-4-
"""

    ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlaceholderType.command])
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)


def test_placeholders_command_a():
    text = r"""
\section*{Foo} bar
"""

    expect = r"""
-TEXINDENT-COMMAND-1- bar
"""

    ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlaceholderType.command])
    assert ret == expect
    assert text == texplain.text_from_placeholders(ret, placeholders)
