import unittest
import fdat
import time


class TestNoDailyPricesCache(unittest.TestCase):

    def setUp(self):
        fdat.set_daily_prices_cache(fdat.NoDailyPricesCache())

    def test_first_and_second_calls_are_slow(self):
        symbol = 'SPY'
        start_date = '2018-08-01'

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(symbol, start_date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time > 1.0)

        pre_call_time = time.time()
        prices_df = fdat.get_daily_prices(symbol, start_date)
        self.assertFalse(prices_df.empty)
        call_time = time.time() - pre_call_time
        self.assertTrue(call_time > 1.0)


if __name__ == '__main__':
    unittest.main()
