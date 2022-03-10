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
    \label{EQ-PS}
    P(S) &\sim S^{-\tau}
\end{align}
as shown in Eq.~\eqref{EQ-PS}.

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
see below \cref{my-other-section}

\section{Another sections}
\label{my-other-section}
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
see below \cref{sec:my-other-section}

\section{Another sections}
\label{sec:my-other-section}
        """

        tex = texplain.TeX(text=text)
        self.assertEqual(
            tex.labels(), ["foo", "EQ-PS", "dep:a", "FIG:dep:b", "FiG:dep", "my-other-section"]
        )

        tex.format_labels()
        self.assertEqual(
            tex.labels(),
            ["sec:foo", "eq:PS", "fig:dep:a", "fig:dep:b", "fig:dep", "sec:my-other-section"],
        )
        self.assertEqual(formatted, tex.get())

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
        self.assertEqual(formatted, tex.get())

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
        self.assertEqual(formatted, tex.get())

    def test_replace_command_simple(self):

        source = r"This is a \TG{I would replace this} text."
        expect = r"This is a  text."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "")
        self.assertEqual(expect, tex.get())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}", "")
        self.assertEqual(expect, tex.get())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"\TG", "")
        self.assertEqual(expect, tex.get())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}", "{}")
        self.assertEqual(expect, tex.get())

        source = r"This is a \TG{text}{foo}{test}."
        expect = r"This is a test."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[3]", "#3")
        self.assertEqual(expect, tex.get())

        source = r"This is a \TG{text}{foo}{test}."
        expect = r"This is a test."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[3]", "{#3}")
        self.assertEqual(expect, tex.get())

        source = r"This is a \TG{text}{test}."
        expect = r"This is a \mycomment{text}{test}."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[2]", r"\mycomment{#1}{#2}")
        self.assertEqual(expect, tex.get())


if __name__ == "__main__":

    unittest.main()
