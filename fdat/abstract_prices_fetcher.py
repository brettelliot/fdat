__all__ = [
    'AbstractPricesFetcher'
]


class AbstractPricesFetcher(object):

    def get_prices(self, ticker, start_date_str, end_date_str):
        """Implement this method! Your method should return a pandas DataFrame.

        Args:
            ticker (str):
                The ticker symbol
            start_date_str (str):
                The start date of the prices to fetch in the format ``YYYY-MM-DD``.
            end_date_str (str):
                The end date of the prices to get in the format ``YYYY-MM-DD``. If left out, we will fetch
                prices for the start date.

        Returns:
            DataFrame:
                Returns a pandas DataFrame indexed by ``date``, that has columns:
                ``ticker``, ``open``, ``high``, ``low``, ``close``,
                ``dividend_amt``, ``split_coeff``,
                ``adj_open``, ``adj_high``, ``adj_low``, and ``adj_close``.

        """
        raise NotImplementedError('AbstractPricesFetcher::get_prices is an abstract method and cannot be called.')
