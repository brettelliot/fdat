import fdat

prices_df = fdat.get_prices('SPY', start_date_str='2017-08-01', end_date_str='2017-08-31', force_download=True)
print(prices_df)
