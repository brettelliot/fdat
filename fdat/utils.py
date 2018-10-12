import pandas as pd
import numpy as np

__all__ = [
    'validate_standard_prices_dataframe'
]


def validate_standard_prices_dataframe(prices_df: pd.DataFrame):
    """Raises an exception if the prices_df doesn't have the right columns or types.

    Args:
        prices_df (DataFrame):
            The dataframe to be validated.

    Returns:
        None

    A valid dataframe looks like this:

    =============== =========
    Column name     type
    =============== =========
    date            object
    symbol          object
    open            float64
    high            float64
    low             float64
    close           float64
    dividend_amt    float64
    split_coeff     float64
    adj_open        float64
    adj_high        float64
    adj_low         float64
    adj_close       float64
    volume          int64
    timezone        object
    =============== =========

    """

    if not isinstance(prices_df, pd.core.frame.DataFrame):
        raise TypeError('prices_df must be a pandas.DataFrame.')

    cols = ['date', 'symbol', 'open', 'high', 'low', 'close', 'dividend_amt', 'split_coeff', 'adj_open', 'adj_high',
            'adj_low', 'adj_close', 'volume', 'timezone']

    if cols != list(prices_df):
        raise ValueError('prices_df does not have the correct columns.')

    if not isinstance(prices_df['date'].dtype, object):
        raise TypeError('prices_df["date"] must be an object.')

    if not isinstance(prices_df['symbol'].dtype, object):
        raise TypeError('prices_df["symbol"] must be an object.')

    if prices_df['open'].dtype != np.float64:
        raise TypeError('prices_df["open"] must be a float.')

    if prices_df['high'].dtype != np.float64:
        raise TypeError('prices_df["high"] must be a float.')

    if prices_df['low'].dtype != np.float64:
        raise TypeError('prices_df["low"] must be a float.')

    if prices_df['close'].dtype != np.float64:
        raise TypeError('prices_df["close"] must be a float.')

    if prices_df['dividend_amt'].dtype != np.float64:
        raise TypeError('prices_df["dividend_amt"] must be a float.')

    if prices_df['split_coeff'].dtype != np.float64:
        raise TypeError('prices_df["split_coeff"] must be a float.')

    if prices_df['adj_open'].dtype != np.float64:
        raise TypeError('prices_df["adj_open"] must be a float.')

    if prices_df['adj_high'].dtype != np.float64:
        raise TypeError('prices_df["adj_high"] must be a float.')

    if prices_df['adj_low'].dtype != np.float64:
        raise TypeError('prices_df["adj_low"] must be a float.')

    if prices_df['adj_close'].dtype != np.float64:
        raise TypeError('prices_df["adj_close"] must be a float.')

    if not isinstance(prices_df['volume'].dtype, object):
        raise TypeError('prices_df["volume"] must be an object.')

    if not isinstance(prices_df['timezone'].dtype, object):
        raise TypeError('prices_df["timezone"] must be an object.')
