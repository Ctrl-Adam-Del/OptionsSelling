from robin_data import get_put_leaps, get_underlying_stocks
from utility import authenticate_robinhood


def run(scan):
    authenticate_robinhood()

    underlying_stock_quotes = get_underlying_stocks(scan)

    for underlying in underlying_stock_quotes.iterrows():

        get_put_leaps(scan, underlying)
