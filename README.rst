=============
What is fdat?
=============

``fdat`` (prounounced eff-dat) is a package for getting financial data like historical stock prices.

For more documentation, please see http://fdat.readthedocs.io.

Installation
------------

``fdat`` can be easily installed with pip::

    $ pip install fdat

Usage
-----
``fdat`` is really simple to use. Below you'll find the basics.

Getting historical daily stock prices for a ticker on a single date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the historical daily stock prices for a ticker on a single date simply import ``fdat`` and call ``get_prices()``:

.. code-block:: python

    import fdat

    prices_df = fdat.get_prices('SPY', '2017-03-30')

The results will be stock prices in a pandas DataFrame:

.. code-block:: none

    TBD

The returned DataFrame has the following columns:

    *blah*
        blah

    *blah*
        blah

If there were no prices for this day, an empty DataFrame will be returned. It should be noted that ``fdat`` fetches earnings announcements from AlphaVantage by default.

Getting the historical daily stock prices for a ticker over a date range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is equally easy to get the historical daily stock prices for a ticker over a date range:

.. code-block:: python

    import fdat

    prices_df = fdat.get_prices('SPY', '2018-01-01', '2018-01-31')

Once again the results will be stock prices in a pandas DataFrame:

.. code-block:: none

    TBD


Caching
~~~~~~~

``fdat`` supports caching so that repeated calls to ``fdat.get_prices()`` don't actually make calls to the servers. Runtime caching is enabled by default which means calls during your program's execution will be cached. However, the ``fdat.RuntimeCache`` is only temporary and the next time your program runs it will call the API again.

Persistent on disk caching is provided via ``fdat.SqliteCache`` and can be easily enabled by setting ``fdat.default_cache`` once before calls to ``fdat.get_prices()``:

.. code-block:: python

    import fdat
    fdat.default_cache = fdat.SqliteCache('fdat.db')

    prices_df = fdat.get_prices('2017-03-30')

Extension
~~~~~~~~~

``fdat`` is very easy to extend in case you want to add fetchers for different financial data or even another caching system. For more documentation, please see http://fdat.readthedocs.io.