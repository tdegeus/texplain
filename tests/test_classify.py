import unittest

import texplain


class MyTests(unittest.TestCase):
    """
    Tests
    """

    def test_equation(self):
        text = r"""
        foo bar
        \begin{equation}
            \label{eq:foo}
            a = 10
        \end{equation}
        baz
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())

        # --

        text = r"""
        My text
        \begin{equation}
            a = b
            \label{eq:qew}
        \end{equation}
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())

    def test_section(self):
        text = r"""
        foo bar
        \section{My section}
        \label{sec:foo}
        baz
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())

    def test_figure(self):
        text = r"""
        foo bar
        \begin{figure}
            \label{fig:foo}
            \caption{My caption}
        \end{figure}
        baz
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())

    def test_custom(self):
        text = r"""
\begin{example}[H]
    \begin{oframed}
        \caption{Self-explanatory vs documentation intensive}
        \label{misc:self-explenatory}
    \end{oframed}
\end{example}
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())


if __name__ == "__main__":
    unittest.main()
