import options_contract_object as oc
from naming_and_cleaning import *


class SingleOptionStrategy:
    def __init__(self, cleaned_data):
        self.cleaned_data = cleaned_data

    def calculate_profit_timed_entry(self, entry_time, exit_time, size=1, pricing=1):
        entry_time = int(to_unix_time(entry_time))
        exit_time = int(to_unix_time(exit_time))
        entry_price = 0
        exit_price = 0

        if pricing == 0:
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == entry_time:
                    entry_price = self.cleaned_data[instant]['low']
                    break
                elif self.cleaned_data[instant]['unix_time'] > entry_time:
                    entry_price = self.cleaned_data[instant]['low']
                    break
                else:
                    continue
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == exit_time:
                    exit_price = self.cleaned_data[instant]['low']
                    break
                elif self.cleaned_data[instant]['unix_time'] > exit_time:
                    exit_price = self.cleaned_data[instant]['low']
                    break
                else:
                    continue
        elif pricing == 1:
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == entry_time:
                    entry_price = round((self.cleaned_data[instant]['low'] + self.cleaned_data[instant]['high']) / 2,
                                        ndigits=2)
                    break
                elif self.cleaned_data[instant]['unix_time'] > entry_time:
                    entry_price = round((self.cleaned_data[instant]['low'] + self.cleaned_data[instant]['high']) / 2,
                                        ndigits=2)
                    break
                else:
                    continue
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == exit_time:
                    exit_price = round((self.cleaned_data[instant]['low'] + self.cleaned_data[instant]['high']) / 2,
                                       ndigits=2)
                    break
                elif self.cleaned_data[instant]['unix_time'] > exit_time:
                    exit_price = round((self.cleaned_data[instant]['low'] + self.cleaned_data[instant]['high']) / 2,
                                       ndigits=2)
                    break
                else:
                    continue
        elif pricing == 2:
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == entry_time:
                    entry_price = self.cleaned_data[instant]['high']
                    break
                elif self.cleaned_data[instant]['unix_time'] > entry_time:
                    entry_price = self.cleaned_data[instant]['high']
                    break
                else:
                    continue
            for instant in self.cleaned_data:
                if self.cleaned_data[instant]['unix_time'] == exit_time:
                    exit_price = self.cleaned_data[instant]['high']
                    break
                elif self.cleaned_data[instant]['unix_time'] > exit_time:
                    exit_price = self.cleaned_data[instant]['high']
                    break
                else:
                    continue

        entry_value = int(size) * entry_price
        exit_value = int(size) * exit_price
        profit_loss_dollars = round(exit_value - entry_value, ndigits=2)
        profit_loss_percent = round(profit_loss_dollars / entry_value, ndigits=2)
        trade_array = {"trade_data": {
            "entry_price": entry_price,
            "entry_time": from_unix_time(entry_time),
            "exit_price": exit_price,
            "exit_time": from_unix_time(exit_time),
            "entry_value": entry_value,
            "exit_value": exit_value,
            "profit_loss_dollars": profit_loss_dollars,
            "profit_loss_percent": profit_loss_percent,
            "size": size,
            "pricing": pricing
        }
        }

        return trade_array


class TwoOptionStrategy:
    def __init__(self, cleaned_data_op_1, cleaned_data_op_2):
        self.op_1_data = cleaned_data_op_1
        self.op_2_data = cleaned_data_op_2

    def long_strangle_simulation(self, entry_window_start, entry_window_end, exit_window_start, exit_window_end,
                                 size=1, pricing=1):
        entry_window_start = int(to_unix_time(entry_window_start))
        entry_window_end = int(to_unix_time(entry_window_end))
        exit_window_start = int(to_unix_time(exit_window_start))
        exit_window_end = int(to_unix_time(exit_window_end))

        # Create a set of unix_time values from op_2_data for faster lookup
        op_2_unix_times = set(value['unix_time'] for value in self.op_2_data.values())

        # Create a new dictionary containing only the elements from op_1_data with unix_time in op_2_unix_times
        self.op_1_data = {key: value for key, value in self.op_1_data.items() if value['unix_time'] in op_2_unix_times}

        entry_data = [value for value in self.op_1_data.values() if
                      entry_window_start <= value['unix_time'] <= entry_window_end]

        exit_data = [value for value in self.op_1_data.values() if
                     exit_window_start <= value['unix_time'] <= exit_window_end]

        # Do nested for loop to run simulation for each entry/end time pair here


contract1 = oc.OptionsContract("AAPL", 170, '2023-09-29', contract_type=True)
contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date='2023-09-28', to_date='2023-09-28',
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

contract2 = oc.OptionsContract("AAPL", 170, '2023-09-29', contract_type=False)
contract2data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date='2023-09-28', to_date='2023-09-28',
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

simulation = TwoOptionStrategy(contract1data.pull_options_price_data(), contract2data.pull_options_price_data())
simulation.long_strangle_simulation(entry_window_start='2023-09-28 09:30:00', entry_window_end='2023-09-28 11:30:00',
                                    exit_window_start='2023-09-28 11:30:00', exit_window_end='2023-09-28 14:30:00')
