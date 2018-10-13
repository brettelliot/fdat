import unittest
import fdat


class TestAVDailyPriceFetcher(unittest.TestCase):

    def setUp(self):

        self.fetcher = fdat.AVDailyPricesFetcher('../av_config.ini')
        pass

    def test_get_daily_prices_single_date(self):

        # Given fdat
        # When we call get_daily_prices with a ticker and a date
        actual_df = self.fetcher.get_daily_prices('SPY', '2018-08-01')

        try:
            # Then we get a dataframe with the columns we expect
            fdat.validate_standard_prices_dataframe(actual_df)
        except Exception as e:
            self.fail(e)

        # And it's got a lot of rows
        self.assertTrue(len(actual_df.index) > 4000)

        # Inspect the data we get back. First using a query method:
        actual = actual_df.query('date == "2018-08-01" & symbol == "SPY"')['open'].item()
        self.assertEqual(actual, 281.56)

        # Next using variable attributes
        actual = actual_df[(actual_df['date']=='2018-08-01') & (actual_df['symbol']=='SPY')]['high'].item()
        self.assertEqual(actual, 282.13)

        # and finally using the cleanest method... resetting the index
        actual_df = actual_df.set_index(['date', 'symbol'])
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['open'], 281.56)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['high'], 282.13)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['low'], 280.1315)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['close'], 280.86)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['volume'], 53853326)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['dividend_amt'], 0.0)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['split_coeff'], 1.0)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['adj_open'], 280.2904)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['adj_high'], 280.8579)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['adj_low'], 278.8684)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['adj_close'], 279.5936)
        self.assertEqual(actual_df.loc['2018-08-01', 'SPY']['timezone'], 'US/Eastern')


if __name__ == '__main__':
    unittest.main()
