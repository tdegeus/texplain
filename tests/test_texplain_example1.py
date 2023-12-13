import filecmp
import pathlib
import shutil
import subprocess

basedir = pathlib.Path(__file__).parent
tmpdir = basedir / "test1"
tmpdir.mkdir(exist_ok=True)


def readlines(filepath):
    with open(filepath) as file:
        return file.read().strip().splitlines()


def test_basic():
    subprocess.run(["texplain", str(basedir / "input1" / "example.tex"), str(tmpdir)])

    for name in ["main.tex", "library.bib"]:
        assert readlines(basedir / "output1" / name) == readlines(tmpdir / name)

    files = ["figure_1.pdf", "figure_2.pdf", "apalike.bst", "unsrtnat.bst", "goose-article.cls"]

    for name in files:
        assert filecmp.cmp(basedir / "output1" / name, tmpdir / name)

    renamed = {
        "Sequential.pdf": "figure_1.pdf",
        "Diverging.pdf": "figure_2.pdf",
    }

    for key in renamed:
        assert filecmp.cmp(basedir / "input1" / "figures" / key, tmpdir / renamed[key])

    shutil.rmtree(tmpdir)
