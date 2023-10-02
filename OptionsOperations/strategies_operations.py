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




test_contract = oc.OptionsContract("AAPL", 170, '2023-09-29')
test_contract_data = oc.OptionsContractsPriceData(options_contract=test_contract,
                                                  from_date='2023-09-28', to_date='2023-09-28',
                                                  window_start_time='09:30:00', window_end_time='16:30:00',
                                                  timespan='minute')

strategy = SingleOptionStrategy(test_contract_data.pull_options_price_data())
trade_example = strategy.calculate_profit_timed_entry('2023-09-28 09:30:00', '2023-09-28 13:00:00')

