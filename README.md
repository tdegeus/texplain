[![ci](https://github.com/tdegeus/texplain/workflows/CI/badge.svg)](https://github.com/tdegeus/texplain/actions)
[![Documentation Status](https://readthedocs.org/projects/texplain/badge/?version=latest)](https://texplain.readthedocs.io/en/latest/?badge=latest)
[![pre-commit](https://github.com/tdegeus/texplain/workflows/pre-commit/badge.svg)](https://github.com/tdegeus/texplain/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/texplain.svg)](https://anaconda.org/conda-forge/texplain)

**Documentation: [https://texplain.readthedocs.io](texplain.readthedocs.io)**

<!-- MarkdownTOC -->

- [Usage](#usage)
    - [pre-commit](#pre-commit)
    - [From the command-line](#from-the-command-line)
    - [From Python](#from-python)
- [Disclaimer](#disclaimer)
- [Getting texplain](#getting-texplain)
    - [Using conda](#using-conda)
    - [Using PyPi](#using-pypi)
    - [From source](#from-source)

<!-- /MarkdownTOC -->

# Usage

Clean-up TeX files.

## pre-commit

For example:

```yaml
repos:
- repo: https://github.com/tdegeus/texplain
  rev: v0.5.6
  hooks:
  - id: texcleanup
    args: [--format-labels, --remove-commentlines, --use-cleveref]
```

## From the command-line

*   [`texcleanup`](https://texplain.readthedocs.io/en/latest/tools.html#texcleanup):
    Run several common fixes, such as ensuring nicely formatted labels.

*   [`texplain`](https://texplain.readthedocs.io/en/latest/tools.html#texplain):
    Create a directory with a TeX-file and only its dependencies
    (those figure-files and references that are actually included).
    This is particularly useful to create a clean version to submit to a journal.

## From Python

All of these tools wrap around a
[Python module](https://texplain.readthedocs.io/en/latest/module.html)
that you can use just as well!

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
