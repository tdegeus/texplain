import texplain


def test_comment_a():
    text = r"This is a % comment"

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_comment_b():
    text = r"This is a. % comment"

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_comment_c():
    text = "This is a. % comment a\nAnd another. % comment b"

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_comment_d():
    text = r"""
% a
% b
 % c
% d
  %% e
 % f
%% g
"""

    formatted = r"""
% a
% b
% c
% d
%% e
% f
%% g
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_comment_indent():
    text = r"""
% a
% b
 % c
% d
\begin{figure}[htbp]
  %% e
 % f
\end{figure}
%% g
"""

    formatted = r"""
% a
% b
% c
% d
\begin{figure}[htbp]
    %% e
    % f
\end{figure}
%% g
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_noindent_verbatim():
    text = r"""
Some text   \begin{verbatim} a = b \end{verbatim}    some more text.
"""

    formatted = r"""
Some text \begin{verbatim} a = b \end{verbatim} some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_noindent_verbatim_a():
    text = r"""
Some text


\begin{verbatim} a = b \end{verbatim}


some more text.
"""

    formatted = r"""
Some text

\begin{verbatim} a = b \end{verbatim}

some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_noindent():
    text = r"""
Some  text
% \begin{noindent}
should be ignored
% \end{noindent}
  some more text.
"""

    formatted = r"""
Some text
% \begin{noindent}
should be ignored
% \end{noindent}
some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_noindent_a():
    text = r"""
Some  text


% \begin{noindent}
should be ignored
% \end{noindent}


  some more text.
"""

    formatted = r"""
Some text

% \begin{noindent}
should be ignored
% \end{noindent}

some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment():
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
    assert ret.strip() == formatted.strip()


def test_environment_a():
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
    assert ret.strip() == formatted.strip()


def test_environment_b():
    text = r"""
Some text \begin{equation}[0, 1)\end{equation} some more text on interval $[0, 1)$.
"""

    formatted = r"""
Some text
\begin{equation}
    [0, 1)
\end{equation}
some more text on interval $[0, 1)$.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_c():
    text = r"""
Some text \begin{equation}
[0, 1)
(2, 3)
\end{equation} some more text on interval $[0, 1)$.
"""

    formatted = r"""
Some text
\begin{equation}
    [0, 1)
    (2, 3)
\end{equation}
some more text on interval $[0, 1)$.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_star_a():
    text = r"""
\begin{figure*}[b]
    \centering
    \includegraphics[width=\linewidth]{example-image}
\end{figure*}
"""

    formatted = r"""
\begin{figure*}[b]
    \centering
    \includegraphics[width=\linewidth]{example-image}
\end{figure*}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_star_b():
    text = r"""
\begin{figure*}[b]
\centering
\includegraphics[width=\linewidth]{example-image}
\end{figure*}
"""

    formatted = r"""
\begin{figure*}[b]
    \centering
    \includegraphics[width=\linewidth]{example-image}
\end{figure*}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_nested_a():
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
    assert ret.strip() == formatted.strip()


def test_environment_nested_b():
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
    assert ret.strip() == formatted.strip()


def test_environment_nested_c():
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
    assert ret.strip() == formatted.strip()


def test_environment_nested_d():
    """
    https://github.com/cmhughes/latexindent.pl/blob/main/test-cases/commands/sub-super-scripts.tex
    """
    text = r"""
\parbox{
    $\int_{x^2}^{y^2}$
    \[
    x^2
    \]}
"""

    formatted = r"""
\parbox{
    $\int_{x^2}^{y^2}$
    \[
        x^2
    \]
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_multiline_a():
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
    assert ret.strip() == formatted.strip()


def test_environment_multiline_b():
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
    assert ret.strip() == formatted.strip()


def test_environment_multiline_option():
    text = r"""
\begin{figure}[b] Foo.
    Bar.
\end{figure}
"""

    formatted = r"""
\begin{figure}[b]
    Foo.
    Bar.
\end{figure}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_multiline_option_a():
    text = r"""
\begin{tcolorbox}[colback=green!5!white] Using a mesoscopic model.
    See details.
\end{tcolorbox}
"""

    formatted = r"""
\begin{tcolorbox}[colback=green!5!white]
    Using a mesoscopic model.
    See details.
\end{tcolorbox}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_environment_comment():
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
    assert ret.strip() == formatted.strip()


def test_environment_nested():
    text = r"""
This is { \normalsize
Some text}
"""

    formatted = r"""
This is {
    \normalsize
    Some text
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_item_simple():
    text = r"""
\begin{itemize} \item a \item b
\item c \item d
\item e \end{itemize}
"""

    formatted = r"""
\begin{itemize}
    \item a
    \item b
    \item c
    \item d
    \item e
\end{itemize}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_item_newline():
    text = r"""
\begin{itemize} \item a \item b

\item c \item d
\item e \end{itemize}
"""

    formatted = r"""
\begin{itemize}
    \item a
    \item b

    \item c
    \item d
    \item e
\end{itemize}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_item_multiline():
    text = r"""
\begin{itemize} \item a \item b has a long
text that spans multiple lines. But also multiple
sentences.

With even
a new paragraph.
\item c \item d
\item e \end{itemize}
"""

    formatted = r"""
\begin{itemize}
    \item a
    \item b has a long text that spans multiple lines.
    But also multiple sentences.

    With even a new paragraph.
    \item c
    \item d
    \item e
\end{itemize}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_item_nested():
    text = r"""
\begin{itemize} \item a \item b
\item c \item d \begin{itemize} \item suba \item subb with
some text.
And another
sentence.
\item subc \item subd \end{itemize}
\item e \end{itemize}
"""

    formatted = r"""
\begin{itemize}
    \item a
    \item b
    \item c
    \item d
    \begin{itemize}
        \item suba
        \item subb with some text.
        And another sentence.
        \item subc
        \item subd
    \end{itemize}
    \item e
\end{itemize}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_command_punctuation():
    text = r"""
A start\footnote{
    This is a footnote
}.
A new sentence.
"""

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_command_punctuation_a():
    text = r"""
A start\footnote{
    This is a footnote
}
a continued sentence.
"""

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_command_punctuation_b():
    text = r"""
\section{My? section}
\label{sec:a}
"""

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_command_label_equation():
    text = r"""
\begin{equation}
    \label{eq:a}
    a = b
\end{equation}
"""

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_command_nested():
    text = r"""
\begin{figure}
    \subfloat{\label{fig:foo}}
\end{figure}
"""

    ret = texplain.indent(text)
    assert ret.strip() == text.strip()


def test_one_sentence_per_line_quote():
    text = r"""
This a ``sentence!'' And another.
"""

    formatted = r"""
This a ``sentence!'' And another.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_full_quote():
    text = r"""
``This a sentence!'' And
another.
"""

    formatted = r"""
``This a sentence!'' And another.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_brace():
    text = r"""
This a sentence. And another
(etc.).
"""

    formatted = r"""
This a sentence.
And another (etc.).
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_full_brace():
    text = r"""
(This a sentence.) (This a second sentence.) And another. And one more (?).
"""

    formatted = r"""
(This a sentence.) (This a second sentence.) And another.
And one more (?).
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_comment_a():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_comment_b():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_block():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_newline():
    text = r"""
This is a \\
long sentence.

With some
more words.
"""

    formatted = r"""
This is a \\
long sentence.

With some more words.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_newline_b():
    text = r"""
This is a \\
long sentence.

With some \\ more. And some more words.

\\ Here is
another
bit of
text.
"""

    formatted = r"""
This is a \\
long sentence.

With some \\
more.
And some more words.

\\
Here is another bit of text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_newline_c():
    text = r"""
This is a \\ \\
long sentence.

With some \\ \\ more. And some more words.


\\ \\ Here is
another
bit of
text.
"""

    formatted = r"""
This is a \\
\\
long sentence.

With some \\
\\
more.
And some more words.

\\
\\
Here is another bit of text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_newline_d():
    text = r"""
\setkomavar{fromaddress}{EPFL\\
Route de la Sorge\\ CH-1015 Lausanne, Switzerland}
"""

    formatted = r"""
\setkomavar{fromaddress}{
    EPFL\\
    Route de la Sorge\\
    CH-1015 Lausanne, Switzerland
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_multiline():
    text = r"""
This is a \\
long sentence.

With
some
more
words.
And
another
following sentence.
"""

    formatted = r"""
This is a \\
long sentence.

With some more words.
And another following sentence.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_environment():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_ignore():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_a():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_b():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_comment():
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
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_comment_a():
    text = r"""
% my comment
A start\footnote{ %
    This is a footnote. With
    some poor formatting.
} %
"""

    formatted = r"""
% my comment
A start\footnote{ %
    This is a footnote.
    With some poor formatting.
} %
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_nested_a():
    text = r"""
This is the
first sentence.

And \footnote{
A text with a \TG{ % some comment
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
    A text with a \TG{ % some comment
        A note in a note.
    }
    footnote.
} the second sentence.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_newline_nested_b():
    text = r"""
This is the
first sentence.

% some header
And \footnote{
A text with a \TG{ % some comment
    A note in
    a note.
}
footnote.
} the
second sentence.
"""

    formatted = r"""
This is the first sentence.

% some header
And \footnote{
    A text with a \TG{ % some comment
        A note in a note.
    }
    footnote.
} the second sentence.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_command_multi_nested():
    text = r"""
This is the
first sentence.

% some header
\TG{ This is
a sentence.
} %
{ And another
sentence.
\TG{with
some}
{
more
formatting
to
do
}
}
"""

    formatted = r"""
This is the first sentence.

% some header
\TG{
    This is a sentence.
} %
{
    And another sentence.
    \TG{
        with some
    }
    {
        more formatting to do
    }
}
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_one_sentence_per_line_nested_environment():
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
    assert ret.strip() == formatted.strip()


def test_math_environment_a():
    text = r"""
Some text \[ a = b \] \[c = d\] some more text.
"""

    formatted = r"""
Some text
\[
    a = b
\]
\[
    c = d
\]
some more text.
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_code():
    text = r"""
% a comment
\if foo \else bar \fi
"""

    formatted = r"""
% a comment
\if
    foo
\else
    bar
\fi
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_code_a():
    text = r"""
% a comment
some text \if@namecite foo \else bar \fi
"""

    formatted = r"""
% a comment
some text
\if@namecite
    foo
\else
    bar
\fi
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_code_b():
    text = r"""
% a comment
some text \if@namecite \if@foo bar \fi \fi
"""

    formatted = r"""
% a comment
some text
\if@namecite
    \if@foo
        bar
    \fi
\fi
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()


def test_code_c():
    text = r"""
\newif\if@namecite
\let\if@namecite\iffalse
\DeclareOption{namecite}{\let\if@namecite\iftrue}

some text \if@namecite foo \else bar \fi
"""

    formatted = r"""
\newif\if@namecite
\let\if@namecite\iffalse
\DeclareOption{namecite}{\let\if@namecite\iftrue}

some text
\if@namecite
    foo
\else
    bar
\fi
"""

    ret = texplain.indent(text)
    assert ret.strip() == formatted.strip()
