from .abstract_daily_prices_fetcher import AbstractDailyPricesFetcher
import configparser
import pandas as pd
import time
import requests

__all__ = [
    'AVDailyPricesFetcher'
]


class AVDailyPricesFetcher(AbstractDailyPricesFetcher):

    def __init__(self, config_file_path):
        self._last_call_time = 0
        self._sleep_time = 60 / 5 + 1  # AV allows 5 requests minute

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)

        config = configparser.ConfigParser()
        config.read(config_file_path)
        self._av_api_key = config['AV']['AV_API_KEY']

    def get_daily_prices(self, ticker, start_date_str, end_date_str=None):
        """Get prices from AlphaVantage as a pandas DataFrame.

        AlphaVantage returns all prices from 1/1/2000 (if available) in one shot. Therefore
        ``get_daily_prices`` will return everything in order to cache it so it doesn't have to call the AB API aagin.

        Args:
            ticker (str):
                The ticker symbol
            start_date_str (str):
                Ignored, since AlphaVantage returns everything.
            end_date_str (str):
                Ignored, since AlphaVantage returns everything.

        Returns:
            DataFrame:
                Returns a pandas DataFrame indexed by ``date``, that has columns:
                ``ticker``, ``open``, ``high``, ``low``, ``close``,
                ``dividend_amt``, ``split_coeff``,
                ``adj_open``, ``adj_high``, ``adj_low``, and ``adj_close``.

        """
        return self._download_then_adjust(ticker)

    def _download_then_adjust(self, ticker):

        df = self._download(ticker)
        df = self._adjust(df)
        return df

    def _download(self, ticker):

        # Be sure not to exceed the api throttling of 1 call per second
        current_time = time.time()
        if current_time <= self._last_call_time + self._sleep_time:
            time.sleep(self._sleep_time)

        self._last_call_time = time.time()

        cleaned_symbol = self._clean_ticker(ticker)

        payload = {'apikey': self._av_api_key, 'symbol': cleaned_symbol,
                   'function': 'TIME_SERIES_DAILY_ADJUSTED', 'outputsize': 'full'}
        response = requests.get('https://www.alphavantage.co/query', params=payload)

        try:
            json_dict = response.json()
            df = pd.DataFrame.from_dict(json_dict['Time Series (Daily)'], orient="index")

            # add a column for the date and ticker
            df['ticker'] = ticker
            df.index = pd.to_datetime(df.index)

            # The columns we get back from AV are:
            # ['1. open', '2. high', '3. low', '4. close',
            # '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient']
            df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close',
                                    '5. adjusted close': 'adj_close', '6. volume': 'volume',
                                    '7. dividend amount': 'dividend_amt',
                                    '8. split coefficient': 'split_coeff'})

            print('Downloaded: {}'.format(ticker))

        except Exception as e:
            print('Error getting {} from Alpha Vantage'.format(ticker))
            print('Error: {}'.format(response.json()))
            print('Exception: {}'.format(e))
            # create an empty dataframe to return
            df = pd.DataFrame({'A': []})

        return df

    @staticmethod
    def _clean_ticker(ticker):
        """Returns a cleaned up version of the stock ticker that works with Alpha Vantage

        Args:
            ticker (str):
             The stock ticker

        Returns:
            str:
                A cleaned stock ticker that works with AlphaVantage
        """

        cleaned_ticker = ticker.replace('.', '-')
        return cleaned_ticker

    @staticmethod
    def _adjust(df):

        # Create adj_open, adj_high, and adj_low
        # The formulas are:
        # k = adj_close / close;
        # adj_open = k * open;
        # adj_high = k * high;
        # adj_low = k * low

        # Prior to this call all the columns were object type for some reason.
        df = df.astype({'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64',
                        'volume': 'int64', 'dividend_amt': 'float64', 'split_coeff': 'float64',
                        'adj_close': 'float64'})

        df['adj_open'] = df['adj_close'] / df['close'] * df['open']
        df['adj_high'] = df['adj_close'] / df['close'] * df['high']
        df['adj_low'] = df['adj_close'] / df['close'] * df['low']

        # reorder the columns ticker first
        df = df[['ticker', 'open', 'high', 'low', 'close', 'volume', 'dividend_amt', 'split_coeff',
                 'adj_open', 'adj_high', 'adj_low', 'adj_close']]

        # Prior to this call all the columns were object type for some reason.
        df = df.astype({'adj_open': 'float64', 'adj_high': 'float64', 'adj_low': 'float64', 'adj_close': 'float64'})

        # df = pd.Series([11, 16, 21]).apply(lambda x: custom_round(x, base=5))
        df = df.round(4)

        return df




