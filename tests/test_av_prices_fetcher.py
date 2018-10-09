import unittest
import fdat


class TestAVPriceFetcher(unittest.TestCase):

    def setUp(self):

        self.fetcher = fdat.AVPricesFetcher('../av_config.ini')
        pass

    def test_get_prices_single_date(self):

        # Given fdat
        # When we call get_prices with a ticker and a date
        actual_df = self.fetcher.get_prices('SPY', '2018-08-01')

        # Then we get a dataframe with the columns we expect
        cols = ['ticker', 'open', 'high', 'low', 'close', 'volume', 'dividend_amt',
                'split_coeff', 'adj_open', 'adj_high', 'adj_low', 'adj_close']
        self.assertListEqual(actual_df.columns.values.tolist(), cols)

        # And it's got a lot of rows
        self.assertTrue(len(actual_df.index) > 4000)

        # And a random inspection of a certain date gets us the right data
        self.assertEqual(actual_df['open']['2018-08-01'], 281.56)
        self.assertEqual(actual_df.loc['2018-08-01', 'open'], 281.56)
        self.assertEqual(actual_df.loc['2018-08-01', 'high'], 282.13)
        self.assertEqual(actual_df.loc['2018-08-01', 'low'], 280.1315)
        self.assertEqual(actual_df.loc['2018-08-01', 'close'], 280.86)
        self.assertEqual(actual_df.loc['2018-08-01', 'volume'], 53853326)
        self.assertEqual(actual_df.loc['2018-08-01', 'dividend_amt'], 0.0)
        self.assertEqual(actual_df.loc['2018-08-01', 'split_coeff'], 1.0)
        self.assertEqual(actual_df.loc['2018-08-01', 'adj_open'], 280.2904)
        self.assertEqual(actual_df.loc['2018-08-01', 'adj_high'], 280.8579)
        self.assertEqual(actual_df.loc['2018-08-01', 'adj_low'], 278.8684)
        self.assertEqual(actual_df.loc['2018-08-01', 'adj_close'], 279.5936)


if __name__ == '__main__':
    unittest.main()
