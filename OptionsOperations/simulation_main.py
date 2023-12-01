from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download

# USER DOCUMENTATION AVAILABLE IN ALTERNATE FILE
# USER INTERFACE - FUTURE PORTION OF PROJECT

# ------------------------------------------------------------------------------------------------------------------- #
#                                   Company Screening Inputs (Multi-Company Report)                                   #
MinimumRevenue = 100000000
PeriodDateStart = '2023-11-01'  # Must remain without 1 month previous, until $75 per month subscription is paid
PeriodDateEnd = '2023-11-30'
ReportHourType = 'amc'
MaxCompaniesReported = 2  # Must remain at 5 until Polygon stock API is paid for $25. Can be expended to the hundreds+

EnterTradingPeriodStart = '09:30:00'
EnterTradingPeriodEnd = '11:30:00'
ExitTradingPeriodStart = '15:30:00'
ExitTradingPeriodEnd = '15:59:00'
# ------------------------------------------------------------------------------------------------------------------- #

# COMBINED LOGIC
user_input_simulation = TestCompanies(min_revenue=MinimumRevenue, from_date=PeriodDateStart, to_date=PeriodDateEnd,
                                      report_hour=ReportHourType, max_companies=MaxCompaniesReported)


viewable = master_callable_inputs_outputs(corrected_strikes=user_input_simulation.correct_strikes,
                                          entry_start=EnterTradingPeriodStart, entry_end=EnterTradingPeriodEnd,
                                          exit_start=ExitTradingPeriodStart, exit_end=ExitTradingPeriodEnd)

pdf = write_dict_to_pdf(viewable)
open_recent_download()
