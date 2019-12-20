[![Travis](https://travis-ci.com/tdegeus/texplain.svg?branch=master)](https://travis-ci.com/tdegeus/texplain)
[![Build status](https://ci.appveyor.com/api/projects/status/jro7k8cm82v82q03?svg=true)](https://ci.appveyor.com/project/tdegeus/texplain)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/texplain.svg)](https://anaconda.org/conda-forge/texplain)

# texplain

Create a directory with a TeX-file and only its dependencies (those figure-files and references that are actually included). This is particularly useful to create a clean version to submit to a journal.

# Contents

<!-- MarkdownTOC -->

- [Disclaimer](#disclaimer)
- [Getting texplain](#getting-texplain)
    - [Using conda](#using-conda)
    - [Using PyPi](#using-pypi)
    - [From source](#from-source)
- [Usage](#usage)

<!-- /MarkdownTOC -->

# Disclaimer

This library is free to use under the [MIT license](https://github.com/tdegeus/texplain/blob/master/LICENSE). Any additions are very much appreciated, in terms of suggested functionality, code, documentation, testimonials, word-of-mouth advertisement, etc. Bug reports or feature requests can be filed on [GitHub](https://github.com/tdegeus/texplain). As always, the code comes with no guarantee. None of the developers can be held responsible for possible mistakes.

Download: [.zip file](https://github.com/tdegeus/texplain/zipball/master) | [.tar.gz file](https://github.com/tdegeus/texplain/tarball/master).

(c - [MIT](https://github.com/tdegeus/texplain/blob/master/LICENSE)) T.W.J. de Geus (Tom) | tom@geus.me | www.geus.me | [github.com/tdegeus/texplain](https://github.com/tdegeus/texplain)

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

# Usage

Basic usage:

```none
texplain <input.tex> <output-directory>
```

To get more information use

```none
texplain --help
```

which prints

```none
texplain
    Create a clean output directory with only included files/citations.

Usage:
    texplain [options] <input.tex> <output-directory>

Options:
        --version   Show version.
    -h, --help      Show help.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/texplain
```
