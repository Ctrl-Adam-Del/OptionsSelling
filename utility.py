import os
import pyotp
from robin_stocks import robinhood as rh


def authenticate_robinhood():
    totp = pyotp.TOTP(os.environ.get('ROBINHOOD_TOTP')).now()
    # print("Current OTP:", totp)
    login = rh.login('kimardenmiller@gmail.com', os.environ.get('ROBINHOOD_PSWD'), mfa_code=totp)
    return login  # todo make email environment variable
