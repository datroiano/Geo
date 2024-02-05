from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download
from OptionsOperations.temp_entries import tickers
from OptionsOperations.__init__ import time
from log_setup import logger
from OptionsOperations.strategies_operations import get_bulk_iterations
from OptionsOperations.naming_and_cleaning import day_before

# USER DOCUMENTATION AVAILABLE IN ALTERNATE FILE
# USER INTERFACE - FUTURE PORTION OF PROJECT

# ------------------------------------------------------------------------------------------------------------------- #
#                                   Company Screening Inputs (Multi-Company Report)                                   #
MinimumRevenueEstimate = 25_000_000_000
PeriodDateStart = ''  # Must remain without 1 month previous, until $75 per month subscription is paid (default)
PeriodDateEnd = ''  # Has to be one less than today's date (blank defaults to this)
ReportHourType = ''  # Has proper functionality - either bmo, amc, or *blank*
MaxCompaniesReported = 5  # Must remain at 5 until Polygon stock API is paid for $25. Can be expended to the hundreds+
TickerPairingSize = 55  # Determines how many options are searched via option chain lookup (to find entry strike)
OptionsPricingConstant = 1  # 0 is low, 1 is average high/low, 2 is high. Default = 1

EnterTradingPeriodStart = '09:30:00'
EnterTradingPeriodEnd = '11:00:00'
ExitTradingPeriodStart = '14:30:00'
ExitTradingPeriodEnd = '15:59:00'

CustomSkipCompanyList = ['CVX', 'CI', 'AAPL']
ReportLineHeight = 5
OpenReport = 'YES'
SkipCompaniesStoredInCache = 'NO'
ClearCacheUponRunning = 'YES'
# ------------------------------------------------------------------------------------------------------------------- #

# COMBINED LOGIC
start_time = time.perf_counter()

PeriodDateStart = get_date_31_days_ago() if PeriodDateStart == "" else PeriodDateStart
PeriodDateEnd = day_before(get_today_date()) if PeriodDateEnd == "" else PeriodDateEnd
CustomSkipCompanyList = tickers if SkipCompaniesStoredInCache.upper() == "YES" else CustomSkipCompanyList

user_input_simulation = TestCompanies(min_revenue=MinimumRevenueEstimate, from_date=PeriodDateStart,
                                      to_date=PeriodDateEnd, report_hour=ReportHourType,
                                      max_companies=MaxCompaniesReported, data_limit=TickerPairingSize,
                                      skipped_tickers=CustomSkipCompanyList)


viewable = master_callable_inputs_outputs(corrected_strikes=user_input_simulation.correct_strikes,
                                          entry_start=EnterTradingPeriodStart, entry_end=EnterTradingPeriodEnd,
                                          exit_start=ExitTradingPeriodStart, exit_end=ExitTradingPeriodEnd,
                                          pricing=OptionsPricingConstant, clear_at_end=ClearCacheUponRunning.upper())

write_dict_to_pdf(viewable, line_height=ReportLineHeight)

if OpenReport.upper() == "YES":
    open_recent_download()
logger.info(f'Bulk Calc Dictionaries: {get_bulk_iterations(viewable)}')
end_time = time.perf_counter()
execution_time = end_time - start_time
logger.info(f"Execution time: {execution_time:.2f} seconds")


