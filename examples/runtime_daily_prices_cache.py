import fdat
import time

# Tell fdat not to use the runtime cache any daily price data.
fdat.set_daily_prices_cache(fdat.RuntimeDailyPricesCache())

ticker = 'SPY'
start_date = '2018-08-01'
end_date = '2018-08-03'

pre_call_time = time.time()
prices_df1 = fdat.get_daily_prices(ticker, start_date)
call_time = time.time() - pre_call_time
print('The 1st call to fdat.get_daily_prices() took {0:.2f} seconds'.format(call_time))

pre_call_time = time.time()
prices_df2 = fdat.get_daily_prices(ticker, start_date, end_date)
call_time = time.time() - pre_call_time
print('The 2nd call to fdat.get_daily_prices() took {0:.2f} seconds'.format(call_time))
print(prices_df2)
