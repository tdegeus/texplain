# texplain

Copy the TeX-file and only those figure-files and references that are included in it to a separate folder. This is particularly useful to create a clean version to submit to a journal.

## Usage

Basic usage:

```bash
texplain <input.tex> <output-directory>
```

To get more information use

```bash
texplain --help
```

which prints

```none
texplain
  Create a clean output directory with only included files/citations.

  This script provides the option to copy figures to the same folder as the main TeX-file
  (--flatten-figures). If that option is used the file-names are modified as follows:

      example/path/to/figure -> example_path_to_figure

  Similar for `--flatting-scripts`.

Usage:
  texplain [options] <input.tex> <output-directory>

Options:
      --clean             Cleans output directory.
      --copy-bbl          Copy existing bbl-files.
      --flatten-figures   Copy figures to the same folder as the main TeX-file.
      --flatten-scripts   Same as `flatten-figures` for scripts (in "\\lstinputlisting{...}").
      --version           Show version.
  -h, --help              Show help.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/texplain
```
