
import robin_stocks as rs
import robin_stocks.robinhood as rh
import pyotp
from datetime import datetime
import os

totp = pyotp.TOTP(os.environ.get('ROBINHOOD_TOTP')).now()
print("Current OTP:", totp)
login = rh.login('kimardenmiller@gmail.com', os.environ.get('ROBINHOOD_PSWD'), mfa_code=totp)

my_holdings = rh.build_holdings()

chain = rh.options.get_chains('TSLA')

last_contract = []

for contract in chain['expiration_dates']:
    date_time_str = datetime.strptime(contract, '%Y-%m-%d')
    last_contract = date_time_str.strftime("%Y-%m-%d")
    days_to_expire = (date_time_str - datetime.today()).days
    if days_to_expire > 365:
        print(date_time_str.strftime("%Y-%m-%d"), days_to_expire, 'days out')

# optionData = rh.find_options_by_expiration(['fb', 'aapl', 'tsla', 'nflx'],
print(last_contract)
optionData = rh.find_options_by_expiration(['fb'],
                                           expirationDate=last_contract,
                                           optionType='call')
for item in optionData:
    print(' price -', item['strike_price'], ' exp - ', item['expiration_date'], ' symbol - ',
          item['chain_symbol'], ' delta - ', item['delta'], ' theta - ', item['theta'])
