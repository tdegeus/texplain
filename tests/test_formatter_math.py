import texplain


def test_simple():
    assert texplain.formatter_math("a=b") == "a = b"
    assert texplain.formatter_math("a-b") == "a - b"
    assert texplain.formatter_math(r"\tau, \nu, \ldots") == r"\tau, \nu, \ldots"


def test_braces():
    assert texplain.formatter_math("{ - b}") == "{-b}"
    assert texplain.formatter_math("{- b}") == "{-b}"
    assert texplain.formatter_math("{-b}") == "{-b}"
