import numpy as np
from datetime import datetime
from robin_stocks import robinhood as rh


def get_underlying(pd, underlying_stock_symbol):
    underlying = pd.DataFrame.from_dict(rh.get_quotes(underlying_stock_symbol))
    underlying['Last'] = float(underlying['last_trade_price'])
    return underlying


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


def filter_for_leaps(pd, chain, min_to_expire):
    old_contracts = []
    # print(chain)
    contracts = pd.DataFrame.from_dict({'Expires': pd.to_datetime(chain['expiration_dates'])})    # todo convert to dataframe return
    contracts['Days'] = contracts['Expires'] - datetime.today()
    # print(pd.Timedelta(days=min_to_expire))
    leaps = contracts[contracts.Expires > datetime.now() + pd.Timedelta(days=min_to_expire)]
    # print(contracts)
    # for contract in chain['expiration_dates']:
    #     date_time_str = datetime.strptime(contract, '%Y-%m-%d')
    #     days_to_expire = (date_time_str - datetime.today()).days
    #     if days_to_expire > min_to_expire:
    #         old_contracts.append({'contract': date_time_str.strftime("%Y-%m-%d"), 'days_to_expire': days_to_expire})
    #         print(date_time_str.strftime("%Y-%m-%d"), days_to_expire, 'days out')

    return leaps


def get_put_leaps(pd, scan, underlying_average_std_dev, underlying, underlying_stock_symbol):
    option_chains = rh.options.get_chains(underlying_stock_symbol)
    # print(option_chains)
    leaps = filter_for_leaps(pd, option_chains, scan.leaps_min_days)  # Manually picking contract for quicker testing
    # leaps = pd.DataFrame.from_dict([{'contract': '2023-06-16', 'days_to_expire': 734}])

    # for leap in leaps:
    for index, leap in leaps.iterrows():
        print(leap['Expires'].strftime('%Y-%m-%d'))
        option_data = pd.DataFrame.from_dict(rh.find_options_by_expiration(
            underlying_stock_symbol, expirationDate=leap['Expires'].strftime('%Y-%m-%d'), optionType='put'))
        option_data['Days'] = leap['Days'].days
        option_data['Strike'] = round(option_data.strike_price.astype('float')).astype('int32')
        option_data['Bid'] = round(option_data['bid_price'].astype('float'), 2)
        option_data['Ask'] = round(option_data['ask_price'].astype('float'), 2)
        option_data['Mid'] = round(((option_data['Ask'] - option_data['Bid']) *
                                    scan.options_bid_ask_midpoint) + option_data['Ask'], 2)
        option_data['Mid/Strike Return'] = round((option_data['Mid'] / option_data['Strike']) * 100, 2)
        option_data['Annualized'] = round((scan.annualized_return_days / option_data['Days']) *
                                          option_data['Mid/Strike Return'], 2)
        option_data['OTM'] = underlying['Last'][0] - option_data['Strike']
        option_data.sort_values('Strike', inplace=True)
        option_data.rename(columns={'expiration_date': 'Expiration', 'open_interest': 'OI'}, inplace=True)
        # print(option_data.head())

        strike_range = option_data[
            option_data.OTM.between(underlying_average_std_dev, underlying_average_std_dev * 2)]
        # print(strike_range.style.format({'Mid/Strike': '{:.2%}'}).render())
        print(strike_range[['Expiration', 'Days', 'Strike', 'OTM', 'OI', 'Bid', 'Ask', 'Mid', 'Mid/Strike Return',
                            'Annualized']])
