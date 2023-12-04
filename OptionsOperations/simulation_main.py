from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download

# USER DOCUMENTATION AVAILABLE IN ALTERNATE FILE
# USER INTERFACE - FUTURE PORTION OF PROJECT

# ------------------------------------------------------------------------------------------------------------------- #
#                                   Company Screening Inputs (Multi-Company Report)                                   #
MinimumRevenueEstimate = 5_500_000_000
PeriodDateStart = '2023-11-19'  # Must remain without 1 month previous, until $75 per month subscription is paid
PeriodDateEnd = '2023-12-03'
ReportHourType = 'amc'  # Has proper functionality
MaxCompaniesReported = 4  # Must remain at 5 until Polygon stock API is paid for $25. Can be expended to the hundreds+
TickerPairingSize = 45  # Determines how many options are searched via option chain lookup
OptionsPricingConstant = 1  # 0 is low, 1 is average high/low, 2 is high. Default = 1

EnterTradingPeriodStart = '09:45:00'
EnterTradingPeriodEnd = '11:00:00'
ExitTradingPeriodStart = '15:45:00'
ExitTradingPeriodEnd = '15:59:00'

SkipCompanyList = []  # Has proper functionality, leave as empty list to attempt all possible matching companies
ReportLineHeight = 5
OpenReport = 'YES'
# ------------------------------------------------------------------------------------------------------------------- #

# COMBINED LOGIC
user_input_simulation = TestCompanies(min_revenue=MinimumRevenueEstimate, from_date=PeriodDateStart, to_date=PeriodDateEnd,
                                      report_hour=ReportHourType, max_companies=MaxCompaniesReported,
                                      data_limit=TickerPairingSize, skipped_tickers=SkipCompanyList)


viewable = master_callable_inputs_outputs(corrected_strikes=user_input_simulation.correct_strikes,
                                          entry_start=EnterTradingPeriodStart, entry_end=EnterTradingPeriodEnd,
                                          exit_start=ExitTradingPeriodStart, exit_end=ExitTradingPeriodEnd,
                                          pricing=OptionsPricingConstant)

write_dict_to_pdf(viewable, line_height=ReportLineHeight)

if OpenReport.upper() == "YES":
    open_recent_download()
