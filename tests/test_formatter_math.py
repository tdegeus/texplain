import texplain


def test_arithmetic():
    assert texplain.formatter_math(r"a=b") == r"a = b"
    assert texplain.formatter_math(r"a-b") == r"a - b"
    # assert texplain.formatter_math(r"a\leq b") == r"a \leq b"
    assert texplain.formatter_math(r"\theta>0") == r"\theta > 0"
    # assert texplain.formatter_math(r"P(x)\sim x^\theta") == r"P(x) \sim x^\theta"


def test_comma():
    assert texplain.formatter_math(r"1,2") == r"1,2"
    assert texplain.formatter_math(r"\tau, \nu, \ldots") == r"\tau, \nu, \ldots"


def test_braces():
    assert texplain.formatter_math(r"{ - b}") == r"{-b}"
    assert texplain.formatter_math(r"{- b}") == r"{-b}"
    assert texplain.formatter_math(r"{-b}") == r"{-b}"
