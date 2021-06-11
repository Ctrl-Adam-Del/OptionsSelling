

class ScoringDailyScan:

    def __init__(self):

        self.annual_trading_days = 252
        self.annualized_return_days = 365
        self.leaps_min_days = 365
        self.options_bid_ask_midpoint = .25     # .25 = .25 from bid & .75 from ask
