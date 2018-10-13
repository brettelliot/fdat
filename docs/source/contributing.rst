============
Contributing
============

Vision
------
The vision for ``fdat`` is to be a drop in replacement for ``pandas_datareader`` BUT only if the situation arises. There are two situations that have come up for me that caused me to create ``fdat``:

#. I want to download financial data once and use it repeatedly even offline. I've been unsuccessful at getting the requests caches to work in this way.

#. I've found it necessary to switch to a historical price source like AlphaVantage when the yahoo and google readers failed and I didn't find any documentation to add my own ``pandas_datareader``. I know there is an AV reader now, but
this will probably happen again and I'd like to be able to easily create my own readers when needed.

#. I needed to auto adjust the OHLC values returned by AV.



Therefore, if possible, I've tried to keep the interface for ``fdat`` as similar as possible to the corresponding ``pandas_datareader`` interface without doing more than I need. For example, at the moment I only need to pull data for one ticker at a time so I haven't implemented the ticker list and returning a multiindex dataframe. It's easy so if you want to contribute, please go ahead :)

Github
------

This repo uses the `Git Branching Model <https://nvie.com/posts/a-successful-git-branching-model/>`_. The head of master branch should always be production ready. The head of the develop branch should contain the latest delivered development changes for the next release. Features should be created in feature branches that branch from the develop branch.

Create virtualenv (recommended, but not required). Then get the repo::

    $ git clone https://github.com/brettelliot/fdat.git
    $ pip install -e

Run the tests::

    $ python setup.py test

Creating a new feature branch from the ``develop`` branch::

    $ git checkout -b be-feature develop

Committing code to the new ``be-feature`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push --set-upstream origin be-feature

Committing code to an existing ``be-feature`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push

Creating the documentation for the first time (from the docs/ directory)::

    $ sphinx-quickstart

Building the documentation (again, from the docs/ directory)::

    $ sphinx-apidoc -f -o source/ ../fdat/
    $ make html

Incorporating a finished feature onto ``develop``::

    $ git checkout develop
    $ git merge --no-ff be-feature
    $ git push origin develop
    $ git branch -d be-feature
    $ git push origin --delete be-feature

Create a release branch from ``develop``, and merge it into ``master``:

.. parsed-literal::

    $ git checkout -b release-|release| develop
    $ git checkout master
    $ git merge --no-ff release-|release|
    $ git push
    $ git tag -a |release| -m "release |release|"
    $ git push origin |release|

Merge the release branch changes back into ``develop`` so it's up to date:

.. parsed-literal::

    $ git checkout develop
    $ git merge --no-ff release-|release|
    $ git branch -d release-|release|

Generating distribution archives::

    $ git checkout master
    $ python setup.py check --strict --metadata
    $ rm -rf dist/
    $ python3 setup.py sdist bdist_wheel

Upload to test.pypi.org::

    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

To test the package from test.pypi.org, create a new virtual env, install the package, then run python and import it::

    $ rm -rf ~/.virtualenvs/fdat_test_pypi
    $ mkvirtualenv fdat_test_pypi
    $ python3 -m pip install --no-cache-dir --extra-index-url https://test.pypi.org/simple/ fdat
    $ python
    >>> import fdat
    >>> fdat.name
    'fdat'
    >>> quit()
    $ deactivate

Upload the package to the real pypi.org website::

    $ twine upload dist/*

To test the package from pypi.org, create a new virtual env, install the package, then run python and import it::

    $ rm -rf ~/.virtualenvs/fdat_pypi
    $ mkvirtualenv fdat_pypi
    $ pip install --no-cache-dir fdat
    $ python
    >>> import fdat
    >>> fdat.name
    'fdat'
    >>> quit()
    $ deactivate

