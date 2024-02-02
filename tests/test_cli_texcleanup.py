import texplain


def test_regex(tmp_path):
    text = r"""
This is some {\it italic text} that needes formatting.
    """

    formatted = r"""
This is some \emph{italic text} that needes formatting.
    """

    fpath = tmp_path / "test.tex"
    fpath.write_text(text.strip())

    texplain.texcleanup(["--re-sub", r"{\\it\s+(.*)}", r"\\emph{\1}", str(fpath)])
    assert fpath.read_text().strip() == formatted.strip()
