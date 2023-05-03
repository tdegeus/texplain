**********
pre-commit
**********

texcleanup
==========

Format ``.pre-commit-config.yaml`` with:

.. code-block:: yaml

    repos:
    - repo: https://github.com/tdegeus/texplain
      rev: v0.8.0
      hooks:
      - id: texcleanup
        args: [--format-labels, --use-cleveref]

texindent
=========

Format ``.pre-commit-config.yaml`` with:

.. code-block:: yaml

    repos:
    - repo: https://github.com/tdegeus/texplain
      rev: v0.8.0
      hooks:
      - id: texindent
        args: []
