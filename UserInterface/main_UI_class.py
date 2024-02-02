import tkinter as tk
from tkinter import ttk
from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download
from OptionsOperations.temp_entries import tickers
from OptionsOperations.__init__ import time
from OptionsOperations.strategies_operations import get_bulk_iterations
from OptionsOperations.naming_and_cleaning import day_before
import logging
from tkinter.scrolledtext import ScrolledText


class MyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Options Operations GUI")

        # Create and place GUI components
        ttk.Label(root, text="Minimum Revenue Estimate:").grid(row=0, column=0)
        self.min_revenue_entry = ttk.Entry(root)
        self.min_revenue_entry.grid(row=0, column=1)
        self.min_revenue_entry.insert(0, str(10_000_000_000))

        ttk.Label(root, text="Period Date Start:").grid(row=1, column=0)
        self.period_date_start_entry = ttk.Entry(root)
        self.period_date_start_entry.grid(row=1, column=1)

        ttk.Label(root, text="Period Date End:").grid(row=2, column=0)
        self.period_date_end_entry = ttk.Entry(root)
        self.period_date_end_entry.grid(row=2, column=1)

        ttk.Label(root, text="Report Hour Type:").grid(row=3, column=0)
        self.report_hour_type_entry = ttk.Entry(root)
        self.report_hour_type_entry.grid(row=3, column=1)
        self.report_hour_type_entry.insert(0, "amc")

        ttk.Label(root, text="Max Companies Reported:").grid(row=4, column=0)
        self.max_companies_reported_entry = ttk.Entry(root)
        self.max_companies_reported_entry.grid(row=4, column=1)
        self.max_companies_reported_entry.insert(0, str(5))

        ttk.Label(root, text="Ticker Pairing Size:").grid(row=5, column=0)
        self.ticker_pairing_size_entry = ttk.Entry(root)
        self.ticker_pairing_size_entry.grid(row=5, column=1)
        self.ticker_pairing_size_entry.insert(0, "55")

        ttk.Label(root, text="Options Pricing Constant:").grid(row=6, column=0)
        self.options_pricing_constant_entry = ttk.Entry(root)
        self.options_pricing_constant_entry.grid(row=6, column=1)
        self.options_pricing_constant_entry.insert(0, "1")

        ttk.Label(root, text="Enter Trading Period Start:").grid(row=7, column=0)
        self.enter_trading_period_start_entry = ttk.Entry(root)
        self.enter_trading_period_start_entry.grid(row=7, column=1)
        self.enter_trading_period_start_entry.insert(0, "09:30:00")

        ttk.Label(root, text="Enter Trading Period End:").grid(row=8, column=0)
        self.enter_trading_period_end_entry = ttk.Entry(root)
        self.enter_trading_period_end_entry.grid(row=8, column=1)
        self.enter_trading_period_end_entry.insert(0, "11:00:00")

        ttk.Label(root, text="Exit Trading Period Start:").grid(row=9, column=0)
        self.exit_trading_period_start_entry = ttk.Entry(root)
        self.exit_trading_period_start_entry.grid(row=9, column=1)
        self.exit_trading_period_start_entry.insert(0, "14:00:00")

        ttk.Label(root, text="Exit Trading Period End:").grid(row=10, column=0)
        self.exit_trading_period_end_entry = ttk.Entry(root)
        self.exit_trading_period_end_entry.grid(row=10, column=1)
        self.exit_trading_period_end_entry.insert(0, "15:59:00")

        ttk.Label(root, text="Custom Skip Company List:").grid(row=11, column=0)
        self.custom_skip_company_list_entry = ttk.Entry(root)
        self.custom_skip_company_list_entry.grid(row=11, column=1)

        ttk.Label(root, text="Report Line Height:").grid(row=12, column=0)
        self.report_line_height_entry = ttk.Entry(root)
        self.report_line_height_entry.grid(row=12, column=1)
        self.report_line_height_entry.insert(0, "5")

        ttk.Label(root, text="Open Report:").grid(row=13, column=0)
        self.open_report_entry = ttk.Entry(root)
        self.open_report_entry.grid(row=13, column=1)
        self.open_report_entry.insert(0, "YES")

        ttk.Label(root, text="Skip Companies Stored in Cache:").grid(row=14, column=0)
        self.skip_companies_stored_in_cache_entry = ttk.Entry(root)
        self.skip_companies_stored_in_cache_entry.grid(row=14, column=1)
        self.skip_companies_stored_in_cache_entry.insert(0, "NO")

        ttk.Label(root, text="Clear Cache Upon Running:").grid(row=15, column=0)
        self.clear_cache_upon_running_entry = ttk.Entry(root)
        self.clear_cache_upon_running_entry.grid(row=15, column=1)
        self.clear_cache_upon_running_entry.insert(0, "YES")

        self.text_widget = ScrolledText(root, wrap=tk.WORD)
        self.text_widget.grid(row=0, column=2, rowspan=16)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger()
        logger.addHandler(TkinterTextHandler(self.text_widget))

        ttk.Button(root, text="Run Logic", command=self.run_operations).grid(row=16, column=0, columnspan=3,
                                                                             sticky="NSEW")

    def run_operations(self):
        # Get values from GUI components
        min_revenue = int(self.min_revenue_entry.get())
        period_date_start = self.period_date_start_entry.get()
        period_date_end = self.period_date_end_entry.get()
        report_hour_type = self.report_hour_type_entry.get()
        max_companies_reported = int(self.max_companies_reported_entry.get())
        ticker_pairing_size = int(self.ticker_pairing_size_entry.get())
        options_pricing_constant = int(self.options_pricing_constant_entry.get())
        enter_trading_period_start = self.enter_trading_period_start_entry.get()
        enter_trading_period_end = self.enter_trading_period_end_entry.get()
        exit_trading_period_start = self.exit_trading_period_start_entry.get()
        exit_trading_period_end = self.exit_trading_period_end_entry.get()
        custom_skip_company_list = self.custom_skip_company_list_entry.get()
        report_line_height = int(self.report_line_height_entry.get())
        open_report = self.open_report_entry.get()
        skip_companies_stored_in_cache = self.skip_companies_stored_in_cache_entry.get()
        clear_cache_upon_running = self.clear_cache_upon_running_entry.get()

        # COMBINED LOGIC
        start_time = time.perf_counter()

        PeriodDateStart = get_date_31_days_ago() if period_date_start == "" else period_date_start
        PeriodDateEnd = day_before(get_today_date()) if period_date_end == "" else period_date_end
        CustomSkipCompanyList = tickers if skip_companies_stored_in_cache.upper() == "YES" else custom_skip_company_list

        user_input_simulation = TestCompanies(min_revenue=min_revenue, from_date=PeriodDateStart,
                                              to_date=PeriodDateEnd, report_hour=report_hour_type,
                                              max_companies=max_companies_reported, data_limit=ticker_pairing_size,
                                              skipped_tickers=CustomSkipCompanyList)

        viewable = master_callable_inputs_outputs(corrected_strikes=user_input_simulation.correct_strikes,
                                                  entry_start=enter_trading_period_start,
                                                  entry_end=enter_trading_period_end,
                                                  exit_start=exit_trading_period_start,
                                                  exit_end=exit_trading_period_end,
                                                  pricing=options_pricing_constant,
                                                  clear_at_end=clear_cache_upon_running.upper())

        write_dict_to_pdf(viewable, line_height=report_line_height)

        if open_report.upper() == "YES":
            open_recent_download()
        logger.info(f'Bulk Calc Dictionaries: {get_bulk_iterations(viewable)}')
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger.info(f"Execution time: {execution_time:.2f} seconds")


class TkinterTextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)



# Create the main window
root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()
