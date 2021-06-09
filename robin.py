import robin_stocks.robinhood as rh
import pandas as pd
from robin_data import get_leaps
from utility import authenticate_robinhood

authenticate_robinhood()

# my_holdings = rh.build_holdings()

underlying_stock_symbol = 'tsla'
chain = rh.options.get_chains(underlying_stock_symbol)
# underlying = rh.get_instruments_by_symbols('tsla')
underlying = rh.get_quotes('tsla')
underlying_last = round(float(underlying[0]['last_trade_price']), 2)
print('Last Trade: ', underlying_last)

underlying_history = pd.DataFrame.from_dict(rh.get_stock_historicals(underlying_stock_symbol,
                                                                     interval='day', span='year'))
underlying_standard_deviation = underlying_history['close_price'].astype('float').std()

pd.set_option('display.max_columns', None, 'display.width', 200)
# print(underlying_history)
print('underlying_standard_deviation: ', round(underlying_standard_deviation, 2))

last_contract = get_leaps(chain)
# print(last_contract)

optionData = pd.DataFrame.from_dict(rh.find_options_by_expiration(underlying_stock_symbol,
                                                                  expirationDate=last_contract, optionType='put'))
optionData['Strike'] = round(optionData.strike_price.astype('float')).astype('int32')
optionData['Bid'] = round(optionData['bid_price'].astype('float'), 2)
optionData['Ask'] = round(optionData['ask_price'].astype('float'), 2)
optionData.sort_values('Strike', inplace=True)
# print(optionData.head())

optionData['OTM'] = underlying_last - optionData['Strike']

strike_range = optionData[optionData.OTM.between(underlying_standard_deviation, underlying_standard_deviation * 2)]
print(strike_range[['Strike', 'OTM', 'Bid', 'Ask']])
