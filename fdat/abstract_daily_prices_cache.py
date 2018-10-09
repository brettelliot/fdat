__all__ = [
    'AbstractDailyPricesCache'
]


class AbstractDailyPricesCache(object):
    """AbstractDailyPricesCache is the base class for daily price caches.

        Derived classes must implement:
            * check_for_missing_dates
            * add_daily_prices
            * get_daily_prices

    """

    def check_for_missing_dates(self, ticker, date_list):
        """Look in the cache for dates and return the dates that aren't in the cache.

        Args:
            ticker (str):
                The ticker symbol of the stock we are checking for.
            date_list (list):
                The list of dates to check the cache for.

        Returns:
            list:
                The dates from the date_list that are not in the cache.

        """
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')

    def add_daily_prices(self, ticker, missing_dates, uncached_prices_df):
        """Add the uncached daily prices to the cache.

        Args:
            ticker (str):
                The ticker symbol of the stock we are adding to the cache
            missing_dates (list):
                The dates that were fetched and should be added to the cache index. Even dates that have no data
                should be added to the cache index so that if requested again, we return nothing for them without
                using the fetcher.
            uncached_prices_df (DataFrame):
                A DataFrame containing uncached prices that should be added to the cache.
        """
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')

    def get_daily_prices(self, ticker, start_date_str, end_date_str=None):
        """Returns the daily prices for ticker from the cache as a pandas DataFrame.

        Args:
            ticker (str):
                The ticker symbol of the stock we are getting data for.
            start_date_str (str):
                The start date of data we want in the format ``YYYY-MM-DD``.
            end_date_str (str):
                The end date data we want in the format ``YYYY-MM-DD``.
                If left out, we will fetch only data for the start date.

        Returns:
            DataFrame:
                Returns a pandas DataFrame indexed by ``date``, that has columns:
                ``ticker``, ``open``, ``high``, ``low``, ``close``,
                ``dividend_amt``, ``split_coeff``,
                ``adj_open``, ``adj_high``, ``adj_low``, and ``adj_close``.
        """
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')
