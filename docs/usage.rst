*****
Usage
*****

The are three ways to use the tools provided here.

pre-commit
==========

For example:

.. code-block:: yaml

    repos:
    - repo: https://github.com/tdegeus/texplain
      rev: v0.5.6
      hooks:
      - id: texcleanup
        args: [--format-labels, --remove-commentlines, --use-cleveref]

Command-line
============

:ref:`Command-line tools`

Python
======

:ref:`Python module`
