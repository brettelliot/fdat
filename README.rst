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

To get the historical daily stock prices for a ticker on a single date simply import ``fdat`` and call ``get_daily_prices()``:

.. code-block:: python

    import fdat

    prices_df = fdat.get_daily_prices('SPY', '2017-08-01')

The results will be stock prices in a pandas DataFrame:

.. code-block:: none

               ticker    open    high       low   close    volume  dividend_amt  split_coeff  adj_open  adj_high   adj_low  adj_close
    2018-08-01    SPY  281.56  282.13  280.1315  280.86  53853326           0.0          1.0  280.2904  280.8579  278.8684   279.5936



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


If there were no prices for this day, an empty DataFrame will be returned. It should be noted that ``fdat`` fetches daily stock price data from AlphaVantage by default.

It is equally easy to get the historical daily stock prices for a ticker over a date range:

.. code-block:: python

    import fdat

    prices_df = fdat.get_daily_prices('SPY', '2018-01-01', '2018-01-31')

Once again the results will be stock prices in a pandas DataFrame:

.. code-block:: none

               ticker    open      high       low   close     volume  dividend_amt  split_coeff  adj_open  adj_high   adj_low  adj_close
    2018-01-02    SPY  267.84  268.8100  267.4000  268.77   86655749           0.0          1.0  264.3817  265.3392  263.9474   265.2997
    2018-01-03    SPY  268.96  270.6400  268.9600  270.47   90070416           0.0          1.0  265.4872  267.1455  265.4872   266.9777
    2018-01-04    SPY  271.20  272.1600  270.5447  271.61   80636408           0.0          1.0  267.6983  268.6459  267.0515   268.1030
    2018-01-05    SPY  272.51  273.5600  271.9500  273.42   83523995           0.0          1.0  268.9914  270.0279  268.4387   269.8897
    2018-01-08    SPY  273.31  274.1000  272.9800  273.92   57319192           0.0          1.0  269.7811  270.5609  269.4553   270.3832
    2018-01-09    SPY  274.40  275.2500  274.0810  274.54   57253957           0.0          1.0  270.8570  271.6960  270.5421   270.9952
    2018-01-10    SPY  273.68  274.4200  272.9200  274.12   69574318           0.0          1.0  270.1463  270.8767  269.3961   270.5806
    2018-01-11    SPY  274.75  276.1200  274.5600  276.12   62361455           0.0          1.0  271.2025  272.5548  271.0149   272.5548
    2018-01-12    SPY  276.42  278.1100  276.0819  277.92   90816076           0.0          1.0  272.8509  274.5190  272.5171   274.3315
    2018-01-16    SPY  279.35  280.0900  276.1800  276.97  106555142           0.0          1.0  275.7431  276.4735  272.6140   273.3938
    2018-01-17    SPY  278.03  280.0500  276.9700  279.61  113258799           0.0          1.0  274.4401  276.4340  273.3938   275.9997
    2018-01-18    SPY  279.48  279.9600  278.5800  279.14  100728006           0.0          1.0  275.8714  276.3452  274.9830   275.5358
    2018-01-19    SPY  279.80  280.4100  279.1400  280.41  140920098           0.0          1.0  276.1873  276.7894  275.5358   276.7894
    2018-01-22    SPY  280.17  282.6900  280.1100  282.69   91322408           0.0          1.0  276.5525  279.0400  276.4933   279.0400
    2018-01-23    SPY  282.74  283.6200  282.3700  283.29   97084700           0.0          1.0  279.0893  279.9579  278.7241   279.6322
    2018-01-24    SPY  284.02  284.7000  281.8400  283.18  134816117           0.0          1.0  280.3528  281.0240  278.2009   279.5236
    2018-01-25    SPY  284.16  284.2700  282.4050  283.30   84587313           0.0          1.0  280.4910  280.5996  278.7587   279.6421
    2018-01-26    SPY  284.25  286.6285  283.9600  286.58  107743119           0.0          1.0  280.5798  282.9276  280.2935   282.8797
    2018-01-29    SPY  285.93  286.4300  284.5000  284.68   90118337           0.0          1.0  282.2382  282.7317  280.8266   281.0043
    2018-01-30    SPY  282.60  284.7360  281.2200  281.76  131796419           0.0          1.0  278.9512  281.0596  277.5890   278.1220
    2018-01-31    SPY  282.73  283.3000  280.6800  281.90  118948131           0.0          1.0  279.0795  279.6421  277.0560   278.2602


Caching
~~~~~~~

``fdat`` supports caching so that repeated calls to the ``fdat.get_XXX()`` methods don't actually make calls to the fetchers. Runtime caching is enabled by default which means calls during your program's execution will be cached. However, the runtime cache is only temporary and the next time your program runs it will call the fetcher.

Persistent on disk caching is provided via the Sqlite caches and can be easily enabled by setting it once before calls to ``fdat.get_XXX()`` methods. For example cache daily price data so getting it doesn't use the fetcher every time:

.. code-block:: python

    import fdat

    # Create an instance of the SqliteDailyPricesCache and tell it where to store the sqlite db.
    fdat.set_daily_prices_cache(fdat.SqliteDailyPricesCache('fdat_daily_prices.db')

    # All future calls to get_daily_prices() will attempt to pull the date from the fetcher first and will also cache
    # any data that is fetched.
    prices_df = fdat.get_daily_prices('2018-08-01')

Extension
~~~~~~~~~

``fdat`` is very easy to extend in case you want to add fetchers for different financial data or even another caching system. For more documentation, please see http://fdat.readthedocs.io.