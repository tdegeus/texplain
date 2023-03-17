*********
texindent
*********


Customisation
=============

Settings
--------

*   Take the default behaviour and switch on/off some rules:
    ``- rule1 - rule2 + rule3 ...``.

*   Use only a specific set of rules:
    ``rule1, rule2``.

Extent
------

*   Globally.

*   A blocks of code:

    .. code-block:: tex

        % \begin{texindent}{settings}
        ...
        % \end{texindent}

*   An environment:

    .. code-block:: tex

        % \texindent{settings}
        \begin{...}
        ...
        \end{...}
