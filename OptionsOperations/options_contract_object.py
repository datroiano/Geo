from OptionsOperations.__init__ import *
from OptionsOperations.naming_and_cleaning import *


#  Creates a data type for option contracts (puts, calls, expirations, underlying, etc.)


#  Information about the contract:
#  Underlying Ticker
#  Strike Price - query using options chain data potentially
#  Expiration Date (inputs varying, input: 2023-09-29)
#  Call/Put Type (Maybe make this bool)


class OptionsContract:
    def __init__(self, ticker, strike, expiration_date, contract_type=True):
        self.ticker = str(ticker).upper()
        self.strike = float(strike)
        self.expiration_date = str(expiration_date)
        self.contract_type = contract_type

    def pull_options_price_data(self, from_date, to_date, window_start_time, window_end_time, timespan,
                                polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz', multiplier=1):
        exp_day = int(self.expiration_date[8:])  # 2023-09-29
        exp_month = int(self.expiration_date[5:7])
        exp_year = int(self.expiration_date[2:4])
        from_date = to_unix_time(f'{from_date} {window_start_time}')
        to_date = to_unix_time(f'{to_date} {window_end_time}')

        options_ticker = create_options_ticker(ticker=self.ticker, strike=self.strike, expiration_year=exp_year,
                                               expiration_month=exp_month, expiration_day=exp_day,
                                               contract_type=self.contract_type)

        # Polygon verification
        headers = {
            "Authorization": f"Bearer {polygon_api_key}"
        }

        # Polygon data endpoint
        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{options_ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

        # Getting the options data as requested
        response = requests.get(endpoint, headers=headers).json()

        if response['queryCount'] == 0 or response['status'] == 'ERROR':  # Return None value
            return None

        # Make a readable python dictionary based on this
        price_data = response['results']

        cleaned_response = dict()
        for timestamp in price_data:
            quote_time = timestamp['t']
            cleaned_response[quote_time] = {
                'volume': timestamp['v'],
                'volume_weighted': timestamp['vw'],
                'open': timestamp['o'],
                'close': timestamp['c'],
                'high': timestamp['h'],
                'low': timestamp['l'],
                'number': timestamp['n']
            }

        return cleaned_response





# Test instance (Below)
# test_contract = OptionsContract("AAPL", 180, '2023-09-29')
# result = test_contract.pull_options_price_data(from_date='2023-09-22', to_date='2023-09-22',
#                                                window_start_time='09:30:00', window_end_time='16:30:00',
#                                                timespan='minute')



