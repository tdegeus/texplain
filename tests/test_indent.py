import unittest

import texplain


class TestIndent(unittest.TestCase):
    """
    Tests
    """

    def test_multiline_command_a(self):

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

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_multiline_command_b(self):

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

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_multiline_command_comment(self):

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

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), formatted.strip())


    def test_command_punctuation(self):
        """
        Keep exact indentation of command.
        """

        text = r"""
A start\footnote{
    This is a footnote
}.
A new sentence.
        """

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), text.strip())

        # -----

        text = r"""
A start\footnote{
    This is a footnote
}
a continued sentence.
        """

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), text.strip())

        # -----

        text = r"""
\section{My section}
\label{sec:a}
        """

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), text.strip())

    def test_force_comment(self):
        """
        Keep comments exactly as they are.
        """

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

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_label_equation(self):
        """
        Keep label where it is in an equation.
        """

        text = r"""
\begin{equation}
    \label{eq:a}
    a = b
\end{equation}
        """

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), text.strip())

    def test_nested_command(self):
        """
        Do nothing against nested commands.
        """

        text = r"""
\begin{figure}
    \subfloat{\label{fig:foo}}
\end{figure}
        """

        config = texplain.texindent_default_config()
        ret = texplain.texindent(text, config)
        self.assertEqual(ret.strip(), text.strip())


if __name__ == "__main__":
    unittest.main()
