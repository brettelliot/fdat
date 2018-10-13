import pandas as pd
from typing import List

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

    def check_for_missing_dates(self, symbol: str, date_list: List[str]) -> List[str]:
        """Look in the cache for dates and return the dates that aren't in the cache.

        Args:
            symbol (str):
                The ticker symbol of the stock we are checking for.
            date_list (list):
                The list of dates to check the cache for.

        Returns:
            list:
                The dates from the date_list that are not in the cache.

        """
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')

    def add_daily_prices(self, symbol: str, missing_dates: List[str], uncached_prices_df: pd.DataFrame) -> None:
        """Add the uncached daily prices to the cache.

        Args:
            symbol (str):
                The ticker symbol of the stock we are adding to the cache
            missing_dates (list):
                The dates that were fetched and should be added to the cache index. Even dates that have no data
                should be added to the cache index so that if requested again, we return nothing for them without
                using the fetcher.
            uncached_prices_df (DataFrame):
                A valid standard prices DataFrame containing uncached prices that should be added to the cache.

        Returns:
            None
        """
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')

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
        raise NotImplementedError('AbstractDailyPricesCache is an abstract base class')
