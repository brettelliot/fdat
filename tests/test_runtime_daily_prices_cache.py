import unittest
import fdat
import time
import pandas as pd


class MockRuntimeDailyPricesCache(fdat.RuntimeDailyPricesCache):
    """Setup a mock cache data 8/1/2018 cached."""

    def __init__(self):
        super().__init__()

        # Seed the cache with some data
        self._keys_df = self._keys_df.append({'keys': '2018-08-01,SPY'}, ignore_index=True)


class TestRuntimeDailyPricesCache(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skip("Skipping test_first_call_is_slow_and_second_call_is_fast")
    def test_first_call_is_slow_and_second_call_is_fast(self):
        fdat.set_daily_prices_cache(fdat.RuntimeDailyPricesCache())
        ticker = 'SPY'
        date = '2018-08-01'

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(ticker, date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time > 1.0)

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(ticker, date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time > 1.0)

    def test_check_for_missing_dates_that_are_in_the_cache(self):

        # Given a RuntimeDailyPricesCache
        cache = MockRuntimeDailyPricesCache()

        # When we are checking dates that are already in the cache
        dates = ['2018-08-01']
        actual = cache.check_for_missing_dates('SPY', dates)

        # Then we should find them and no missing dates should be returned
        expected = []
        self.assertListEqual(actual, expected)

    def test_check_for_missing_dates_that_are_not_in_the_cache(self):

        # Given a RuntimeDailyPricesCache
        cache = MockRuntimeDailyPricesCache()

        # When we are checking dates that are not already in the cache
        dates = ['2018-08-31']
        actual = cache.check_for_missing_dates('SPY', dates)

        # Then we shouldn't find them and they should be returned back to us as a missing date
        expected = ['2018-08-31']
        self.assertListEqual(actual, expected)




if __name__ == '__main__':
    unittest.main()
