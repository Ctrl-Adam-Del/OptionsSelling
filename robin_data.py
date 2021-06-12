import numpy as np
from datetime import datetime
from robin_stocks import robinhood as rh


def get_underlying_stocks(scan):
    if scan.underlying_stock_symbol_testing:
        underlying_symbols = scan.pd.DataFrame(scan.underlying_stock_symbol_testing)
    else:
        underlying_symbols = scan.pd.read_csv(scan.underlying_stock_symbol_import, index_col=0, parse_dates=True)

    quote_count = 0
    underlying_stock_quotes = None
    for underlying in underlying_symbols.iterrows():
        stock_quote = scan.pd.DataFrame.from_dict(rh.get_quotes(underlying[1]['Ticker Symbol']))
        stock_quote['StdDevAvg'] = underlying_std_dev(scan, stock_quote['symbol'][0])
        # print(stock_quote['symbol'][0])
        if quote_count > 0:
            underlying_stock_quotes = scan.pd.concat([underlying_stock_quotes, stock_quote])
        else:
            underlying_stock_quotes = stock_quote
        quote_count += 1

    underlying_stock_quotes['Last'] = underlying_stock_quotes['last_trade_price'].apply(scan.pd.to_numeric)

    return underlying_stock_quotes


def underlying_std_dev(scan, underlying_stock_symbol):
    underlying_history = scan.pd.DataFrame.from_dict(rh.get_stock_historicals(underlying_stock_symbol,
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
    return round(underlying_average_std_dev, 1)


def filter_for_leaps(pd, chain, min_to_expire):
    contracts = pd.DataFrame.from_dict({'Expires': pd.to_datetime(chain['expiration_dates'])})
    contracts['Days'] = contracts['Expires'] - datetime.today()
    leaps = contracts[contracts.Expires > datetime.now() + pd.Timedelta(days=min_to_expire)]
    return leaps


def get_put_leaps(scan, underlying):
    option_chains = rh.options.get_chains(underlying[1]['symbol'])
    leaps = filter_for_leaps(scan.pd, option_chains, scan.leaps_min_days)  # Manual contract for quicker testing
    # leaps = pd.DataFrame.from_dict([{'contract': '2023-06-16', 'days_to_expire': 734}])

    # for leap in leaps:
    for index, leap in leaps.iterrows():
        option_data = scan.pd.DataFrame.from_dict(rh.find_options_by_expiration(
            underlying[1]['symbol'], expirationDate=leap['Expires'].strftime('%Y-%m-%d'), optionType='put'))
        option_data['Symbol'] = underlying[1]['symbol']
        option_data['StdDevAvg'] = underlying[1]['StdDevAvg']
        option_data['Days'] = leap['Days'].days
        option_data['Strike'] = option_data.strike_price.apply(scan.pd.to_numeric)
        option_data['Bid'] = round(option_data['bid_price'].apply(scan.pd.to_numeric), 2)
        option_data['Ask'] = round(option_data['ask_price'].apply(scan.pd.to_numeric), 2)
        option_data['Mid'] = round(((option_data['Ask'] - option_data['Bid']) *
                                    scan.options_bid_ask_midpoint) + option_data['Ask'], 2)
        option_data['Return'] = round((option_data['Mid'] / option_data['Strike']) * 100, 2)
        option_data['Annual'] = round((scan.annualized_return_days / option_data['Days']) *
                                          option_data['Return'], 2)
        option_data['OTM'] = underlying[1]['Last'] - option_data['Strike']
        option_data.sort_values('Strike', inplace=True)
        option_data.rename(columns={'expiration_date': 'Expiration', 'open_interest': 'OI'}, inplace=True)
        # print(option_data.head())

        strike_range = option_data[
            option_data.OTM.between(underlying[1]['StdDevAvg'], underlying[1]['StdDevAvg'] * 2)]
        # print(strike_range.style.format({'Mid/Strike': '{:.2%}'}).render())
        print('\nContract: ', leap['Expires'].strftime('%Y-%m-%d'))
        print(strike_range[['Symbol', 'StdDevAvg', 'Expiration', 'Days', 'Strike', 'OTM', 'OI', 'Bid', 'Ask', 'Mid',
                            'Return', 'Annual']])
