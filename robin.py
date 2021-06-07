
import robin_stocks as rs
import robin_stocks.robinhood as rh
import pyotp
from datetime import datetime
import os

totp = pyotp.TOTP(os.environ.get('ROBINHOOD_TOTP')).now()
print("Current OTP:", totp)
login = rh.login('kimardenmiller@gmail.com', os.environ.get('ROBINHOOD_PSWD'), mfa_code=totp)

my_stocks = rh.build_holdings()

chain = rh.options.get_chains('TSLA')

for contract in chain['expiration_dates']:
    date_time_obj = datetime.strptime(contract, '%Y-%m-%d')
    days_to_expire = (date_time_obj - datetime.today()).days
    if days_to_expire > 365:
        print(date_time_obj.strftime("%Y-%m-%d"), days_to_expire, 'days out')
