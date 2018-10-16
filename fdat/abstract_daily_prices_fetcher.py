

__all__ = [
    'AbstractDailyPricesFetcher'
]


class AbstractDailyPricesFetcher(object):

    def get_daily_prices(self, symbol: str, start_date: str, end_date: str):
        """Implement this method in derived classes.

        In the derived class use fdata.utils.validate_standard_prices_dataframe() to ensure the DataFrame
        being returned by get_daily_prices() is valid.

        Args:
            symbol (str):
                The ticker symbol
            start_date (str):
                The start date of the prices to fetch in the format ``YYYY-MM-DD``.
            end_date (str):
                The end date of the prices to get in the format ``YYYY-MM-DD``. If left out, we will fetch
                prices for the start date.

        Returns:
            DataFrame:
                Returns a valid standard prices DataFrame.


        """
        raise NotImplementedError('AbstractDailyPricesFetcher::_get_daily_prices is an abstract method \
                                    and cannot be called.')
