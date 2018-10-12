import unittest
import fdat
import pandas as pd


class TestValidateStandardPricesDataframe(unittest.TestCase):

    def test_not_a_dataframe(self):

        # Given some data that is not a pandas.DataFrame,
        actual = 'some_data'

        # When it's passed to validate_standard_prices_dataframe
        try:
            fdat.utils.validate_standard_prices_dataframe(actual)
            self.fail('A TypeError exception should have been raised.')
        except TypeError:
            # Then a TypeError exception should be raised.
            pass
        except Exception as e:
            self.fail('TypeError exception should have been raised.')

    def test_is_a_dataframe_with_the_wrong_columns(self):

        # Given some data that is a pandas.DataFrame but missing columns
        actual = pd.DataFrame()

        # When it's passed to validate_standard_prices_dataframe
        try:
            fdat.utils.validate_standard_prices_dataframe(actual)
            self.fail('A ValueError exception should have been raised.')
        except ValueError:
            # Then a ValueError exception should be raised since the columns are incorrect.
            pass
        except Exception as e:
            self.fail('A ValueError exception should have been raised.')

    def test_is_a_dataframe_with_the_correct_columns_but_incorrect_types(self):

        # Given some data that is a pandas.DataFrame with columns but missing type data
        cols = ['date', 'symbol', 'open', 'high', 'low', 'close', 'dividend_amt', 'split_coeff', 'adj_open', 'adj_high',
                'adj_low', 'adj_close', 'volume', 'timezone']
        actual = pd.DataFrame(columns=cols)

        # When it's passed to validate_standard_prices_dataframe
        try:
            fdat.utils.validate_standard_prices_dataframe(actual)
            self.fail('A TypeError exception should have been raised.')
        except TypeError:
            # Then a Type exception should be raised since the columns have incorrect types.
            pass
        except Exception as e:
            self.fail('A TypeError exception should have been raised.')

    def test_is_a_dataframe_with_the_correct_columns_and_types(self):

        # Given some data that is a pandas.DataFrame with the right columns and types
        cols = ['date', 'symbol', 'open', 'high', 'low', 'close', 'dividend_amt', 'split_coeff', 'adj_open', 'adj_high',
                'adj_low', 'adj_close', 'volume', 'timezone']
        actual = pd.DataFrame(columns=cols)

        # Prior to this call all the columns were object type for some reason.
        actual = actual.astype({'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64',
                                'dividend_amt': 'float64', 'split_coeff': 'float64',
                                'adj_open': 'float64', 'adj_high': 'float64',
                                'adj_low': 'float64', 'adj_close': 'float64',
                                'volume': 'int64', 'timezone': 'object'})

        # When it's passed to validate_standard_prices_dataframe
        try:
            fdat.utils.validate_standard_prices_dataframe(actual)
        except Exception as e:
            self.fail('A TypeError exception should have been raised.')
