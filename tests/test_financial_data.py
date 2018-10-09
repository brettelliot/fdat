import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import fdat


class TestFinancialData(unittest.TestCase):

    def setUp(self):

        # Given an instance of FinancialData with the default cache and fetchers
        self.fd = fdat.FinancialData()

    def test_default_get_daily_prices_single_date(self):

        # When we call get_daily_prices with a ticker and a date
        actual_df = self.fd.get_daily_prices('SPY', '2018-08-01')

        #actual_df['date'] = actual_df.index
        #print(actual_df.to_dict(orient='list'))

        expected_dict = {'ticker': ['SPY'],
                         'open': [281.56], 'high': [282.13], 'low': [280.1315], 'close': [280.86],
                         'volume': [53853326], 'dividend_amt': [0.0], 'split_coeff': [1.0],
                         'adj_open': [280.2904], 'adj_high': [280.8579],
                         'adj_low': [278.8684], 'adj_close': [279.5936]}
        expected_df = pd.DataFrame.from_dict(expected_dict)
        expected_df.index = pd.to_datetime(['2018-08-01'])
        cols = ['ticker', 'open', 'high', 'low', 'close', 'volume', 'dividend_amt',
                'split_coeff', 'adj_open', 'adj_high', 'adj_low', 'adj_close']
        expected_df = expected_df[cols]

        # Then we should get a dataframe with all the data back.
        assert_frame_equal(actual_df, expected_df)


if __name__ == '__main__':
    unittest.main()
