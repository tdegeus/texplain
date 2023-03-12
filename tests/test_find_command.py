import unittest

import texplain


class MyTests(unittest.TestCase):
    """
    Tests
    """

    def test_basic(self):
        text = r"This is some \foo \bar"
        ret = texplain.find_command(text)

        self.assertEqual(r"\foo", text[ret[0][0][0] : ret[0][0][1]])

    def test_argument(self):
        text = r"This is some \foo{fooarg} \bar{[bararg}  {bararg2}"
        ret = texplain.find_command(text)

        self.assertEqual(text[ret[0][0][0] : ret[0][0][1]], r"\foo")
        self.assertEqual(text[ret[0][1][0] : ret[0][1][1]], r"{fooarg}")

        self.assertEqual(text[ret[1][0][0] : ret[1][0][1]], r"\bar")
        self.assertEqual(text[ret[1][1][0] : ret[1][1][1]], r"{[bararg}")
        self.assertEqual(text[ret[1][2][0] : ret[1][2][1]], r"{bararg2}")

    def test_argument_comment(self):
        text = r"This is some \foo{fooarg} \bar{[bararg}  {bararg2}  % some } nonsense"
        ret = texplain.find_command(text)

        self.assertEqual(text[ret[0][0][0] : ret[0][0][1]], r"\foo")
        self.assertEqual(text[ret[0][1][0] : ret[0][1][1]], r"{fooarg}")

        self.assertEqual(text[ret[1][0][0] : ret[1][0][1]], r"\bar")
        self.assertEqual(text[ret[1][1][0] : ret[1][1][1]], r"{[bararg}")
        self.assertEqual(text[ret[1][2][0] : ret[1][2][1]], r"{bararg2}")

    def test_argument_comment_a(self):
        text = r"""
        This is a text with a \command%
        % first comment
        [
            option1
        ]%
        % second comment
        {
            argument1
        }

        \bar
        [
            option2
        ]
        % comment
        {
            argument2
        }
        """
        ret = texplain.find_command(text)

        self.assertEqual(text[ret[0][0][0] : ret[0][0][1]], r"\command")
        self.assertEqual(
            text[ret[0][1][0] : ret[0][1][1]].replace(" ", "").replace("\n", ""), r"[option1]"
        )
        self.assertEqual(
            text[ret[0][2][0] : ret[0][2][1]].replace(" ", "").replace("\n", ""), r"{argument1}"
        )

        self.assertEqual(text[ret[1][0][0] : ret[1][0][1]], r"\bar")
        self.assertEqual(
            text[ret[1][1][0] : ret[1][1][1]].replace(" ", "").replace("\n", ""), r"[option2]"
        )
        self.assertEqual(
            text[ret[1][2][0] : ret[1][2][1]].replace(" ", "").replace("\n", ""), r"{argument2}"
        )

    def test_option_argument(self):
        text = r"This is some \foo[fooopt]{fooarg} \bar [baropt] [{baropt2}] {[bararg}  {bararg2}"
        ret = texplain.find_command(text)

        self.assertEqual(text[ret[0][0][0] : ret[0][0][1]], r"\foo")
        self.assertEqual(text[ret[0][1][0] : ret[0][1][1]], r"[fooopt]")
        self.assertEqual(text[ret[0][2][0] : ret[0][2][1]], r"{fooarg}")

        self.assertEqual(text[ret[1][0][0] : ret[1][0][1]], r"\bar")
        self.assertEqual(text[ret[1][1][0] : ret[1][1][1]], r"[baropt]")
        self.assertEqual(text[ret[1][2][0] : ret[1][2][1]], r"[{baropt2}]")
        self.assertEqual(text[ret[1][3][0] : ret[1][3][1]], r"{[bararg}")
        self.assertEqual(text[ret[1][4][0] : ret[1][4][1]], r"{bararg2}")

    def test_nested_command(self):
        text = r"""
\begin{figure}
    \subfloat{\label{fig:foo}}
\end{figure}
        """

        ret = texplain.find_command(text)

        self.assertEqual(text[ret[0][0][0] : ret[0][0][1]], r"\begin")
        self.assertEqual(text[ret[0][1][0] : ret[0][1][1]], r"{figure}")

        self.assertEqual(text[ret[1][0][0] : ret[1][0][1]], r"\subfloat")
        self.assertEqual(text[ret[1][1][0] : ret[1][1][1]], r"{\label{fig:foo}}")

        self.assertEqual(text[ret[2][0][0] : ret[2][0][1]], r"\label")
        self.assertEqual(text[ret[2][1][0] : ret[2][1][1]], r"{fig:foo}")

        self.assertEqual(text[ret[3][0][0] : ret[3][0][1]], r"\end")
        self.assertEqual(text[ret[3][1][0] : ret[3][1][1]], r"{figure}")


if __name__ == "__main__":
    unittest.main()
