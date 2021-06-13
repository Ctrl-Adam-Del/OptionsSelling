import pandas as pd


class ScoringDailyScan:

    def __init__(self):

        self.annual_trading_days = 252
        self.annualized_return_days = 365
        self.leaps_min_days = 365
        self.options_bid_ask_midpoint = .25     # .25 = .25 away from bid & .75 away from ask

        self.underlying_stock_symbol_testing = {'Ticker Symbol': ['GE']}
        # self.underlying_stock_symbol_testing = {'Ticker Symbol': ['TSLA', 'GE']}
        self.underlying_stock_symbol_import = 'zdata/VG_Horse_3.0_BCC_Hold253days_30picks_20000324_today.xBA7xdOU.csv'

        self.pd = pd
