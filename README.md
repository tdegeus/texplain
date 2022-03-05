[![ci](https://github.com/tdegeus/texplain/workflows/CI/badge.svg)](https://github.com/tdegeus/texplain/actions)
[![pre-commit](https://github.com/tdegeus/texplain/workflows/pre-commit/badge.svg)](https://github.com/tdegeus/texplain/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/texplain.svg)](https://anaconda.org/conda-forge/texplain)

# texplain

Clean-up TeX files.
From the command-line you can use:
*   `texcleanup`:
    Run several common fixes, such as ensuring nicely formatting labels.
*   `texplain`:
    Create a directory with a TeX-file and only its dependencies
    (those figure-files and references that are actually included).
    This is particularly useful to create a clean version to submit to a journal.

**Documentation: [https://texplain.readthedocs.org](texplain.readthedocs.org)**

# Contents

<!-- MarkdownTOC -->

- [Disclaimer](#disclaimer)
- [Getting texplain](#getting-texplain)
    - [Using conda](#using-conda)
    - [Using PyPi](#using-pypi)
    - [From source](#from-source)

<!-- /MarkdownTOC -->

# Disclaimer

This library is free to use under the
[MIT license](https://github.com/tdegeus/texplain/blob/master/LICENSE).
Any additions are very much appreciated, in terms of suggested functionality, code, documentation,
testimonials, word-of-mouth advertisement, etc.
Bug reports or feature requests can be filed on [GitHub](https://github.com/tdegeus/texplain).
As always, the code comes with no guarantee.
None of the developers can be held responsible for possible mistakes.

Download:
[.zip file](https://github.com/tdegeus/texplain/zipball/master) |
[.tar.gz file](https://github.com/tdegeus/texplain/tarball/master).

(c - [MIT](https://github.com/tdegeus/texplain/blob/master/LICENSE)) T.W.J. de Geus (Tom) |
tom@geus.me |
www.geus.me |
[github.com/tdegeus/texplain](https://github.com/tdegeus/texplain)

# Getting texplain

## Using conda

```bash
conda install -c conda-forge texplain
```

## Using PyPi

```bash
python -m pip install texplain
```

## From source

```bash
# Download texplain
git checkout https://github.com/tdegeus/texplain.git
cd texplain

# Install
python -m pip install .
```

