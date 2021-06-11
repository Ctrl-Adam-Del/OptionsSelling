from robin_data import underlying_historical, get_put_leaps, get_underlying
from utility import authenticate_robinhood


def run(scan, pd):
    authenticate_robinhood()

    underlying_stock_symbol = 'TSLA'

    underlying = get_underlying(pd, underlying_stock_symbol)
    underlying_average_std_dev = underlying_historical(pd, scan, underlying['Last'], underlying_stock_symbol)
    print(f'{underlying_stock_symbol} Last: ${underlying["Last"][0]:.2f} '
          f'Average StdDev: {underlying_average_std_dev:.2f}')

    get_put_leaps(pd, scan, underlying_average_std_dev, underlying, underlying_stock_symbol)


