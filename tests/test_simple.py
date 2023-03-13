import unittest

import numpy as np

import texplain


class MyTests(unittest.TestCase):
    """
    Tests
    """

    def test_find_commented(self):
        """
        Test the find_commented method
        """
        text = "0123456%89"
        indices = texplain.find_commented(text)
        self.assertEqual(indices, [[7, 10]])

    def test_is_commented(self):
        """
        Test the is_commented method
        """
        text = "0123456%89"
        expect = np.array([False, False, False, False, False, False, False, True, True, True])
        log = texplain.is_commented(text)
        self.assertTrue(np.all(log == expect))

    def test_format_labels(self):
        text = r"""
\chapter{My chapter}
\label{main}

\section{My header}
\label{foo}

\subsection{Deeper down}
\label{subfoo}

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
see below \cref{my-o-sec}

\section{Another sections}
\label{my-o-sec}

Foo\footnote{
    \label{myfootnote}
    This is a footnote.
}

\section{Measurement of \texorpdfstring{$\ell_c$}{l\_c}}
\label{sec-lc}

Bar
        """

        formatted = r"""
\chapter{My chapter}
\label{ch:main}

\section{My header}
\label{sec:foo}

\subsection{Deeper down}
\label{sec:subfoo}

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
see below \cref{sec:my-o-sec}

\section{Another sections}
\label{sec:my-o-sec}

Foo\footnote{
    \label{note:myfootnote}
    This is a footnote.
}

\section{Measurement of \texorpdfstring{$\ell_c$}{l\_c}}
\label{sec:lc}

Bar
        """

        tex = texplain.TeX(text=text)
        self.assertEqual(
            tex.labels(),
            [
                "main",
                "foo",
                "subfoo",
                "EQ-PS",
                "dep:a",
                "FIG:dep:b",
                "FiG:dep",
                "my-o-sec",
                "myfootnote",
                "sec-lc",
            ],
        )

        for i in range(3):
            tex.format_labels()
            self.assertEqual(
                tex.labels(),
                [
                    "ch:main",
                    "sec:foo",
                    "sec:subfoo",
                    "eq:PS",
                    "fig:dep:a",
                    "fig:dep:b",
                    "fig:dep",
                    "sec:my-o-sec",
                    "note:myfootnote",
                    "sec:lc",
                ],
            )
            self.assertEqual(formatted.strip(), str(tex).strip())

    def test_format_labels_prefix(self):
        text = r"""
\chapter{My chapter}
\label{main}

\section{My header}
\label{foo}

\subsection{Deeper down}
\label{subfoo}

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
see below \cref{my-o-sec}

\section{Another sections}
\label{my-o-sec}

Foo

\section{Measurement of \texorpdfstring{$\ell_c$}{l\_c}}
\label{sec-lc}

Bar
        """

        formatted = r"""
\chapter{My chapter}
\label{ch:SI:main}

\section{My header}
\label{sec:SI:foo}

\subsection{Deeper down}
\label{sec:SI:subfoo}

Some test here
\begin{align}
    \label{eq:SI:PS}
    P(S) &\sim S^{-\tau}
\end{align}
as shown in Eq.~\eqref{eq:SI:PS}.

\begin{figure}[htp]
    \subfloat{\label{fig:SI:dep:a}}
    \subfloat{\label{fig:SI:dep:b}}
    \caption{
        \textbf{\protect\subref*{fig:SI:dep:a}.}
        The rest.
    }
    \label{fig:SI:dep}
\end{figure}

see \cref{fig:SI:dep:a,fig:SI:dep,fig:SI:dep:b}
see below \cref{sec:SI:my-o-sec}

\section{Another sections}
\label{sec:SI:my-o-sec}

Foo

\section{Measurement of \texorpdfstring{$\ell_c$}{l\_c}}
\label{sec:SI:lc}

Bar
        """

        tex = texplain.TeX(text=text)
        self.assertEqual(
            tex.labels(),
            [
                "main",
                "foo",
                "subfoo",
                "EQ-PS",
                "dep:a",
                "FIG:dep:b",
                "FiG:dep",
                "my-o-sec",
                "sec-lc",
            ],
        )

        for i in range(3):
            tex.format_labels(prefix="SI")
            self.assertEqual(
                tex.labels(),
                [
                    "ch:SI:main",
                    "sec:SI:foo",
                    "sec:SI:subfoo",
                    "eq:SI:PS",
                    "fig:SI:dep:a",
                    "fig:SI:dep:b",
                    "fig:SI:dep",
                    "sec:SI:my-o-sec",
                    "sec:SI:lc",
                ],
            )
            self.assertEqual(formatted.strip(), str(tex).strip())

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
        self.assertEqual(formatted.strip(), str(tex).strip())

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
        self.assertEqual(formatted.strip(), str(tex).strip())

    def test_replace_command_simple(self):
        source = r"This is a \TG{I would replace this} text."
        expect = r"This is a  text."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "")
        self.assertEqual(expect.strip(), str(tex).strip())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}", "")
        self.assertEqual(expect.strip(), str(tex).strip())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"\TG", "")
        self.assertEqual(expect.strip(), str(tex).strip())

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}", "{}")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{text}{foo}{test}."
        expect = r"This is a test."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[3]", "#3")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{text}{foo}{test}."
        expect = r"This is a test."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[3]", "{#3}")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{text}{test}."
        expect = r"This is a \mycomment{text}{test}."
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[2]", r"\mycomment{#1}{#2}")
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_replace_command_recursive(self):
        source = r"This is a \TG{I would replace this\TG{reasons...}} text. \TG{And this too}Foo"
        expect = r"This is a  text. Foo"
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{Foo\TG{my}{Bar}}{Bar} text. \TG{And this too}{Bar}"
        expect = r"This is a Bar text. Bar"
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[2]", "#2")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{Foo}{\TG{my}{Bar}} text. \TG{And this too}{Bar}"
        expect = r"This is a Bar text. Bar"
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[2]", "#2")
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"This is a \TG{Foo}{\TG{my}{Bar}} text. \TG{And this too}{Bar}"
        expect = r"This is a \AB{\AB{Bar}{my}}{Foo} text. \AB{Bar}{And this too}"
        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[2]", r"\AB{#2}{#1}")
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_comments(self):
        source = r"This is a %, text with comments"
        expect = r"This is a "
        tex = texplain.TeX(text=source)
        tex.remove_comments()
        self.assertEqual(expect.strip(), str(tex).strip())

        source = "This is a %, text with comments\nAnd some more"
        expect = "This is a \nAnd some more"
        tex = texplain.TeX(text=source)
        tex.remove_comments()
        self.assertEqual(expect.strip(), str(tex).strip())

        source = r"Here, 10 \% of water was removed % after cheating"
        expect = r"Here, 10 \% of water was removed "
        tex = texplain.TeX(text=source)
        tex.remove_comments()
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_comments_external(self):
        source = r"""
Overall, our approach explains why excitations.%, where $\omega_c$ cannot be readily observed.
%
%Our analysis explains why string-like rearrangements are,
%as otherwise excitations display too small displacements to probe the granularity of the material.
        """

        expect = """
Overall, our approach explains why excitations.
        """

        tex = texplain.TeX(text=source)
        tex.remove_commentlines()
        tex.remove_comments()
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_command_a(self):
        """
        Remove a command.
        """

        source = r"Foo \TG{bar.}"
        expect = r"Foo bar."

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "#1")
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_command_b(self):
        """
        Remove a command, including in commented text.
        """

        source = r"\TG{Foo} %\TG{bar}."
        expect = r"Foo %bar."

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "#1")
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_command_c(self):
        """
        Remove a command, with unmatching brackets in commented text.
        """

        source = r"Foo \TG{bar.}%Foo bar.}"
        expect = r"Foo bar.%Foo bar.}"

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "#1", ignore_commented=True)
        self.assertEqual(expect.strip(), str(tex).strip())

    def test_remove_command_d(self):
        """
        Remove a command, but leave those in commented text.
        """

        source = r"Foo \TG{bar.}%\TG{Foo bar.}"
        expect = r"Foo bar.%\TG{Foo bar.}"

        tex = texplain.TeX(text=source)
        tex.replace_command(r"{\TG}[1]", "#1", ignore_commented=True)
        self.assertEqual(expect.strip(), str(tex).strip())


if __name__ == "__main__":
    unittest.main()
