import unittest
import fdat


class TestAVDailyPriceFetcher(unittest.TestCase):

    def setUp(self):

        self.fetcher = fdat.AVDailyPricesFetcher('../av_config.ini')
        pass

    def test_get_daily_prices_single_date(self):

        # Given fdat
        # When we call get_daily_prices with a ticker and a date
        symbol = 'SPY'
        start_date = '2018-08-01'
        actual_df = self.fetcher.get_daily_prices(symbol, start_date)

        try:
            # Then we get a dataframe with the columns we expect
            fdat.validate_standard_prices_dataframe(actual_df)
        except Exception as e:
            self.fail(e)

        # And it's got a lot of rows
        self.assertTrue(len(actual_df.index) > 4000)

        # Inspect the data we get back. First using a query method:
        actual = actual_df.query('date == @start_date & symbol == @symbol')['open'].item()
        self.assertEqual(actual, 281.56)

        # Next using variable attributes
        actual = actual_df[(actual_df['date'] == start_date) & (actual_df['symbol'] == symbol)]['high'].item()
        self.assertEqual(actual, 282.13)

        # and finally using the cleanest method... resetting the index
        actual_df = actual_df.set_index(['date', 'symbol'])
        self.assertEqual(actual_df.loc[start_date, symbol]['open'], 281.56)
        self.assertEqual(actual_df.loc[start_date, symbol]['high'], 282.13)
        self.assertEqual(actual_df.loc[start_date, symbol]['low'], 280.1315)
        self.assertEqual(actual_df.loc[start_date, symbol]['close'], 280.86)
        self.assertEqual(actual_df.loc[start_date, symbol]['volume'], 53853326)
        self.assertEqual(actual_df.loc[start_date, symbol]['dividend_amt'], 0.0)
        self.assertEqual(actual_df.loc[start_date, symbol]['split_coeff'], 1.0)
        self.assertEqual(actual_df.loc[start_date, symbol]['adj_open'], 280.2904)
        self.assertEqual(actual_df.loc[start_date, symbol]['adj_high'], 280.8579)
        self.assertEqual(actual_df.loc[start_date, symbol]['adj_low'], 278.8684)
        self.assertEqual(actual_df.loc[start_date, symbol]['adj_close'], 279.5936)
        self.assertEqual(actual_df.loc[start_date, symbol]['timezone'], 'US/Eastern')


if __name__ == '__main__':
    unittest.main()
