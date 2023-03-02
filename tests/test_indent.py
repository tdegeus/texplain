import unittest

import numpy as np

import texplain


class TestIndent(unittest.TestCase):
    """
    Tests
    """

    def test_command_punctuation(self):
        """
        Remove white space between command closing bracket and punctuation.
        """

        text = r"""
A start\footnote{
    This is a footnote
}
.
A new sentence.
        """

        formatted = r"""
A start\footnote{
    This is a footnote
}.
A new sentence.
        """

        self.assertTrue(False)

        # -----

        text = r"""
A start\footnote{
    This is a footnote
}
a continued sentence.
        """

        formatted = r"""
A start\footnote{
    This is a footnote
}
a continued sentence.
        """

        self.assertTrue(False)

    def test_force_comment(self):
        """
        Keep the comment where it is even if a formatting tool does not like it.
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

        self.assertTrue(False)

#     def test_envlabel_newline(self):
#         """
#         Put label on a new line.
#         """

#         text = r"""
# \section{My section}\label{sec:a}
#         """

#         formatted = r"""
# \section{My section}
# \label{sec:a}
#         """

#         self.assertTrue(False)

#         # ----

#         text = r"""
# \begin{equation}
#     \label{eq:a} a = b
# \end{equation}
#         """

#         formatted = r"""
# \begin{equation}
#     \label{eq:a}
#     a = b
# \end{equation}
#         """

#         # ----

#         text = r"""
# \begin{figure}
#     \subfloat{\label{fig:foo}}
# \end{figure}
#         """

#         formatted = r"""
# \begin{figure}
#     \subfloat{\label{fig:foo}}
# \end{figure}
#         """

#         self.assertTrue(False)

if __name__ == "__main__":

    unittest.main()
