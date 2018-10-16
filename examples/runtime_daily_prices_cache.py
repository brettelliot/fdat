import fdat
import time

# Tell fdat not to use the runtime cache any daily price data.
fdat.set_daily_prices_cache(fdat.RuntimeDailyPricesCache())

symbols = ['SPY', 'XOM']
start_date = '2018-08-01'
end_date = '2018-08-03'

for symbol in symbols:
    pre_call_time = time.time()
    prices_df1 = fdat.get_daily_prices(symbol, start_date)
    call_time = time.time() - pre_call_time
    print('{0}: The 1st call to fdat.get_daily_prices() took {1:.2f} seconds'.format(symbol, call_time))
    print(prices_df1)

    pre_call_time = time.time()
    prices_df2 = fdat.get_daily_prices(symbol, start_date, end_date)
    call_time = time.time() - pre_call_time
    print('{0}: The 2nd call to fdat.get_daily_prices() took {1:.2f} seconds'.format(symbol, call_time))
    print(prices_df2)
