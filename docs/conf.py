import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information

project = "texplain"
copyright = "2017-2023, Tom de Geus"
author = "Tom de Geus"
html_theme = "furo"
autodoc_type_aliases = {"Iterable": "Iterable", "ArrayLike": "ArrayLike"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinxarg.ext",
    "sphinx.ext.autosectionlabel",
    "sphinx_mdinclude",
]
