import unittest

import texplain


class TestPlaceholderMethods(unittest.TestCase):
    """
    Implementation of :py:class:`texplain.Placeholder`.
    """

    def test_select(self):
        text = r"foo \footnote{bar} baz"
        placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
        self.assertEqual(repl, "foo place baz")
        self.assertEqual(text, placeholder.to_text(repl))

        text = "foo\n\\footnote{bar} baz"
        placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
        self.assertEqual(placeholder.content, r"\footnote{bar}")
        self.assertEqual(repl, "foo\nplace baz")
        self.assertEqual(text, placeholder.to_text(repl))
        self.assertEqual(text, placeholder.to_text("foo place baz"))
        self.assertEqual(text, placeholder.to_text("foo   place   baz"))

        text = "foo\n\\footnote{bar}\nbaz"
        placeholder, repl = texplain.Placeholder.from_text("place", text, 4, 18)
        self.assertEqual(placeholder.content, r"\footnote{bar}")
        self.assertEqual(repl, "foo\nplace\nbaz")
        self.assertEqual(text, placeholder.to_text(repl))
        self.assertEqual(text, placeholder.to_text("foo place baz"))
        self.assertEqual(text, placeholder.to_text("foo   place   baz"))

        text = "foo\n    \\footnote{bar}\nbaz"
        placeholder, repl = texplain.Placeholder.from_text("place", text, 4 + 4, 18 + 4)
        self.assertEqual(placeholder.content, r"\footnote{bar}")
        self.assertEqual(repl, "foo\n    place\nbaz")
        self.assertEqual(text, placeholder.to_text(repl))
        self.assertEqual(text, placeholder.to_text("foo place baz"))
        self.assertEqual(text, placeholder.to_text("foo   place   baz"))


class TestPlaceholders(unittest.TestCase):
    """
    Practical tests of
    -   :py:func:`texplain.text_to_placeholders`
    -   :py:func:`texplain.text_from_placeholders`
    """

    def test_noindent(self):
        """
        Replace noindent with placeholders.
        """

        text = r"""
        This is a text
        %\begin{noindent}
        should be ignored
        %\end{noindent}
        More text.

        Bla bla bla.
        % \begin{noindent}
        should also be ignored
        % \end{noindent}
        A last sentence.
        """

        expect = r"""
        This is a text
        -TEXINDENT-NOINDENT-1-
        More text.

        Bla bla bla.
        -TEXINDENT-NOINDENT-2-
        A last sentence.
        """

        change_indent = r"""
        This is a text -TEXINDENT-NOINDENT-1- More text.

        Bla bla bla. -TEXINDENT-NOINDENT-2- A last sentence.
        """

        ret, placeholders = texplain.text_to_placeholders(
            text, [texplain.PlacholderType.noindent_block]
        )
        self.assertEqual(ret, expect)
        self.assertEqual(text, texplain.text_from_placeholders(ret, placeholders))
        self.assertEqual(text, texplain.text_from_placeholders(change_indent, placeholders))

    def test_comments(self):
        """
        Replace comments with placeholders.
        """

        text = """
        This is a text% with some inline comment
        More text.
        % A free comment
        """

        expect = """
        This is a text-TEXINDENT-COMMENT-1-
        More text.
        -TEXINDENT-COMMENT-2-
        """

        ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlacholderType.comment])
        self.assertEqual(ret, expect)
        self.assertEqual(text, texplain.text_from_placeholders(ret, placeholders))

    def test_environment(self):
        """
        Replace environment with placeholders.
        """

        text = r"""
        This is a text
        \begin{equation}
            \begin{split}
                a = 10 \\
                a = 20.
            \end{split}
        \end{equation}
        More text.
        Even more text.
        \begin{equation}
            b = 20.
        \end{equation}

        Bla bla bla.
        \begin{equation}
            c = 30.
        \end{equation}
        A last sentence.
        """

        expect = """
        This is a text
        -TEXINDENT-ENVIRONMENT-1-
        More text.
        Even more text.
        -TEXINDENT-ENVIRONMENT-2-

        Bla bla bla.
        -TEXINDENT-ENVIRONMENT-3-
        A last sentence.
        """

        ret, placeholders = texplain.text_to_placeholders(
            text, [texplain.PlacholderType.environment]
        )
        self.assertEqual(ret, expect)
        self.assertEqual(text, texplain.text_from_placeholders(ret, placeholders))

    def test_math(self):
        text = r"""
        This is a text
        $a = 10\$$.
        More text.
        $a = 20$.
        Even more text.
        $b = 20$.
        Bla bla bla.
        $c = 30$.
        A last sentence.
        """

        expect = """
        This is a text
        -TEXINDENT-MATH-1-.
        More text.
        -TEXINDENT-MATH-2-.
        Even more text.
        -TEXINDENT-MATH-3-.
        Bla bla bla.
        -TEXINDENT-MATH-4-.
        A last sentence.
        """

        ret, placeholders = texplain.text_to_placeholders(
            text, [texplain.PlacholderType.inline_math]
        )
        self.assertEqual(ret, expect)
        self.assertEqual(text, texplain.text_from_placeholders(ret, placeholders))

    def test_command(self):
        text = r"""
        This is a text \command[foo]{arg1} {arg2} with
        \foo

        \bar

        some \TG{\text{...}}
        """

        expect = """
        This is a text -TEXINDENT-COMMAND-1- with
        -TEXINDENT-COMMAND-2-

        -TEXINDENT-COMMAND-3-

        some -TEXINDENT-COMMAND-4-
        """

        ret, placeholders = texplain.text_to_placeholders(text, [texplain.PlacholderType.command])
        self.assertEqual(ret, expect)
        self.assertEqual(text, texplain.text_from_placeholders(ret, placeholders))


if __name__ == "__main__":
    unittest.main()
