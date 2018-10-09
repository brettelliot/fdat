import sqlite3
import pandas as pd
import requests
import configparser
import time
import tempfile
from .av_daily_prices_fetcher import AVDailyPricesFetcher
from .no_daily_prices_cache import NoDailyPricesCache

_default_daily_prices_cache = NoDailyPricesCache()
_default_daily_prices_fetcher = AVDailyPricesFetcher('../av_config.ini')


class FinancialData(object):
    """The FinancialData class is gateway to data from all the configured fetchers."""

    def __init__(self, daily_prices_cache=None, daily_prices_fetcher=None):
        if daily_prices_cache is not None:
            self._daily_prices_cache = daily_prices_cache
        else:
            self._daily_prices_cache = _default_daily_prices_cache

        if daily_prices_fetcher is not None:
            self._daily_prices_fetcher = daily_prices_fetcher
        else:
            self._daily_prices_fetcher = _default_daily_prices_fetcher

    def set_daily_prices_cache(self, cache):
        if cache is not None:
            self._daily_prices_cache = cache
        else:
            raise TypeError('FinancialData::get_daily_prices requires a Cache.')

    def set_daily_prices_fetcher(self, fetcher):
        if fetcher is not None:
            self._daily_prices_fetcher = fetcher
        else:
            raise TypeError('FinancialData::get_daily_prices requires a PriceFetcher.')

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

        if self._daily_prices_fetcher is None:
            raise TypeError('FinancialData::get_daily_prices requires a PriceFetcher.')

        if self._daily_prices_cache is None:
            raise TypeError('FinancialData::get_daily_prices requires a Cache.')

        # Create a list of dates strings in the format: YYYY-MM-DD
        calendar_date_range = pd.date_range(start_date, end_date)
        date_list = calendar_date_range.strftime('%Y-%m-%d').tolist()

        # Check the cache to make sure it has data for all the dates in the date range
        missing_dates = self._daily_prices_cache.check_for_missing_dates(ticker, date_list)

        # If the cache is missing some data, fetch it and add that to the cache.
        if missing_dates:
            uncached_prices_df = self._daily_prices_fetcher.get_daily_prices(ticker, start_date, end_date)
            self._daily_prices_cache.add_daily_prices(ticker, missing_dates, uncached_prices_df)

        # Return the prices that have been cached.
        return self._daily_prices_cache.get_daily_prices(ticker, start_date, end_date)


class FinancialData2(object):
    """The FinancialData class is gateway to data from all the configured providers.

    """
    def __init__(self):

        self._last_call_time = 0
        self._sleep_time = 60 / 5 + 1  # AV allows 5 requests minute

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)

        config = configparser.ConfigParser()
        config.read('../av_config.ini')
        self._av_api_key = config['AV']['AV_API_KEY']

        self.f = tempfile.NamedTemporaryFile()

        self._conn = self._create_connection(self.f.name)
        if self._conn is not None:
            self._create_daily_price_table()

        else:
            print('Error! cannot create the database connection.')

    def __del__(self):
        self._conn.close()

    def _create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            # print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

        return conn

    def _create_daily_price_table(self):
        sql = ('CREATE TABLE IF NOT EXISTS daily_data ('
               'date text NOT NULL,'
               'symbol text NOT NULL,'
               'open real NOT NULL,'
               'high real NOT NULL,'
               'low real NOT NULL,'
               'close real NOT NULL,'
               'volume integer NOT NULL,'
               'dividend_amt real,'
               'split_coeff real,'
               'adj_open real NOT NULL,'
               'adj_high real NOT NULL,'
               'adj_low real NOT NULL,'
               'adj_close real NOT NULL,'
               'PRIMARY KEY (date, symbol));')

        try:
            c = self._conn.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def get_prices(self, symbol, start_date_str, end_date_str, force_download=False):

        df = self._read_from_sql(symbol, start_date_str, end_date_str)

        if df.empty or force_download:
            df = self._download_then_adjust_and_store(symbol, start_date_str, end_date_str)
        else:
            print('Read: {}'.format(symbol))

        return df

    def _read_from_sql(self, symbol, start_date, end_date):

        # Create a query like this one:
        # SELECT * FROM daily_data WHERE symbol='AMZN' AND date between '2018-08-18' AND '2018-08-31';
        values = (symbol, start_date, end_date)
        sql = "SELECT * FROM daily_data WHERE symbol=? AND date BETWEEN ? AND ?;"

        try:
            df = pd.read_sql(sql, self._conn, index_col='date', params=values, parse_dates=['date'])
        except Exception as e:
            print(e)
            # create an empty dataframe to return
            df = pd.DataFrame({'A': []})
        return df

    def _download_then_adjust_and_store(self, symbol, start_date, end_date):

        df = self._download(symbol)
        df = self._adjust(df)
        self._store(df)
        df = self._read_from_sql(symbol, start_date, end_date)
        return df

    def _download(self, symbol):

        # Be sure not to exceed the api throttling of 1 call per second
        current_time = time.time()
        if current_time <= self._last_call_time + self._sleep_time:
            time.sleep(self._sleep_time)

        self._last_call_time = time.time()

        cleaned_symbol = self._clean_symbol(symbol)

        payload = {'apikey': self._av_api_key, 'symbol': cleaned_symbol,
                   'function': 'TIME_SERIES_DAILY_ADJUSTED', 'outputsize': 'full'}
        response = requests.get('https://www.alphavantage.co/query', params=payload)

        try:
            json_dict = response.json()
            df = pd.DataFrame.from_dict(json_dict['Time Series (Daily)'], orient="index")

            # add a column for the date and symbol
            df['symbol'] = symbol
            df['date'] = df.index

            # The columns we get back from AV are:
            # ['1. open', '2. high', '3. low', '4. close',
            # '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient']
            df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close',
                                    '5. adjusted close': 'adj_close', '6. volume': 'volume',
                                    '7. dividend amount': 'dividend_amt',
                                    '8. split coefficient': 'split_coeff'})

            print('Downloaded: {}'.format(symbol))

        except Exception as e:
            print('Error getting {} from Alpha Vantage'.format(symbol))
            print('Error: {}'.format(response.json()))
            print('Exception: {}'.format(e))
            # create an empty dataframe to return
            df = pd.DataFrame({'A': []})

        return df

    def _clean_symbol(self, symbol):
        """
        Returns a cleaned up version of the stock symbol that works with Alpha Vantage
        :param symbol: (str) The stock ticker
        :return: (str) A cleaned stock ticker that works with AlphaVantage
        """

        cleaned_symbol = symbol.replace('.', '-')
        return cleaned_symbol

    def _adjust(self, df):

        # Create adj_open, adj_high, and adj_low
        # The formulas are:
        # k = adj_close / close;
        # adj_open = k * open;
        # adj_high = k * high;
        # adj_low = k * low

        # Prior to this call all the columns were object type for some reason.
        df = df.astype({'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64',
                        'volume': 'float64', 'dividend_amt': 'float64', 'split_coeff': 'float64',
                        'adj_close': 'float64'})

        df['adj_open'] = df['adj_close'] / df['close'] * df['open']
        df['adj_high'] = df['adj_close'] / df['close'] * df['high']
        df['adj_low'] = df['adj_close'] / df['close'] * df['low']

        # reorder the columns so date and symbol are first
        df = df[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'dividend_amt', 'split_coeff',
                 'adj_open', 'adj_high', 'adj_low', 'adj_close']]

        # Prior to this call all the columns were object type for some reason.
        df = df.astype({'adj_open': 'float64', 'adj_high': 'float64', 'adj_low': 'float64', 'adj_close': 'float64'})

        return df

    def _store(self, df):

        # generate a list of tuples for each row in the dataframe
        values = list(df.itertuples(index=False))

        sql = ('REPLACE INTO daily_data'
               '(date, symbol, open, high, low, close, volume, dividend_amt, split_coeff, adj_open, adj_high, adj_low, adj_close)'
               'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);')

        cur = self._conn.cursor()
        cur.executemany(sql, values)
        self._conn.commit()

        return df
