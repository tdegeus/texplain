import texplain


def convert(text, indices):
    ret = []
    for cmd in indices:
        iret = []
        for arg in cmd:
            iret.append(text[arg[0] : arg[1]])
        ret.append(iret)
    return ret


def test_basic():
    text = r"This is some \foo \bar"
    expect = [[r"\foo"], [r"\bar"]]
    assert expect == convert(text, texplain.find_command(text))


def test_argument():
    text = r"This is some \foo{fooarg} \bar{[bararg}  {bararg2}"
    expect = [[r"\foo", r"{fooarg}"], [r"\bar", r"{[bararg}", r"{bararg2}"]]
    assert expect == convert(text, texplain.find_command(text))


def test_argument_comment():
    text = r"This is some \foo{fooarg} \bar{[bararg}  {bararg2}  % some } nonsense"
    expect = [[r"\foo", r"{fooarg}"], [r"\bar", r"{[bararg}", r"{bararg2}"]]
    assert expect == convert(text, texplain.find_command(text))


def test_argument_comment_a():
    text = r"""
This is a text with a \command%
% first comment
[
    opt1
]%
% second comment
{
    arg1
}

\bar
[
    opt2
]
% comment
{
    arg2
}
"""
    expect = [[r"\command", r"[opt1]", r"{arg1}"], [r"\bar", r"[opt2]", r"{arg2}"]]
    ret = convert(text, texplain.find_command(text))
    ret = [[arg.replace(" ", "").replace("\n", "") for arg in cmd] for cmd in ret if cmd]
    assert expect == ret


def test_option_argument():
    text = r"This is some \foo[fooopt]{fooarg} \bar [baropt] [{baropt2}] {[bararg}  {bararg2}"
    expect = [
        [r"\foo", r"[fooopt]", r"{fooarg}"],
        [r"\bar", r"[baropt]", r"[{baropt2}]", r"{[bararg}", r"{bararg2}"],
    ]
    assert expect == convert(text, texplain.find_command(text))


def test_nested_command():
    text = r"""
\begin{figure}
    \subfloat{\label{fig:foo}}
\end{figure}
"""
    expect = [
        [r"\begin", r"{figure}"],
        [r"\subfloat", r"{\label{fig:foo}}"],
        [r"\label", r"{fig:foo}"],
        [r"\end", r"{figure}"],
    ]
    assert expect == convert(text, texplain.find_command(text))


def test_option_a():
    text = r"\begin{figure}[htb]{a} Foo."
    expect = [[r"\begin", r"{figure}", r"[htb]", r"{a}"]]
    assert expect == convert(text, texplain.find_command(text))


def test_math():
    text = r"\begin{equation} [0, 1) \end{equation}"
    expect = [[r"\begin", r"{equation}"], [r"\end", r"{equation}"]]
    assert expect == convert(text, texplain.find_command(text))
