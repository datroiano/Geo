import statistics
import OptionsOperations.options_contract_object as oc
from OptionsOperations.naming_and_cleaning import next_third_friday
from OptionsOperations.log_setup import logger
from OptionsOperations.strategies_operations import TwoOptionStrategy, MetaAnalysis


class MasterSimulation:
    def __init__(self, corrected_strikes, entry_start, entry_end, exit_start, exit_end, pricing=1):
        self.corrected_strikes = corrected_strikes
        self.entry_start = entry_start
        self.entry_end = entry_end
        self.exit_start = exit_start
        self.exit_end = exit_end
        self.pricing = pricing
        self.attempt_size = len(corrected_strikes)

        self.simulation_results, self.error_bound = self.master_simulation_creation()

    def master_simulation_creation(self):
        error_bound = []
        attempted_entries = [tick['symbol'] for tick in self.corrected_strikes]
        logger.info(f'Length of Entries Dictionary: {self.attempt_size}\nAttempted Entries: {attempted_entries}')

        price_mapping = {0: "low", 1: "average", 2: "high"}
        price_text = price_mapping.get(self.pricing, "high")

        master_out = []
        i = 0  # Iteration counter
        j = 0  # Actually used iteration counter (non-error)

        for item in self.corrected_strikes:
            i += 1
            ticker = item['symbol']
            strike1 = item['target_strike']
            strike2 = item['target_strike']
            expirations = item['target_expiration_date']
            trade_date = item['trade_date']

            try:
                contract1 = oc.OptionsContract(ticker, strike1, expirations, is_call=True)
                contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                                             from_date=trade_date, to_date=trade_date,
                                                             window_start_time='09:30:00',
                                                             window_end_time='16:30:00',
                                                             timespan='minute')
            except Exception: # Try a standard expiration date opposed to nearest Friday
                try:
                    contract1 = oc.OptionsContract(ticker, strike1, next_third_friday(expirations), is_call=True)
                    contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                                                 from_date=trade_date, to_date=trade_date,
                                                                 window_start_time='09:30:00',
                                                                 window_end_time='16:30:00',
                                                                 timespan='minute')
                except Exception as e:
                    logger.error(f"Iteration {i} - Option Contract 1 Fail ({ticker}): {e}")
                    error_bound.append([ticker, "Option Contract 1 Data Fail"])
                    continue

            try:
                contract2 = oc.OptionsContract(ticker, strike2, expirations, is_call=False)
                contract2data = oc.OptionsContractsPriceData(options_contract=contract2,
                                                             from_date=trade_date, to_date=trade_date,
                                                             window_start_time='09:30:00',
                                                             window_end_time='16:30:00',
                                                             timespan='minute')
            except Exception:
                try:
                    contract2 = oc.OptionsContract(ticker, strike2, next_third_friday(expirations), is_call=False)
                    contract2data = oc.OptionsContractsPriceData(options_contract=contract2,
                                                                 from_date=trade_date, to_date=trade_date,
                                                                 window_start_time='09:30:00',
                                                                 window_end_time='16:30:00',
                                                                 timespan='minute')
                except Exception as e:
                    logger.error(f"Iteration {i} - Option Contract 2 Fail ({ticker}): {e}")
                    error_bound.append([ticker, "Option Contract 2 Data Fail"])
                    continue

            try:
                simulation = TwoOptionStrategy(contract1data.pull_options_price_data(),
                                               contract2data.pull_options_price_data())
                long_straddle = simulation.long_strangle_simulation(
                    entry_window_start=f'{trade_date} {self.entry_start}',
                    entry_window_end=f'{trade_date} {self.entry_end}',
                    exit_window_start=f'{trade_date} {self.exit_start}',
                    exit_window_end=f'{trade_date} {self.exit_end}',
                    pricing=self.pricing)
            except Exception as e:
                logger.error(f"Iteration {i} - Simulation Error ({ticker}): {e}")
                error_bound.append([ticker, "Simulation Failure"])
                continue

            j += 1

            meta_data = MetaAnalysis(long_straddle)
            if len(long_straddle) == 0:
                logger.error(f'Iteration {i} - Simulation Fail ({ticker})')
                error_bound.append([ticker,"Simulation Failure"])
                continue

            avg_return = statistics.mean(meta_data.profit_loss_percent_table())
            variance = statistics.variance(meta_data.profit_loss_percent_table())
            std_dev = statistics.stdev(meta_data.profit_loss_percent_table())

            new_entry = {'ticker': ticker,
                         'earnings_report_date': item['earnings_report_date'],
                         'trade_date': trade_date,
                         'reporting_period': item['period'],
                         'option_strike_price': strike1,
                         'option_expiration_date': expirations,
                         'options_pricing_model': price_text,
                         'company_fiscal_year': item["fiscal_year"],
                         'company_fiscal_quarter': item['fiscal_quarter'],
                         'revenue_estimated': item['revenue_estimate'],
                         'revenue_actual': item['revenue_actual'],
                         'simulation': {'average_return_percent': round(avg_return, ndigits=4),
                                        'return_variance': round(variance, ndigits=4),
                                        'return_standard_deviation': round(std_dev, ndigits=4),
                                        'trades_simulated': len(long_straddle),
                                        'raw_simulation_data': long_straddle}
                         }

            master_out.append(new_entry)
            logger.info(f'{ticker} (ITERATIONS PASSED)')

        return master_out, error_bound
