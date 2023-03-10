import unittest

import texplain

class TestComment(unittest.TestCase):

    def test_comment_a(self):

        text = r"This is a % comment"

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_comment_b(self):

        text = r"This is a. % comment"

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_comment_c(self):

        text = "This is a. % comment a\nAnd another. % comment b"

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())



class TestIndentEnvironment(unittest.TestCase):

    def test_environment(self):

        text = r"""
Some text \begin{equation} a = b \end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{equation}
    a = b
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_a(self):

        text = r"""
Some text \begin{equation}a = b\end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{equation}
    a = b
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_nested_a(self):

        text = r"""
Some text \begin{equation} \begin{split} a = b \end{split} \end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{equation}
    \begin{split}
        a = b
    \end{split}
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_nested_b(self):

        text = r"""
Some text \begin{equation} \begin{equation} a = b \end{equation} \end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{equation}
    \begin{equation}
        a = b
    \end{equation}
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_nested_c(self):

        text = r"""
Some text
\begin{equation}
\begin{equation}
\begin{equation}
\begin{equation}
a = b
\end{equation}
\end{equation}
\end{equation}
\end{equation}
some more text.
        """

        formatted = r"""
Some text
\begin{equation}
    \begin{equation}
        \begin{equation}
            \begin{equation}
                a = b
            \end{equation}
        \end{equation}
    \end{equation}
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_multiline_a(self):

        text = r"""
Some text \begin{figure}
 \foo
 \bar \end{figure} some more text.
        """

        formatted = r"""
Some text
\begin{figure}
    \foo
    \bar
\end{figure}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_multiline_b(self):

        text = r"""
Some text \begin{figure}
 \foo
 \bar \end{figure} \begin{equation} a = b \end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{figure}
    \foo
    \bar
\end{figure}
\begin{equation}
    a = b
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment_comment(self):

        text = r"""
Some text \begin{equation} % some comment
a = b \end{equation} some more text.
        """

        formatted = r"""
Some text
\begin{equation} % some comment
    a = b
\end{equation}
some more text.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())



class TestIndentCommand(unittest.TestCase):

    def test_command_punctuation(self):

        text = r"""
A start\footnote{
    This is a footnote
}.
A new sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_command_punctuation_a(self):

        text = r"""
A start\footnote{
    This is a footnote
}
a continued sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_command_punctuation_b(self):

        text = r"""
\section{My? section}
\label{sec:a}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_label_equation(self):

        text = r"""
\begin{equation}
    \label{eq:a}
    a = b
\end{equation}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_nested_command(self):

        text = r"""
\begin{figure}
    \subfloat{\label{fig:foo}}
\end{figure}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())


class TestOneSentencePerLine(unittest.TestCase):

    def test_quote(self):

        text = r"""
This a ``sentence!'' And another.
        """

        formatted = r"""
This a ``sentence!'' And another.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_full_quote(self):

        text = r"""
``This a sentence!'' And
another.
        """

        formatted = r"""
``This a sentence!'' And another.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_brace(self):

        text = r"""
This a sentence. And another
(etc.).
        """

        formatted = r"""
This a sentence.
And another (etc.).
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_full_brace(self):

        text = r"""
(This a sentence.) (This a second sentence.) And another. And one more (?).
        """

        formatted = r"""
(This a sentence.) (This a second sentence.) And another.
And one more (?).
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_comment_a(self):

        text = r"""
This is % some comment
a sentence.
And
here
is
another.
With a % another comment
final statement.
        """

        formatted = r"""
This is % some comment
a sentence.
And here is another.
With a % another comment
final statement.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_comment_b(self):

        text = r"""
This is a text% with a comment
that ends here.
But this is
not a comment.
        """

        formatted = r"""
This is a text% with a comment
that ends here.
But this is not a comment.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_block(self):

        text = r"""
This is the
first sentence.

And the
second sentence.
        """

        formatted = r"""
This is the first sentence.

And the second sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_environment(self):

        text = r"""
This is the
first sentence.

And the
\begin{foo}
    With some
    sub sentence.
\end{foo}
second sentence.
        """

        formatted = r"""
This is the first sentence.

And the
\begin{foo}
    With some sub sentence.
\end{foo}
second sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_ignore(self):

        text = r"""
This is the
first sentence.

And \TG{?}{and some}{.} the
second sentence.
        """

        formatted = r"""
This is the first sentence.

And \TG{?}{and some}{.} the second sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_newline(self):

        text = r"""
This is the
first sentence.

And \footnote{
A text with a
footnote.
} the
second sentence.
        """

        formatted = r"""
This is the first sentence.

And \footnote{
    A text with a footnote.
} the second sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_newline_a(self):

        text = r"""
A start\footnote{This is a footnote. With
    some poor formatting.
}.
A new sentence.
        """

        formatted = r"""
A start\footnote{
    This is a footnote.
    With some poor formatting.
}.
A new sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_newline_b(self):

        text = r"""
A start\footnote[Some option]{This is a footnote. With
    some poor formatting.
}.
A new sentence.
        """

        formatted = r"""
A start\footnote[Some option]{
    This is a footnote.
    With some poor formatting.
}.
A new sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


    def test_command_newline_comment(self):

        text = r"""
A start\footnote{ %
    This is a footnote. With
    some poor formatting.
}.
A new sentence.
        """

        formatted = r"""
A start\footnote{ %
    This is a footnote.
    With some poor formatting.
}.
A new sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_newline_comment_a(self):

        text = r"""
A start\footnote{ %
    This is a footnote. With
    some poor formatting.
} %
        """

        formatted = r"""
A start\footnote{ %
    This is a footnote.
    With some poor formatting.
} %
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_newline_nested_a(self):

        text = r"""
This is the
first sentence.

And \footnote{
A text with a \TG{
    A note in
    a note.
}
footnote.
} the
second sentence.
        """

        formatted = r"""
This is the first sentence.

And \footnote{
    A text with a \TG{
        A note in a note.
    }
    footnote.
} the second sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_nested_environment(self):

        text = r"""
\some{
\mycommand{
\begin{something}
Some text \emph{with some highlighting}. And two sentences.
\end{something}
}
}
        """

        formatted = r"""
\some{
    \mycommand{
        \begin{something}
            Some text \emph{with some highlighting}.
            And two sentences.
        \end{something}
    }
}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

if __name__ == "__main__":
    unittest.main()
