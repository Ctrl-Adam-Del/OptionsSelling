from datetime import datetime

import numpy as np
from robin_stocks import robinhood as rh


def get_leaps(chain, min_to_expire):
    contracts = []
    for contract in chain['expiration_dates']:
        date_time_str = datetime.strptime(contract, '%Y-%m-%d')
        days_to_expire = (date_time_str - datetime.today()).days
        if days_to_expire > min_to_expire:
            contracts.append({'contract': date_time_str.strftime("%Y-%m-%d"), 'days_to_expire': days_to_expire})
            print(date_time_str.strftime("%Y-%m-%d"), days_to_expire, 'days out')
    return contracts


def underlying_historical(pd, scan, underlying_last, underlying_stock_symbol):
    underlying_history = pd.DataFrame.from_dict(rh.get_stock_historicals(underlying_stock_symbol,
                                                                         interval='day', span='5year'))
    underlying_1year_std_dev = underlying_history.tail(
        scan.annual_trading_days)['close_price'].astype('float').std()
    underlying_2year_std_dev = underlying_history.tail(
        scan.annual_trading_days * 2)['close_price'].astype('float').std()
    underlying_5year_std_dev = underlying_history.tail(
        scan.annual_trading_days * 5)['close_price'].astype('float').std()
    underlying_average_std_dev = np.average(
        [underlying_1year_std_dev, underlying_2year_std_dev, underlying_5year_std_dev])
    # print(underlying_history)
    # print(f'{underlying_stock_symbol} Last: ${underlying_last:.2f} 1yrStdDev: {underlying_1year_std_dev:.2f} '
    #       f'2yrStdDev: {underlying_2year_std_dev:.2f} 5yrStdDev: {underlying_5year_std_dev:.2f} '
    #       f'Average StdDev: {underlying_average_std_dev:.2f}')
    return underlying_average_std_dev
