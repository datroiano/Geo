from OptionsOperations.__init__ import *
from OptionsOperations.naming_and_cleaning import *


#  Creates a data type for option contracts (puts, calls, expirations, underlying, etc.)


#  Information about the contract:
#  Underlying Ticker
#  Strike Price - query using options chain data potentially
#  Expiration Date (inputs varying, input: 2023-09-29)
#  Call/Put Type (Maybe make this bool)


class OptionsContract:
    def __int__(self, ticker, strike, expiration_date, contract_type=True):
        self.ticker = str(ticker).upper()
        self.strike = float(strike)
        self.expiration_date = str(expiration_date)
        self.contract_type = bool(contract_type)

    def pull_options_price_data(self, from_date, to_date, window_start_time, window_end_time, timespan,
                                polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz', multiplier='1'):
        exp_day = int(self.expiration_date[8:])  # 2023-09-29
        exp_month = int(self.expiration_date[5:7])
        exp_year = int(self.expiration_date[0:4])
        f_date = f'{from_date} {window_start_time}'
        t_date = f'{to_date} {window_end_time}'

        options_ticker = create_options_ticker(ticker=self.ticker, strike=self.strike, expiration_year=exp_year,
                                               expiration_month=exp_month, expiration_day=exp_day,
                                               contract_type=self.contract_type)

        # Polygon verification
        headers = {
            "Authorization": f"Bearer {polygon_api_key}"
        }

        # Polygon data endpoint
        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/{multiplier}/{timespan}/{f_date}/{t_date}"

        # Getting the options data as requested
        response = requests.get(endpoint, headers=headers).json()

        try:
            if response['queryCount'] == 0:  # Handle options issues where no data was returned
                return None
            else:
                return dict(response)
        except:
            pass
        print(response)


# RUN TO DEBUG

# Test instance (Below)
test_contract = OptionsContract()
test_contract.ticker, test_contract.strike, test_contract.expiration_date = "AAPL", 180, '2023-09-29'
test_contract.contract_type = True
test_contract.pull_options_price_data(from_date='2023-09-22',to_date='2023-09-22',
                                      window_start_time='09:30:00', window_end_time='16:30:00',
                                      timespan='minute', multiplier='1')
