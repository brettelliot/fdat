from .financial_data import FinancialData

_financial_data = FinancialData()

__all__ = [
    'get_prices'
]


def get_prices(ticker_str, start_date_str, end_date_str=None, force_download=False):

    if end_date_str is None:
        end_date_str = start_date_str

    return _financial_data.get_prices(ticker_str, start_date_str, end_date_str, force_download)
