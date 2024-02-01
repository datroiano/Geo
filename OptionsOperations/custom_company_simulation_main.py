from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download
from OptionsOperations.temp_entries import tickers
from OptionsOperations.__init__ import time
from log_setup import logger
from OptionsOperations.strategies_operations import get_bulk_iterations
from OptionsOperations.naming_and_cleaning import day_before


# ------------------------------------------------------------------------------------------------------------------- #
#                                   Settings and Company Input Selection                                              #
TestTheseCompanies = 'GOOGL'
PeriodDateStart = ''  # Must remain without 1 month previous, until $75 per month subscription is paid (default)
PeriodDateEnd = ''  # Has to be one less than today's date (blank defaults to this)
TickerPairingSize = 55  # Determines how many options are searched via option chain lookup (to find entry strike)
OptionsPricingConstant = 1  # 0 is low, 1 is average high/low, 2 is high. Default = 1

EnterTradingPeriodStart = '09:30:00'
EnterTradingPeriodEnd = '11:00:00'
ExitTradingPeriodStart = '14:30:00'
ExitTradingPeriodEnd = '15:59:00'

CustomSkipCompanyList = []
ReportLineHeight = 5
OpenReport = 'YES'
SkipCompaniesStoredInCache = 'NO'
ClearCacheUponRunning = 'YES'
# ------------------------------------------------------------------------------------------------------------------- #

PeriodDateStart = get_date_31_days_ago() if PeriodDateStart == "" else PeriodDateStart
PeriodDateEnd = day_before(get_today_date()) if PeriodDateEnd == "" else PeriodDateEnd

user_input_simulation = TestCompanies(min_revenue=0, from_date=PeriodDateStart,
                                      to_date=PeriodDateEnd, report_hour="",
                                      max_companies=5, data_limit=TickerPairingSize,
                                      skipped_tickers=CustomSkipCompanyList, underlying_ticker=TestTheseCompanies)

viewable = master_callable_inputs_outputs(corrected_strikes=user_input_simulation.correct_strikes,
                                          entry_start=EnterTradingPeriodStart, entry_end=EnterTradingPeriodEnd,
                                          exit_start=ExitTradingPeriodStart, exit_end=ExitTradingPeriodEnd,
                                          pricing=OptionsPricingConstant, clear_at_end=ClearCacheUponRunning.upper())

write_dict_to_pdf(viewable, line_height=ReportLineHeight)

if OpenReport.upper() == "YES":
    open_recent_download()
