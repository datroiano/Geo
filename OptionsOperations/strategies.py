import options_contract_object as oc


class SingleOptionStrategy:
    def __init__(self, cleaned_data):
        self.cleaned_data = cleaned_data
        self.prices = {key: data['open'] for key, data in cleaned_data.items()}
        self.volumes = {key: data['volume'] for key, data in cleaned_data.items()}


# Using an OptionsContract instance
test_contract = oc.OptionsContract("AAPL", 180, '2023-09-29')
test_contract_data = oc.OptionsContractsPriceData(options_contract=test_contract,
                                                  from_date='2023-09-28', to_date='2023-09-28',
                                                  window_start_time='09:30:00', window_end_time='16:30:00',
                                                  timespan='minute')

strategy = SingleOptionStrategy(test_contract_data.pull_options_price_data())

