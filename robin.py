import robin_stocks.robinhood as rh
import pandas as pd
from robin_data import get_leaps
from utility import authenticate_robinhood


authenticate_robinhood()
pd.set_option('display.max_columns', None, 'display.max_rows', None, 'display.width', 200)

underlying_stock_symbol = 'TSLA'
underlying = rh.get_quotes(underlying_stock_symbol)
underlying_last = round(float(underlying[0]['last_trade_price']), 2)
option_chains = rh.options.get_chains(underlying_stock_symbol)  # todo all puts?

# my_holdings = rh.build_holdings()
# underlying = rh.get_instruments_by_symbols('tsla')

underlying_history = pd.DataFrame.from_dict(rh.get_stock_historicals(underlying_stock_symbol,
                                                                     interval='day', span='year'))
underlying_standard_deviation = underlying_history['close_price'].astype('float').std()

# print(underlying_history)
print(f'{underlying_stock_symbol} Last: ${underlying_last:.2f} StdDev: {underlying_standard_deviation:.2f}')

leaps = get_leaps(option_chains, 365)

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
        option_data.OTM.between(underlying_standard_deviation, underlying_standard_deviation * 2)]
    print(strike_range[['expiration_date', 'Strike', 'OTM', 'open_interest', 'Bid', 'Ask']])
