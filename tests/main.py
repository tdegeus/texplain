import unittest

import texplain


class MyTests(unittest.TestCase):
    """
    Tests
    """

    def test_labels(self):

        text = r"""
\section{My header}
\label{foo}

Some test here
\begin{align}
    \label{EQ:PS}
    P(S) &\sim S^{-\tau}
\end{align}
as shown in Eq.~\eqref{EQ:PS}.

\begin{figure}[htp]
    \subfloat{\label{dep:a}}
    \subfloat{\label{FIG:dep:b}}
    \caption{
        \textbf{\protect\subref*{dep:a}.}
        The rest.
    }
    \label{FiG:dep}
\end{figure}

see \cref{dep:a,FiG:dep,FIG:dep:b}
        """

        formatted = r"""
\section{My header}
\label{sec:foo}

Some test here
\begin{align}
    \label{eq:PS}
    P(S) &\sim S^{-\tau}
\end{align}
as shown in Eq.~\eqref{eq:PS}.

\begin{figure}[htp]
    \subfloat{\label{fig:dep:a}}
    \subfloat{\label{fig:dep:b}}
    \caption{
        \textbf{\protect\subref*{fig:dep:a}.}
        The rest.
    }
    \label{fig:dep}
\end{figure}

see \cref{fig:dep:a,fig:dep,fig:dep:b}
        """

        tex = texplain.TeX(text=text)
        self.assertEqual(tex.labels(), ["foo", "EQ:PS", "dep:a", "FIG:dep:b", "FiG:dep"])

        tex.format_labels()
        self.assertEqual(formatted, tex.tex)
        self.assertEqual(tex.labels(), ["sec:foo", "eq:PS", "fig:dep:a", "fig:dep:b", "fig:dep"])

    def test_remove_commentlines(self):

        text = r"""
This is my
% actually I was working
  % and I think that
final text.
        """

        formatted = r"""
This is my
final text.
        """

        tex = texplain.TeX(text=text)
        tex.remove_commentlines()
        self.assertEqual(formatted, tex.tex)

    def test_use_cleveref(self):

        text = r"""
This is Sec.~\ref{sec:foo} what I would
classically Eq.~\eqref{eq:bar} write,
but it is maybe not Eq.~(\ref{eq:bar})
this most efficient.
        """

        formatted = r"""
This is \cref{sec:foo} what I would
classically \cref{eq:bar} write,
but it is maybe not \cref{eq:bar}
this most efficient.
        """

        tex = texplain.TeX(text=text)
        tex.use_cleveref()
        self.assertEqual(formatted, tex.tex)


if __name__ == "__main__":

    unittest.main()
