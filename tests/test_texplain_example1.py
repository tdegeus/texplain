import filecmp
import os
import shutil
import subprocess
import unittest

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = os.path.join(basedir, "test1")


def readlines(filepath):
    with open(filepath) as file:
        return file.read().strip().splitlines()


class MyTests(unittest.TestCase):
    """
    Tests
    """

    @classmethod
    def tearDownClass(self):

        shutil.rmtree(tmpdir)

    def test_basic(self):

        subprocess.run(["texplain", os.path.join(basedir, "input1", "example.tex"), tmpdir])

        for name in ["main.tex", "library.bib"]:
            self.assertEqual(
                readlines(os.path.join(basedir, "output1", name)),
                readlines(os.path.join(tmpdir, name)),
            )

        files = ["figure_1.pdf", "figure_2.pdf", "apalike.bst", "unsrtnat.bst", "goose-article.cls"]

        for name in files:
            self.assertTrue(
                filecmp.cmp(os.path.join(basedir, "output1", name), os.path.join(tmpdir, name))
            )

        renamed = {
            "Sequential.pdf": "figure_1.pdf",
            "Diverging.pdf": "figure_2.pdf",
        }

        for key in renamed:
            self.assertTrue(
                filecmp.cmp(
                    os.path.join(basedir, "input1", "figures", key),
                    os.path.join(tmpdir, renamed[key]),
                )
            )


if __name__ == "__main__":

    unittest.main()
