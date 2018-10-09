from .financial_data import FinancialData
from .abstract_prices_fetcher import AbstractPricesFetcher
from .av_prices_fetcher import AVPricesFetcher
from .abstract_cache import AbstractCache
from .no_cache import NoCache

name = 'fdat'

_financial_data = FinancialData()

__all__ = [
    'get_prices',
    'set_cache',
    'set_prices_fetcher',
    'AbstractPricesFetcher',
    'AVPricesFetcher',
    'AbstractCache',
    'NoCache'
]


def get_prices(ticker_str, start_date_str, end_date_str=None):

    if end_date_str is None:
        end_date_str = start_date_str

    return _financial_data.get_prices(ticker_str, start_date_str, end_date_str)


def set_cache(cache):
    _financial_data.set_cache(cache)


def set_prices_fetcher(prices_fetcher):
    _financial_data.set_prices_fetcher(prices_fetcher)
