from OptionsOperations import options_contract_object as oc
from PDFCreation import raw_pdf as pdf

# Using an OptionsContract instance (TESTS RAW PDF PRINTING)
# test_contract = oc.OptionsContract("AAPL", 180, '2023-09-29')
# test_contract_data = oc.OptionsContractsPriceData(options_contract=test_contract,
#                                                   from_date='2023-09-28', to_date='2023-09-28',
#                                                   window_start_time='09:30:00', window_end_time='16:30:00',
#                                                   timespan='minute')
#
#
# pdf.raw_data_pdf(cleaned_response=test_contract_data.pull_options_price_data())
