from .FinancialData import FinancialData
from .abstract_daily_prices_fetcher import AbstractDailyPricesFetcher
from .av_daily_prices_fetcher import AVDailyPricesFetcher
from .abstract_daily_prices_cache import AbstractDailyPricesCache
from .no_daily_prices_cache import NoDailyPricesCache
from .runtime_daily_prices_cache import RuntimeDailyPricesCache
from .sqlite_daily_prices_cache import SqliteDailyPricesCache
from .utils import *
import pandas as pd

name = 'fdat'

_financial_data = FinancialData()

__all__ = [
    'get_daily_prices',
    'set_daily_prices_cache',
    'set_daily_prices_fetcher',
    'validate_standard_prices_dataframe',
    'standard_prices_dataframe_column_order',
    'AbstractDailyPricesFetcher',
    'AVDailyPricesFetcher',
    'AbstractDailyPricesCache',
    'NoDailyPricesCache',
    'RuntimeDailyPricesCache',
    'SqliteDailyPricesCache'
]


def get_daily_prices(symbol: str, start_date: str, end_date: str=None) -> pd.DataFrame:
    """Returns a DataFrame containing daily price data for the stock over the date range.

    Args:
        symbol (str):
            The ticker symbol of the stock to get prices for.
        start_date (str):
            The start date in the format "YYYY-MM-DD".
        end_date (str):
            The end date in the format "YYYY-MM-DD". If left out, only prices for the start_date will be returned.

    Returns:
        DataFrame:
            A pandas DataFrame indexed by ``date``, that has columns:
            ``symbol``, ``open``, ``high``, ``low``, ``close``,
            ``dividend_amt``, ``split_coeff``,
            ``adj_open``, ``adj_high``, ``adj_low``, and ``adj_close``,
            ``volume``, and ``timezone``.

    """

    if end_date is None:
        end_date = start_date

    return _financial_data.get_daily_prices(symbol, start_date, end_date)


def set_daily_prices_cache(cache: AbstractDailyPricesCache) -> None:
    """Set the cache for daily price data.

    Args:
        cache (AbstractDailyPricesCache):
            An instance of AbstractDailyPricesCache to use.

    Returns:
        None

    """
    _financial_data.set_daily_prices_cache(cache)


def set_daily_prices_fetcher(fetcher: AbstractDailyPricesFetcher) -> None:
    """Set the fetcher for daily price data.

    Args:
        fetcher (AbstractDailyPricesFetcher):
            An instance of AbstractDailyPricesFetcher to use.

    Returns:
        None

    """
    _financial_data.set_daily_prices_fetcher(fetcher)
