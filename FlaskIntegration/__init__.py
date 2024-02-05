# FlaskIntegration/app.py
from flask import Flask, render_template, request
from OptionsOperations.earnings_calendar_pulls import *
from OptionsOperations.strategies_operations import master_callable_inputs_outputs
from PDFCreation.raw_pdf import write_dict_to_pdf
from OptionsOperations.excel_functions import open_recent_download
from OptionsOperations.temp_entries import tickers
from OptionsOperations.__init__ import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_operations', methods=['POST'])
def run_operations():
    if request.method == 'POST':
        # Get values from the form
        min_revenue_str = request.form['min_revenue'].replace(',', '')
        min_revenue = int(min_revenue_str)

        period_date_start = request.form['period_date_start']
        period_date_end = request.form['period_date_end']
        report_hour_type = request.form['report_hour_type']
        max_companies_reported = int(request.form['max_companies_reported'])
        ticker_pairing_size = int(request.form['ticker_pairing_size'])
        options_pricing_constant = int(request.form['options_pricing_constant'])
        enter_trading_period_start = request.form['enter_trading_period_start']
        enter_trading_period_end = request.form['enter_trading_period_end']
        exit_trading_period_start = request.form['exit_trading_period_start']
        exit_trading_period_end = request.form['exit_trading_period_end']
        custom_skip_company_list = request.form['custom_skip_company_list']
        custom_skip_company_list = [ticker.strip().upper() for ticker in custom_skip_company_list.split(',')]
        report_line_height = 5
        open_report = request.form['open_report']
        skip_companies_stored_in_cache = "NO"
        clear_cache_upon_running = "YES"

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

        global financial_data
        financial_data = viewable

        if open_report.upper() == "YES":
            open_recent_download()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger.info(f"Execution time: {execution_time:.2f} seconds")

        return render_template('result.html', result='Operation completed successfully',
                               execution_time=execution_time)


@app.route('/financial_dashboard')
def financial_dashboard():
    global financial_data
    if request.method == 'GET':
        if financial_data is not None:
            return render_template('financial_dashboard.html', data=financial_data)
        else:
            return render_template('financial_dashboard.html', data=None)
    else:
        # Handle other methods if needed
        return render_template('error.html', error_message='Method Not Allowed')


if __name__ == '__main__':
    app.run(debug=False)
