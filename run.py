import robin_stocks.robinhood as rh
from robin_data import underlying_historical
from utility import authenticate_robinhood


def run(scan, pd):
    authenticate_robinhood()

    underlying_stock_symbol = 'TSLA'
    underlying = rh.get_quotes(underlying_stock_symbol)
    underlying_last = float(underlying[0]['last_trade_price'])

    # my_holdings = rh.build_holdings()
    # underlying = rh.get_instruments_by_symbols('tsla')

    underlying_average_std_dev = underlying_historical(pd, scan, underlying_last, underlying_stock_symbol)
    print(f'{underlying_stock_symbol} Last: ${underlying_last:.2f} Average StdDev: {underlying_average_std_dev:.2f}')

    option_chains = rh.options.get_chains(underlying_stock_symbol)  # todo force to puts?
    # leaps = get_leaps(option_chains, scan.leaps_min_days)
    leaps = [{'contract': '2023-06-16', 'days_to_expire': '734'}]

    for leap in leaps:
        option_data = pd.DataFrame.from_dict(rh.find_options_by_expiration(
            underlying_stock_symbol, expirationDate=leap['contract'], optionType='put'))
        print(leap['contract'])
        option_data['Strike'] = round(option_data.strike_price.astype('float')).astype('int32')
        option_data['Bid'] = round(option_data['bid_price'].astype('float'), 2)
        option_data['Ask'] = round(option_data['ask_price'].astype('float'), 2)
        option_data['OTM'] = underlying_last - option_data['Strike']
        option_data.sort_values('Strike', inplace=True)
        option_data.rename(columns={'expiration_date': 'Expiration', 'open_interest': 'OI'}, inplace=True)
        # print(optionData.head())

        strike_range = option_data[
            option_data.OTM.between(underlying_average_std_dev, underlying_average_std_dev * 2)]
        print(strike_range[['Expiration', 'Strike', 'OTM', 'OI', 'Bid', 'Ask']])


