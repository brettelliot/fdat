import pandas as pd
import numpy as np
from .abstract_daily_prices_cache import AbstractDailyPricesCache
from typing import List
import fdat

__all__ = [
    'RuntimeDailyPricesCache'
]


class RuntimeDailyPricesCache(AbstractDailyPricesCache):
    """The ``RuntimeDailyPricesCache`` will cache daily price data for the program's lifetime."""

    def __init__(self):

        # Create the set containing keys that represent dates that data exists for a certain stock.
        # The keys will be a string in the format: ``YYYY-MM-DD,ticker`` such as ``2018-08-01,SPY``
        self._keys = set()

        # Create the cache that will hold the price data
        cols = fdat.standard_prices_dataframe_column_order()
        self._cache_df = pd.DataFrame(columns=cols)

    def check_for_missing_dates(self, symbol: str, dates: List[str]) -> List[str]:
        """Given a list of dates, find any that aren't already cached.

        Args:
            symbol (str):
                The ticker symbol of the stock we are checking for.
            dates (list):
                The list of dates to check the cache for.

        Returns:
            list[str]:
                The missing dates from dates list that are not in the cache.

        """
        missing_dates_list = []
        for date in dates:
            key = date + ',' + symbol
            if key not in self._keys:
                missing_dates_list.append(date)

        return missing_dates_list

    def add_daily_prices(self, symbol: str, missing_dates: List[str], uncached_prices_df: pd.DataFrame) -> None:
        """Cache the daily prices.

        Args:
            symbol (str):
                The ticker symbol of the stock we are adding to the cache
            missing_dates (list):
                The dates that were fetched and should be added to the cache index. Even dates that have no data
                should be added to the cache index so that if requested again, we return nothing for them without
                using the fetcher.
            uncached_prices_df (DataFrame):
                A valid standard prices DataFrame containing uncached prices that should be added to the cache.
        """

        fdat.validate_standard_prices_dataframe(uncached_prices_df)

        # create the new keys to add to the keys set.
        new_keys = []

        for date in missing_dates:
            new_key = date + ',' + symbol
            new_keys.append(new_key)

        for date in uncached_prices_df['date'].tolist():
            new_key = date + ',' + symbol
            new_keys.append(new_key)

        # add all the dates to the index set
        self._keys |= set(new_keys)

        # Add the uncached prices to the cache
        self._cache_df = pd.concat([self._cache_df, uncached_prices_df])
        fdat.validate_standard_prices_dataframe(self._cache_df)

    def get_daily_prices(self, symbol: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """Returns a valid standard prices DataFrame containing daily price data for the stock over the date range.

        Args:
            symbol (str):
                The ticker symbol of the stock to get prices for.
            start_date (str):
                The start date in the format "YYYY-MM-DD".
            end_date (str):
                The end date in the format "YYYY-MM-DD". If left out, only prices for the start_date will be returned.

        Returns:
            DataFrame:
                A valid standard prices DataFrame containing daily price data for the stock over the date range.

        """
        if end_date is None:
            end_date = start_date

        if end_date is None:
            end_date = start_date

        df = self._cache_df.query('date >= @start_date & date <= @end_date & symbol == @symbol')
        fdat.validate_standard_prices_dataframe(df)

        return df

