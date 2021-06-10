from datetime import datetime


def get_leaps(chain, min_to_expire):
    contracts = []
    for contract in chain['expiration_dates']:
        date_time_str = datetime.strptime(contract, '%Y-%m-%d')
        days_to_expire = (date_time_str - datetime.today()).days
        if days_to_expire > min_to_expire:
            contracts.append({'contract': date_time_str.strftime("%Y-%m-%d"), 'days_to_expire': days_to_expire})
            print(date_time_str.strftime("%Y-%m-%d"), days_to_expire, 'days out')
    return contracts
