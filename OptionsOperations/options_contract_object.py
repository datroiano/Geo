from OptionsOperations.naming_and_cleaning import *


#  Creates a data type for option contracts (puts, calls, expirations, underlying, etc.)


#  Information about the contract:
#  Underlying Ticker
#  Strike Price - query using options chain data potentially
#  Expiration Date (inputs varying, input: 2023-09-29)
#  Call/Put Type (Maybe make this bool)


class OptionsContract:
    def __init__(self, ticker, strike, expiration_date, is_call=True):
        self.ticker = str(ticker).upper()
        self.strike = float(strike)
        self.expiration_date = str(expiration_date)
        self.is_call = is_call


class OptionsContractsPriceData(OptionsContract):
    def __init__(self, options_contract=None, from_date=None, to_date=None, window_start_time=None,
                 window_end_time=None, timespan=None, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz', multiplier=1):
        super().__init__(options_contract.ticker, options_contract.strike, options_contract.expiration_date,
                         options_contract.is_call)

        self.polygon_api_key = polygon_api_key
        self.from_date = from_date
        self.to_date = to_date
        self.window_start_time = window_start_time
        self.window_end_time = window_end_time
        self.timespan = timespan
        self.multiplier = multiplier
        self.exp_day = int(self.expiration_date[8:])  # 2023-09-29
        self.exp_month = int(self.expiration_date[5:7])
        self.exp_year = int(self.expiration_date[2:4])

    def _make_api_request(self):
        from_date = to_unix_time(f'{self.from_date} {self.window_start_time}')
        to_date = to_unix_time(f'{self.to_date} {self.window_end_time}')

        options_ticker = create_options_ticker(ticker=self.ticker, strike=self.strike, expiration_year=self.exp_year,
                                               expiration_month=self.exp_month, expiration_day=self.exp_day,
                                               contract_type=self.is_call)

        headers = {"Authorization": f"Bearer {self.polygon_api_key}"}

        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{options_ticker}/range/{self.multiplier}/{self.timespan}/{from_date}/{to_date}"

        response = requests.get(endpoint, headers=headers).json()

        return response

    def pull_options_price_data(self):
        response = self._make_api_request()

        if response.get('queryCount', 0) == 0 or response.get('status') == 'ERROR':
            return None

        cleaned_response = {
            from_unix_time(timestamp['t']): {
                'volume': timestamp['v'],
                'volume_weighted': timestamp['vw'],
                'open': timestamp['o'],
                'unix_time': timestamp['t'],
                'close': timestamp['c'],
                'high': timestamp['h'],
                'low': timestamp['l'],
                'number': timestamp['n']
            }
            for timestamp in response.get('results', [])
        }

        return cleaned_response

    def get_query_count_for_timeperiod(self):
        response = self._make_api_request()

        if response.get('queryCount', 0) == 0 or response.get('status') == 'ERROR':
            return None

        return response.get('queryCount')

    def get_raw_data(self):
        response = self._make_api_request()

        if response.get('queryCount', 0) == 0 or response.get('status') == 'ERROR':
            return None

        return response


# Using an OptionsContract instance
# test_contract = OptionsContract("AAPL", 180, '2023-09-29')
# test_contract_data = OptionsContractsPriceData(options_contract=test_contract,
#                                                from_date='2023-09-28', to_date='2023-09-28',
#                                                window_start_time='09:30:00', window_end_time='16:30:00',
#                                                timespan='minute')
# printable = test_contract_data.pull_options_price_data()
# print(printable)
