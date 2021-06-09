from datetime import datetime


def get_leaps(chain):
    contract_date = []
    for contract in chain['expiration_dates']:
        date_time_str = datetime.strptime(contract, '%Y-%m-%d')
        contract_date = date_time_str.strftime("%Y-%m-%d")
        days_to_expire = (date_time_str - datetime.today()).days
        if days_to_expire > 365:
            print(contract_date, days_to_expire, 'days out')
    return contract_date
