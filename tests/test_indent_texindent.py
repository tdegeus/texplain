import unittest

import texplain


class TestSentence(unittest.TestCase):
    def test_simple(self):
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
        self.assertEqual(ret.strip(), formatted.strip())

    def test_squash(self):
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
        self.assertEqual(ret.strip(), formatted.strip())


if __name__ == "__main__":
    unittest.main()
