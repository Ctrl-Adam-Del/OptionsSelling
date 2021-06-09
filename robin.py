import robin_stocks.robinhood as rh
from robin_data import get_leaps
from utility import authenticate_robinhood

authenticate_robinhood()

# my_holdings = rh.build_holdings()

chain = rh.options.get_chains('TSLA')
# underlying = rh.get_instruments_by_symbols('tsla')
underlying = rh.get_quotes('tsla')
print('Last Trade: ', underlying[0]['last_trade_price'])
standard_deviation_1 = 'stdev_1'
print('1 StDev', standard_deviation_1)
last_contract = get_leaps(chain)

# optionData = rh.find_options_by_expiration(['fb', 'aapl', 'tsla', 'nflx'],
print(last_contract)
optionData = rh.find_options_by_expiration(['fb'], expirationDate=last_contract, optionType='call')

for item in optionData:
    if float(item['strike_price']) == 300:
        print('300 found')
    # print(' Strike', item['strike_price'], ' exp - ', item['expiration_date'], ' symbol - ',
    #       item['chain_symbol'], ' delta - ', item['delta'], ' theta - ', item['theta'])
