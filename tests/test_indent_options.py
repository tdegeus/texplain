import unittest

import texplain


class TestNoindent(unittest.TestCase):
    def test_verbatim(self):
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
        self.assertEqual(ret.strip(), formatted.strip())


class TestSquash(unittest.TestCase):
    def test_spaces(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_lines(self):
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
        self.assertEqual(ret.strip(), formatted.strip())


class TestEnvironment(unittest.TestCase):
    def test_environment(self):
        text = r"""
This a text \begin{math} a = b \end{math} with \begin{equation} a = b \end{equation} some math.
        """

        formatted = r"""
This a text \begin{math} a = b \end{math} with \begin{equation} a = b \end{equation} some math.
        """

        ret = texplain.indent(text, environment=False, indentation=False)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_inline(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_linebreak(self):
        text = r"""
First \\ second \\ third.
        """

        formatted = r"""
First \\ second \\ third.
        """

        ret = texplain.indent(text, linebreak=False)
        self.assertEqual(ret.strip(), formatted.strip())


class TestSentence(unittest.TestCase):
    def test_multiline(self):
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
        self.assertEqual(ret.strip(), formatted.strip())


class TestArgument(unittest.TestCase):
    def test_multiline(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

        formatted = r"""
This is a \footenote{
    With a footnote
}
long sentence.

And another following sentence.
        """

        ret = texplain.indent(text, sentence=True, argument=True)
        self.assertEqual(ret.strip(), formatted.strip())

        formatted = r"""
This is a \footenote{With a
footnote}
long sentence.

And another
following sentence.
        """

        ret = texplain.indent(text, sentence=False, argument=False)
        self.assertEqual(ret.strip(), formatted.strip())

        formatted = r"""
This is a \footenote{With a
footnote}
long sentence.

And another following sentence.
        """

        ret = texplain.indent(text, sentence=True, argument=False)
        self.assertEqual(ret.strip(), formatted.strip())


if __name__ == "__main__":
    unittest.main()
