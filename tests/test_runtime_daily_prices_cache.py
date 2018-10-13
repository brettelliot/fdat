import unittest
import fdat
import time
import pandas as pd
import datetime


class MockRuntimeDailyPricesCache(fdat.RuntimeDailyPricesCache):
    """Setup a mock cache data 8/1/2018 cached."""

    def __init__(self):
        super().__init__()

        # Seed the cache with some data
        self._keys = {'2018-08-01,SPY'}

        # Seed the cache with some data
        data = {'date': ['2018-08-01'],
                'symbol': ['SPY'],
                'open': [281.56],
                'high': [282.13],
                'low': [280.1315],
                'close': [280.86],
                'dividend_amt': [0.0],
                'split_coeff': [1.0],
                'adj_open': [280.2904],
                'adj_high': [280.8579],
                'adj_low': [278.8684],
                'adj_close': [279.5936],
                'volume': [53853326],
                'timezone': ['US/Eastern']
                }

        self._cache_df = pd.DataFrame(data)

        cols = fdat.standard_prices_dataframe_column_order()
        self._cache_df = self._cache_df[cols]


class TestRuntimeDailyPricesCache(unittest.TestCase):

    def setUp(self):
        pass

    def test_first_call_is_slow_and_second_call_is_fast(self):
        fdat.set_daily_prices_cache(fdat.RuntimeDailyPricesCache())
        symbol = 'SPY'
        date = '2018-08-01'

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(symbol, date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time > 1.0)

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(symbol, date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time < 1.0)

    def test_check_for_missing_dates_that_are_in_the_cache(self):

        # Given a RuntimeDailyPricesCache
        cache = MockRuntimeDailyPricesCache()

        # When we are checking dates that are already in the cache
        symbol = 'SPY'
        dates = ['2018-08-01']
        actual = cache.check_for_missing_dates(symbol, dates)

        # Then we should find them and no missing dates should be returned
        expected = []
        self.assertListEqual(actual, expected)

    def test_check_for_missing_dates_that_are_not_in_the_cache(self):

        # Given a RuntimeDailyPricesCache
        cache = MockRuntimeDailyPricesCache()

        # When we are checking dates that are not already in the cache
        symbol = 'SPY'
        dates = ['2018-08-31']
        actual = cache.check_for_missing_dates(symbol, dates)

        # Then we shouldn't find them and they should be returned back to us as a missing date
        expected = ['2018-08-31']
        self.assertListEqual(actual, expected)

    def test_add_daily_prices(self):

        # Given a RuntimeDailyPricesCache
        cache = MockRuntimeDailyPricesCache()

        # When we add some new pricing data to the cache
        symbol = 'SPY'
        date = '2018-08-02'
        data = {'date': [date],
                'symbol': [symbol],
                'open': [300.00],
                'high': [400.00],
                'low': [200.00],
                'close': [350.00],
                'dividend_amt': [0.0],
                'split_coeff': [1.0],
                'adj_open': [300.00],
                'adj_high': [400.00],
                'adj_low': [200.00],
                'adj_close': [350.00],
                'volume': [66666666],
                'timezone': ['US/Eastern']
                }

        uncached_prices_df = pd.DataFrame(data)
        cols = fdat.standard_prices_dataframe_column_order()
        uncached_prices_df = uncached_prices_df[cols]
        fdat.validate_standard_prices_dataframe(uncached_prices_df)

        assert('2018-08-02,SPY' not in cache._keys)
        cache.add_daily_prices(symbol, [date], uncached_prices_df)

        # Then it's added to the _cache_df
        self.assertEqual(len(cache._cache_df), 2)
        new_row = cache._cache_df.loc[(cache._cache_df['date'] == '2018-08-02') & (cache._cache_df['symbol'] == 'SPY')]
        self.assertEqual(new_row.at[0, 'open'], 300.00)
        self.assertEqual(new_row.at[0, 'adj_close'], 350.00)

        # And it's added to the _keys
        assert ('2018-08-02,SPY' in cache._keys)

    def test_get_daily_prices(self):

        # Given a cache with some data
        cache = MockRuntimeDailyPricesCache()

        # When asked to provide the prices data for a date
        symbol = 'SPY'
        start_date = '2018-08-01'
        prices_df = cache.get_daily_prices(symbol, start_date)
        fdat.validate_standard_prices_dataframe(prices_df)

        # Then theres a row in the cache with the values we seeded the cache with.
        self.assertEqual(len(prices_df), 1)
        actual = prices_df.query('date == @start_date & symbol == @symbol')['adj_close'].item()
        self.assertEqual(actual, 279.5936)
        actual = prices_df.query('date == @start_date & symbol == @symbol')['close'].item()
        self.assertEqual(actual, 280.86)



if __name__ == '__main__':
    unittest.main()
