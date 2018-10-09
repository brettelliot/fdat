import fdat

prices_df = fdat.get_prices('SPY', '2018-01-01', '2018-01-31')
print(prices_df)
