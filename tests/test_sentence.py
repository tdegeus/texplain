import texplain
import textwrap

def test_sentence_linebreak():
    tests = []

    symbols = [r"\\", r"\linebreak", r"\newline", r"\begin{align}"]

    for symbol in symbols:
        a = rf"""
        Some text {symbol} and some more.
        """
        b = rf"""
        Some text {symbol}
        and some more.
        """
        tests.append([textwrap.dedent(a), textwrap.dedent(b)])

    for a, b in tests:
        ret = texplain.indent(a)
        # assert ret.strip() == b.strip()

