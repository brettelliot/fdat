import pandas as pd
import numpy as np
from .abstract_daily_prices_cache import AbstractDailyPricesCache
from typing import List

__all__ = [
    'RuntimeDailyPricesCache'
]


class RuntimeDailyPricesCache(AbstractDailyPricesCache):
    """The ``RuntimeDailyPricesCache`` will cache daily price data for the program's lifetime."""

    def __init__(self):

        # Create the index where the keys will be a string in the format: 'YYYY-MM-DD,ticker'
        self._keys_df = pd.DataFrame(columns=['keys'])

    def check_for_missing_dates(self, ticker: str, dates: List[str]) -> List[str]:
        """Given a list of dates, find any that aren't already cached.

        Args:
            ticker (str):
                The ticker symbol of the stock we are checking for.
            dates (list):
                The list of dates to check the cache for.

        Returns:
            list[str]:
                The dates from the date_list that are not in the cache.

        """
        missing_dates_list = []
        for date in dates:
            key = date + ',' + ticker
            # If the date, ticker pair is not in the index then add the date
            if not self._keys_df['keys'].str.contains(key).any():
                missing_dates_list.append(date)

        return missing_dates_list

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

    def get_daily_prices(self, ticker: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """Returns a DataFrame containing daily price data for the stock over the date range.

        Args:
            ticker (str):
                The ticker symbol of the stock to get prices for.
            start_date (str):
                The start date in the format "YYYY-MM-DD".
            end_date (str):
                The end date in the format "YYYY-MM-DD". If left out, only prices for the start_date will be returned.

        Returns:
            DataFrame:
                A pandas DataFrame indexed by ``date``, that has columns:
                ``ticker``, ``open``, ``high``, ``low``, ``close``,
                ``dividend_amt``, ``split_coeff``,
                ``adj_open``, ``adj_high``, ``adj_low``, and ``adj_close``.

        """
        if end_date is None:
            end_date = start_date

        return self._no_cache_df[start_date:end_date]