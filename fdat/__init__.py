from .FinancialData import FinancialData
from .abstract_daily_prices_fetcher import AbstractDailyPricesFetcher
from .av_daily_prices_fetcher import AVDailyPricesFetcher
from .abstract_daily_prices_cache import AbstractDailyPricesCache
from .no_daily_prices_cache import NoDailyPricesCache

name = 'fdat'

_financial_data = FinancialData()

__all__ = [
    'get_daily_prices',
    'set_daily_prices_cache',
    'set_daily_prices_fetcher',
    'AbstractDailyPricesFetcher',
    'AVDailyPricesFetcher',
    'AbstractDailyPricesCache',
    'NoDailyPricesCache'
]


def get_daily_prices(ticker_str, start_date_str, end_date_str=None):
    """Gets daily stock prices for the ticker symbol for the dates in the range.

    Args:
        ticker_str:
        start_date_str:
        end_date_str:

    Returns:

    """

    if end_date_str is None:
        end_date_str = start_date_str

    return _financial_data.get_daily_prices(ticker_str, start_date_str, end_date_str)


def set_daily_prices_cache(cache):
    _financial_data.set_daily_prices_cache(cache)


def set_daily_prices_fetcher(prices_fetcher):
    _financial_data.set_daily_prices_fetcher(prices_fetcher)
