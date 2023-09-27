#  Creates a data type for option contracts (puts, calls, expirations, underlyings, etc)

#  Information about the contract:
    #  Underlying Ticker
    #  Strike Price - query using options chain data potentially
    #  Expiration Date (inputs varying, input: 2023-09-29)
    #  Call/Put Type (Maybe make this bool)






class OptionsContract:
    def __int__(self, ticker, strike, expiration_date, call):
        self.ticker = str(ticker).upper()
        self.strike = float(strike)
        self.expiration_date = str(expiration_date)
        self.call = bool(call)

    def pull_options_price_data(self, from_date, to_date, window_start_time, window_end_time, timespan, multiplier='1'):
