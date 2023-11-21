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

        op_2_unix_times = set(value['unix_time'] for value in self.op_2_data.values())
        self.op_1_data = {key: value for key, value in self.op_1_data.items() if value['unix_time'] in op_2_unix_times}
        op_1_unix_times = set(value['unix_time'] for value in self.op_1_data.values())
        self.op_2_data = {key: value for key, value in self.op_2_data.items() if value['unix_time'] in op_1_unix_times}

        entry_data_1 = [value for value in self.op_1_data.values() if
                        entry_window_start <= value['unix_time'] <= entry_window_end]

        exit_data_1 = [value for value in self.op_1_data.values() if
                       exit_window_start <= value['unix_time'] <= exit_window_end]

        entry_data_2 = [value for value in self.op_2_data.values() if
                        entry_window_start <= value['unix_time'] <= entry_window_end]

        exit_data_2 = [value for value in self.op_2_data.values() if
                       exit_window_start <= value['unix_time'] <= exit_window_end]

        combined_entry_data = [
            {
                'unix_time': item1['unix_time'],
                'time': from_unix_time(item1['unix_time']),  # You need to define this function
                'strategy_value': item1['low'] + item2['low'],
                'strategy_volume': item1['volume'] + item2['volume']
            }
            for item1 in entry_data_1
            for item2 in entry_data_2
            if item1['unix_time'] == item2['unix_time']
        ]

        combined_exit_data = [
            {
                'unix_time': item1['unix_time'],
                'time': from_unix_time(item1['unix_time']),  # You need to define this function
                'strategy_value': item1['low'] + item2['low'],
                'strategy_volume': item1['volume'] + item2['volume']
            }
            for item1 in exit_data_1
            for item2 in exit_data_2
            if item1['unix_time'] == item2['unix_time']
        ]

        simulation_data = []
        for item1 in combined_entry_data:
            entry_time = item1['unix_time']
            for item2 in combined_exit_data:
                exit_time = item2['unix_time']

                if entry_time < exit_time:
                    entry_strategy_value = item1['strategy_value']
                    exit_strategy_value = item2['strategy_value']

                    profit_loss_dollars = (exit_strategy_value - entry_strategy_value) * size
                    profit_loss_percent = ((exit_strategy_value - entry_strategy_value) * size / entry_strategy_value)

                    simulation_data.append({
                        'entry_time': from_unix_time(entry_time),
                        'exit_time': from_unix_time(exit_time),
                        'entry_strategy_value': round(entry_strategy_value * size, ndigits=2),
                        'exit_strategy_value': round(exit_strategy_value * size, ndigits=2),
                        'profit_loss_dollars': round(profit_loss_dollars, ndigits=2),
                        'profit_loss_percent': round(profit_loss_percent, ndigits=2)
                    })

        return simulation_data


class MetaAnalysis:
    def __init__(self, simulation_data):
        self.simulation_data = simulation_data

    def profit_loss_dollars_table(self):
        return [entry['profit_loss_dollars'] for entry in self.simulation_data]

    def profit_loss_percent_table(self):
        return [entry['profit_loss_percent'] for entry in self.simulation_data]


contract1 = oc.OptionsContract("AAPL", 170, '2023-09-29', is_call=True)
contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date='2023-09-28', to_date='2023-09-28',
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

contract2 = oc.OptionsContract("AAPL", 170, '2023-09-29', is_call=False)
contract2data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date='2023-09-28', to_date='2023-09-28',
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

simulation = TwoOptionStrategy(contract1data.pull_options_price_data(), contract2data.pull_options_price_data())
x = simulation.long_strangle_simulation(entry_window_start='2023-09-28 09:30:00',
                                        entry_window_end='2023-09-28 11:30:00',
                                        exit_window_start='2023-09-28 11:30:00', exit_window_end='2023-09-28 14:30:00')


y = MetaAnalysis(x)
z = y.profit_loss_percent_table()


