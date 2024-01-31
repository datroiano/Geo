from OptionsOperations.strategies_operations import *


# eventual form inputs for EXCEL creation
ticker = 'GOOG'
trade_date = '2024-01-30'
expirations = '2024-02-02'
strike1 = 145
strike2 = strike1

contract1 = oc.OptionsContract(ticker, strike1, expirations, is_call=True)
contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date=trade_date, to_date=trade_date,
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

contract2 = oc.OptionsContract(ticker, strike2, expirations, is_call=False)
contract2data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date=trade_date, to_date=trade_date,
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

simulation = TwoOptionStrategy(contract1data.pull_options_price_data(), contract2data.pull_options_price_data())
long_straddle_example = simulation.long_strangle_simulation(entry_window_start=f'{trade_date} 09:30:00',
                                                            entry_window_end=f'{trade_date} 11:30:00',
                                                            exit_window_start=f'{trade_date} 14:30:00',
                                                            exit_window_end=f'{trade_date} 16:00:00')

meta_long_straddle_example = MetaAnalysis(simulation_data=long_straddle_example)
average_return = statistics.mean(meta_long_straddle_example.profit_loss_percent_table())
standard_deviation_return = statistics.stdev(meta_long_straddle_example.profit_loss_percent_table())
excel_ready_data = meta_long_straddle_example.create_data_frame()


save_to_excel(excel_ready_data, avg_return=average_return, std_dev=standard_deviation_return)
open_recent_download()
