import fdat

prices_df = fdat.get_daily_prices('SPY', '2018-08-01')
print(prices_df)