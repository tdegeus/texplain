import unittest

import texplain


class MyTests(unittest.TestCase):
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

    def test_hybrid(self):
        text = r"""
\begin{itemize}
    \item
    \begin{referee}
        Some question
    \end{referee}

    Some response

    \begin{figure}[htp]
        \centering
        \subfloat{\label{fig:1a}}
        \subfloat{\label{fig:1b}}
        \includegraphics[width=\linewidth]{foo}
        \caption{Foo bar}
        \label{fig:1}
    \end{figure}
\end{itemize}
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())

        # ---

        text = r"""
Foo bar

\section{My section}
%
\label{sec:my}

Foo bar

\begin{figure}[htp]
    \centering
    \subfloat{\label{fig:1a}}
    \subfloat{\label{fig:1b}}
    \includegraphics[width=\linewidth]{foo}
    \caption{Foo bar}
    \label{fig:1}
\end{figure}
        """

        tex = texplain.TeX(text)
        tex.format_labels()
        self.assertEqual(str(tex).strip(), text.strip())


if __name__ == "__main__":
    unittest.main()
