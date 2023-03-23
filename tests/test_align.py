import unittest

import texplain


class TestAlignTabular(unittest.TestCase):
    """
    Alignment of tabular environments.
    """

    def test_align_no_newline(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_align_empty(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_align_nested(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_align_empty_leading_column(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_align_empty_column(self):
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
        self.assertEqual(ret.strip(), formatted.strip())


if __name__ == "__main__":
    unittest.main()
