from .abstract_daily_prices_cache import AbstractDailyPricesCache

__all__ = [
    'NoDailyPricesCache'
]


class NoDailyPricesCache(AbstractDailyPricesCache):
    """``NoDailyPricesCache`` is an instance of ``AbstractDailyPricesCache`` that works with \
    ``FinancialData`` but doesn't cache anything.

    The ``NoDailyPricesCache`` cache is good for testing or making sure you're always using the latest data.

    """

    def __init__(self):
        self._no_cache_df = None

    def check_for_missing_dates(self, ticker, date_list):
        """``NoDailyPricesCache`` doesn't cache anything so just return the dates that are passed in because \
        they are all missing.

        Args:
            ticker (str):
                The ticker symbol of the stock we are checking for.
            date_list (list):
                The list of dates to check the cache for.

        Returns:
            list:
                The dates from the date_list that are not in the cache.

        """
        return date_list

    def add_daily_prices(self, ticker, missing_dates, uncached_prices_df):
        """Just store the prices so that the next call to ``get_daily_prices`` will use them.

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
        self._no_cache_df = uncached_prices_df

    def get_daily_prices(self, ticker, start_date_str, end_date_str=None):
        """Returns exactly what was passed into the last call to ``add_daily_prices``

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
        if end_date_str is None:
            end_date_str = start_date_str

        return self._no_cache_df[start_date_str:end_date_str]