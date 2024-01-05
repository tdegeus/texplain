import texplain


def test_tabular_align_no_newline():
    text = r"""
\begin{tabular}{ccc}
a & b & c \\
1 & 2 & 3 \\
40 & 50 & 60
\end{tabular}
"""

    formatted = r"""
\begin{tabular}{ccc}
    a  & b  & c  \\
    1  & 2  & 3  \\
    40 & 50 & 60
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_align_empty():
    text = r"""
\begin{tabular}[t]{c}%
\@author
\end{tabular}
"""

    formatted = r"""
\begin{tabular}[t]{c}%
    \@author
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_align_nested():
    text = r"""
{
\begin{tabular}[t]{c}%
\@author % foo
\end{tabular}
}
"""

    formatted = r"""
{
    \begin{tabular}[t]{c}%
        \@author % foo
    \end{tabular}
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_align_empty_leading_column():
    text = r"""
\begin{tabular}[t]{ccc}
& foo & foobar \\
1 & 2 & 3 \\
4 & 5 & 6
\end{tabular}
"""

    formatted = r"""
\begin{tabular}[t]{ccc}
      & foo & foobar \\
    1 & 2   & 3      \\
    4 & 5   & 6
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_align_empty_column():
    text = r"""
\begin{tabular}[t]{ccc}
& foo & foobar \\
& 2 & 3 \\
& 5 & 6
\end{tabular}
"""

    formatted = r"""
\begin{tabular}[t]{ccc}
    & foo & foobar \\
    & 2   & 3      \\
    & 5   & 6
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_overflow():
    text = r"""
\begin{tabular}{lll}
    \toprule
    Foo & Bar  & Baz   \\
    \midrule
    $a$ & $b = 1000$ & $e$  \\
    $c'$ & $d = 2$ & $f'$ \\
    this is a very long column with a lot of text, this is a very long column with a lot of text & this is a very long column with a lot of text, this is a very long column with a lot of text & short \\
    \bottomrule
\end{tabular}
"""

    formatted = r"""
\begin{tabular}{lll}
    \toprule
    Foo & Bar & Baz \\
    \midrule
    $a$ & $b = 1000$ & $e$ \\
    $c'$ & $d = 2$ & $f'$ \\
    this is a very long column with a lot of text, this is a very long column with a lot of text & this is a very long column with a lot of text, this is a very long column with a lot of text & short \\
    \bottomrule
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_math():
    text = r"""
\begin{tabular}{lll}
    \toprule
    Foo & Bar  & Baz   \\
    \midrule
    $a$ & $b = 1000$ & $e$  \\
    $c'$ & $d = 2$ & $f'$ \\
    \bottomrule
\end{tabular}
"""

    formatted = r"""
\begin{tabular}{lll}
    \toprule
    Foo  & Bar        & Baz  \\
    \midrule
    $a$  & $b = 1000$ & $e$  \\
    $c'$ & $d = 2$    & $f'$ \\
    \bottomrule
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_tabular_math_empty():
    text = r"""
\begin{tabular}{lll}
    \toprule
    Foo & Bar  & Baz   \\
    \midrule
    $a$ & & $e$  \\
    $c'$ & $d = 2$ & $f'$ \\
    \bottomrule
\end{tabular}
"""

    formatted = r"""
\begin{tabular}{lll}
    \toprule
    Foo  & Bar     & Baz  \\
    \midrule
    $a$  &         & $e$  \\
    $c'$ & $d = 2$ & $f'$ \\
    \bottomrule
\end{tabular}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()
