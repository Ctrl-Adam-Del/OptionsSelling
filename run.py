from robin_data import underlying_std_dev, get_put_leaps, get_underlying_stocks
from utility import authenticate_robinhood


def run(scan, pd):
    authenticate_robinhood()

    underlying_stock_quotes = get_underlying_stocks(scan)
    # underlying_average_std_dev = underlying_std_dev(scan, underlying_stock_symbol)
    # print(f'{underlying_stock_symbol} Last: ${underlying["Last"][0]:.2f} '
    #       f'Average StdDev: {underlying_average_std_dev:.2f}')

    for underlying in underlying_stock_quotes.iterrows():

        get_put_leaps(scan, underlying)
