=============
What is fdat?
=============

``fdat`` (pronounced eff-dat) is a package for getting financial data like historical stock prices.

For more documentation, please see http://fdat.readthedocs.io.

Installation
------------

``fdat`` can be easily installed with pip::

    $ pip install fdat

Usage
-----
``fdat`` is really simple to use. Below you'll find the basics.

Historical daily stock prices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the historical daily stock prices for a ticker on a single date simply import ``fdat`` and call ``get_prices()``:

.. code-block:: python

    import fdat

    prices_df = fdat.get_prices('SPY', '2017-08-01')

The results will be stock prices in a pandas DataFrame:

.. code-block:: none

               ticker    open   high      low   close    volume  dividend_amt  split_coeff    adj_open    adj_high     adj_low  adj_close
    date
    2017-08-01    SPY  247.46  247.5  246.716  247.32  55050401           0.0          1.0  241.834417  241.873508  241.107331   241.6976


The returned DataFrame is indexed by date and has the following columns:

    *ticker*
        blah

    *open, high, low, close*
        The stocks open, high, low and close price.

    *dividend_amt*
        The amount of any dividend events on that day.

    *split_coeff*
        The coefficient of any splits that happened on that day.

    *adj_open, adj_high, adj_low, adj_close*
        The stock prices after adjusting for dividends and splits.


If there were no prices for this day, an empty DataFrame will be returned. It should be noted that ``fdat`` fetches earnings announcements from AlphaVantage by default.

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