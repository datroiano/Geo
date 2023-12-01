import math
import statistics

import options_contract_object as oc
from naming_and_cleaning import *
from OptionsOperations.__init__ import *


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
                        'profit_loss_percent': round(profit_loss_percent, ndigits=4)
                    })

        return simulation_data


class MetaAnalysis:
    def __init__(self, simulation_data):
        self.simulation_data = simulation_data

    def profit_loss_dollars_table(self):
        return [entry['profit_loss_dollars'] for entry in self.simulation_data]

    def profit_loss_percent_table(self):
        return [entry['profit_loss_percent'] for entry in self.simulation_data]

    def create_data_frame(self):
        nested_dict = {}
        for item in self.simulation_data:
            for key, value in item.items():
                if key not in nested_dict:
                    nested_dict[key] = [value]
                else:
                    nested_dict[key].append(value)
        simulation_df = pd.DataFrame(nested_dict)

        return simulation_df


def master_callable_inputs_outputs(corrected_strikes, entry_start, entry_end, exit_start, exit_end):
    master_out = []
    i = 0
    for item in corrected_strikes:
        if len(item) == 0:
            continue
        else:
            ticker = item['symbol']
            strike1 = item['target_strike']
            strike2 = item['target_strike']
            expirations = item['target_expiration_date']
            trade_date = item['date']
            try:
                contract1 = oc.OptionsContract(ticker, strike1, expirations, is_call=True)
                contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                                             from_date=trade_date, to_date=trade_date,
                                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                                             timespan='minute')
            except:
                continue

            try:
                contract2 = oc.OptionsContract(ticker, strike2, expirations, is_call=False)
                contract2data = oc.OptionsContractsPriceData(options_contract=contract2,
                                                             from_date=trade_date, to_date=trade_date,
                                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                                             timespan='minute')
            except:
                continue

            try:
                simulation = TwoOptionStrategy(contract1data.pull_options_price_data(), contract2data.pull_options_price_data())
                long_straddle = simulation.long_strangle_simulation(entry_window_start=f'{trade_date} {entry_start}',
                                                                    entry_window_end=f'{trade_date} {entry_end}',
                                                                    exit_window_start=f'{trade_date} {exit_start}',
                                                                    exit_window_end=f'{trade_date} {exit_end}')
            except:
                continue

            new_entry = {'ticker': ticker,
                         'strike_price': strike1,
                         'expiration_date': expirations,
                         'trade_date': trade_date,
                         f'sim{i+1}': long_straddle}

            master_out.append(new_entry)

            i += 1

    return master_out


# test_corrected_strikes = [{'symbol': 'CRM', 'target_strike': 230, 'date': '2023-11-29', 'target_expiration_date': '2023-12-01'}, {'symbol': 'HPQ', 'target_strike': 28, 'date': '2023-11-21', 'target_expiration_date': '2023-11-24'}]
#
# master_callable_inputs_outputs(test_corrected_strikes, entry_start='09:30:00', entry_end='11:00:00',
#                                exit_start="14:00:00", exit_end="15:59:00")
