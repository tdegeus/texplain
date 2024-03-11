import texplain


def test_equation():
    texts = []

    t = r"""
foo bar
\begin{equation}
    \label{eq:foo}
    a = 10
\end{equation}
baz
"""
    texts.append(t)

    t = r"""
My text
\begin{equation}
    a = b
    \label{eq:qew}
\end{equation}
"""
    texts.append(t)

    for text in texts:
        tex = texplain.TeX(text)
        tex.format_labels()
        assert str(tex).strip() == text.strip()


def test_section():
    text = r"""
foo bar
\section{My section}
\label{sec:foo}
baz
"""
    tex = texplain.TeX(text)
    tex.format_labels()
    assert str(tex).strip() == text.strip()


def test_figure():
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
    assert str(tex).strip() == text.strip()


def test_figure_b():
    text = r"""
foo bar
\begin{figure*}
    \label{fig:foo}
    \caption{My caption}
\end{figure*}
baz
"""
    tex = texplain.TeX(text)
    tex.format_labels()
    assert str(tex).strip() == text.strip()


def test_custom():
    texts = []

    t0 = r"""
\begin{example}[H]
    \begin{oframed}
        \caption{Self-explanatory vs documentation intensive}
        \label{misc:self-explenatory}
    \end{oframed}
\end{example}
"""
    texts.append(t0)

    texts.append("\n\n".join([r"\section{My section}"]) + t0)
    texts.append("\n\n".join([r"\section{My section}", r"\label{sec:mysec}"]) + t0)

    for text in texts:
        tex = texplain.TeX(text)
        tex.format_labels()
        assert str(tex).strip() == text.strip()


def test_nested():
    texts = []

    t = r"""
\begin{appendices}

    \section{My section}

    \begin{figure}[H]
        \caption{Self-explanatory vs documentation intensive}
        \label{fig:self-explenatory}
    \end{figure}

\end{appendices}
"""
    texts.append(t)

    t = r"""
\begin{appendices}

    \section{My section}
    \label{sec:mysec}

    \begin{figure}[H]
        \caption{Self-explanatory vs documentation intensive}
        \label{fig:self-explenatory}
    \end{figure}

\end{appendices}
"""
    texts.append(t)

    t = r"""
\begin{appendices}

    \section{My section}
    \label{sec:mysec}

    \begin{example}[H]
        \begin{oframed}
            \caption{Self-explanatory vs documentation intensive}
            \label{misc:self-explenatory}
        \end{oframed}
    \end{example}

\end{appendices}
"""
    texts.append(t)

    for text in texts:
        tex = texplain.TeX(text)
        tex.format_labels()
        assert str(tex).strip() == text.strip()


def test_hybrid():
    texts = []

    t = r"""
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
    texts.append(t)

    t = r"""
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
    texts.append(t)

    for text in texts:
        tex = texplain.TeX(text)
        tex.format_labels()
        assert str(tex).strip() == text.strip()
