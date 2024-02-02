from jinja2 import Template
import os

# Provided nested dictionary
data = {
    "ticker": "AAPL",
    "earnings_report_date": "2024-02-01",
    "trade_date": "2024-02-01",
    "reporting_period": "amc",
    "option_strike_price": 185,
    "option_expiration_date": "2024-02-02",
    "options_pricing_model": "average",
    "company_fiscal_year": 2024,
    "company_fiscal_quarter": 1,
    "revenue_estimated": 120302741943,
    "revenue_actual": 119575000000,
    "sim_company_2": {
        "average_return_percent": -0.0153,
        "return_variance": 0.0001,
        "return_standard_deviation": 0.0082,
        "raw_simulation_data": [
            {
                "entry_time": "2024-02-01 09:30:00",
                "exit_time": "2024-02-01 14:00:00",
                "entry_strategy_value": 6.91,
                "entry_trading_volume": 843,
                "exit_strategy_value": 6.95,
                "exit_trading_volume": 18,
                "profit_loss_dollars": 0.04,
                "profit_loss_percent": 0.0058,
            }
            # Additional trades can be added here
        ],
    },
}


def generate_html_reports(data):

    # Function to delete HTML files in the current directory
    def delete_html_files():
        for filename in os.listdir():
            if filename.endswith(".html"):
                os.remove(filename)

    # Delete existing HTML files before generating new ones
    delete_html_files()

    # HTML template for the main report
    main_report_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ ticker }} Earnings Report</title>
    </head>
    <body>
        <h1>{{ ticker }} Earnings Report</h1>

        <h2>Key Statistics</h2>
        <ul>
            <li><strong>Earnings Report Date:</strong> {{ earnings_report_date }}</li>
            <li><strong>Trade Date:</strong> {{ trade_date }}</li>
            <li><strong>Reporting Period:</strong> {{ reporting_period }}</li>
            <li><strong>Option Strike Price:</strong> ${{ option_strike_price }}</li>
            <li><strong>Option Expiration Date:</strong> {{ option_expiration_date }}</li>
            <li><strong>Options Pricing Model:</strong> {{ options_pricing_model }}</li>
            <li><strong>Revenue Actual:</strong> ${{ revenue_actual }}</li>
            <li><strong>Average Return Percent:</strong> {{ sim_company_2.average_return_percent }}</li>
            <li><strong>Return Variance:</strong> {{ sim_company_2.return_variance }}</li>
            <li><strong>Return Standard Deviation:</strong> {{ sim_company_2.return_standard_deviation }}</li>
        </ul>

        <h2>All Trades</h2>
        <ul>
            {% for trade in sim_company_2.raw_simulation_data %}
                <li>{{ trade.entry_time }} - Profit/Loss: ${{ trade.profit_loss_dollars }} ({{ trade.profit_loss_percent }})</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

    # HTML template for individual trades
    trade_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ ticker }} Trades</title>
    </head>
    <body>
        <h1>{{ ticker }} Trades</h1>

        <h2>All Trades</h2>
        <ul>
            {% for trade in raw_simulation_data %}
                <li>
                    <strong>Trade Time:</strong> {{ trade.entry_time }}<br>
                    <strong>Exit Time:</strong> {{ trade.exit_time }}<br>
                    <strong>Entry Strategy Value:</strong> {{ trade.entry_strategy_value }}<br>
                    <strong>Entry Trading Volume:</strong> {{ trade.entry_trading_volume }}<br>
                    <strong>Exit Strategy Value:</strong> {{ trade.exit_strategy_value }}<br>
                    <strong>Exit Trading Volume:</strong> {{ trade.exit_trading_volume }}<br>
                    <strong>Profit/Loss Dollars:</strong> ${{ trade.profit_loss_dollars }}<br>
                    <strong>Profit/Loss Percent:</strong> {{ trade.profit_loss_percent }}<br>
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

    # Render the main report template with data
    main_report_rendered = Template(main_report_template).render(data)

    # Save the main report HTML content to a file
    with open(f"{data['ticker']}_earnings_report.html", "w") as main_report_file:
        main_report_file.write(main_report_rendered)

    # Consolidated HTML file for all trades
    consolidated_trade_template = Template(trade_template).render(data.get("sim_company_2", {}))

    # Save consolidated trade HTML content to a file
    with open(f"{data['ticker']}_Trades.html", "w") as consolidated_trade_file:
        consolidated_trade_file.write(consolidated_trade_template)

    print("HTML files generated successfully.")

# Example usage:
generate_html_reports(data)
