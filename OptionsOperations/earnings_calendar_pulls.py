import statistics

from OptionsOperations.__init__ import *
from OptionsOperations.naming_and_cleaning import *


class TestCompanies:
    def __init__(self, min_revenue, from_date, to_date, report_hour="amc", underlying_ticker=""):
        self.min_revenue = int(min_revenue)
        self.from_date = from_date
        self.to_date = to_date
        self.underlying_ticker = underlying_ticker
        self.report_hour = report_hour

        # Make finnhub client request to retrieve tickers, report dates, and time period
        self.symbols_list = self.finnhub_retrieval()

        # Make initial Polygon request to retrieve average price
        self.price_averages = self.polygon_retrieval(avg_time_start="09:30:00", avg_time_end="11:00:00")

    def finnhub_retrieval(self):
        finnhub_client = finnhub.Client(api_key="ck45p3hr01qus81pq4u0ck45p3hr01qus81pq4ug")

        raw_data = finnhub_client.earnings_calendar(_from=self.from_date, to=self.to_date,
                                                    symbol=self.underlying_ticker, international=False)
        earnings_calendar = raw_data["earningsCalendar"]

        symbols_list = []
        for item in earnings_calendar:
            if (
                    (not self.report_hour or item["hour"] == self.report_hour)
                    and item["revenueEstimate"] is not None
                    and str(item["revenueEstimate"]).isdigit()
                    and int(item["revenueEstimate"]) >= self.min_revenue
            ):
                new_entry = {'symbol': item["symbol"],
                             'date': item["date"],
                             'period': item["hour"]
                             }

                symbols_list.append(new_entry)

        return symbols_list

    def polygon_retrieval(self, avg_time_start, avg_time_end, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        price_averages = []
        i = 0

        headers = {
            "Authorization": f"Bearer {polygon_api_key}"
        }
        multiplier = "1"
        timespan = "minute"

        for item in self.symbols_list:
            if item["date"] is None or item["symbol"] is None:
                continue
            else:
                ticker = item['symbol']
                from_date = item['date']
                to_date = item['date']

                endpoint = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

                response = requests.get(endpoint, headers=headers).json()

                processed_data = []
                for result in response['results']:
                    if int(to_unix_time(f'{from_date} {avg_time_start}')) <= int(result['t']) <= int(to_unix_time(f'{to_date} {avg_time_end}')):
                        ticker = response['ticker']
                        time = from_unix_time(result['t'])
                        high = result['h']
                        low = result['l']

                        processed_data.append({
                            'ticker': ticker,
                            'date': time,
                            'high': high,
                            'low': low
                        })

                raw_prices = []
                for data_point in processed_data:
                    raw_prices.append((data_point['high'] + data_point['low']) / 2)

                new_entry = {
                    'symbol': ticker,
                    'avg_price': round(statistics.mean(raw_prices), ndigits=2)
                }

                price_averages.append(new_entry)

                i += 1
                if i >= 4:
                    break

        return price_averages





x = TestCompanies(min_revenue=1000000000, from_date="2023-11-01", to_date="2023-11-29", report_hour="amc")
print(x.price_averages)


# url = "https://api.tdameritrade.com/v1/marketdata/chains"
#
# api_key = '50KAT7SOS174SYNEXYD1EFS9GDUOMVGX'
#
# symbol = 'AAPL'
#
# query_params = {
#     'apikey': api_key,
#     'symbol': symbol,
#     'strikeCount': 2,
# }
#
# response = requests.get(url, params=query_params)
#
# if response.status_code == 200:
#     print(response.json())
# else:
#     print("Error:", response.status_code, response.text)