import unittest
import fdat
import pandas as pd
from pandas.util.testing import assert_frame_equal
import datetime


"""
class MockFetcher(ecal.AbstractFetcher):

    def __init__(self):
        sample_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04']}

        sample_df = pd.DataFrame.from_dict(sample_dict)
        sample_df = sample_df.set_index('date')
        sample_df = sample_df[['ticker', 'when']]
        self.calendar_df = sample_df

    def fetch_calendar(self, start_date_str, end_date_str=None):
        return self.calendar_df
"""


class TestFdatGetDailyPrices(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_daily_prices_single_date(self):

        # Given fdat
        # When we call get_daily_prices with a ticker and a date
        actual_df = fdat.get_daily_prices('SPY', '2018-08-01')

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
