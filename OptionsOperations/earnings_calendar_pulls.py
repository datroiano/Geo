import statistics
from OptionsOperations.naming_and_cleaning import *


class TestCompanies:
    def __init__(self, min_revenue, from_date, to_date, data_limit, skipped_tickers, report_hour="amc", underlying_ticker="",
                 max_companies=1):
        self.min_revenue = int(min_revenue)
        self.from_date = from_date
        self.to_date = to_date
        self.underlying_ticker = underlying_ticker
        self.report_hour = report_hour
        self.max_companies = max_companies
        self.data_limit = data_limit
        self.skipped_tickers = skipped_tickers

        # Make finnhub client request to retrieve tickers, report dates, and time period
        self.symbols_list = self.finnhub_retrieval()

        # Make initial Polygon request to retrieve average price
        self.price_averages = self.polygon_retrieval(avg_time_start="09:30:00", avg_time_end="11:00:00")

        # Make secondary Polygon request to retrieve and sort option chains, choosing target strike
        self.correct_strikes = self.option_chain_retrieval(data_limit=self.data_limit)

    def finnhub_retrieval(self):
        finnhub_client = finnhub.Client(api_key="ck45p3hr01qus81pq4u0ck45p3hr01qus81pq4ug")

        raw_data = finnhub_client.earnings_calendar(_from=self.from_date, to=self.to_date,
                                                    symbol=self.underlying_ticker, international=False)
        earnings_calendar = raw_data["earningsCalendar"]

        symbols_list = []
        for item in earnings_calendar:
            if len(self.skipped_tickers) != 0:
                skip_flag = False  # Flag to track if a match is found in skipped_tickers
                for tick in self.skipped_tickers:
                    if item['symbol'] == tick:
                        skip_flag = True  # Set flag if a match is found
                        break  # Break out of the inner loop

                if skip_flag:
                    continue  # Continue the outer loop if a match is found in skipped_tickers

            if (
                    (not self.report_hour or item["hour"] == self.report_hour)
                    and item["revenueEstimate"] is not None
                    and str(item["revenueEstimate"]).isdigit()
                    and int(item["revenueEstimate"]) >= self.min_revenue
            ):
                if item['hour'] == 'amc':
                    trade_date = item['date']
                elif item['hour'] == 'bmo':
                    trade_date = day_before(item['date'])
                else:
                    continue

                earnings_report_date = item['date']
                new_entry = {
                    'symbol': item["symbol"],
                    'trade_date': trade_date,
                    'earnings_date': earnings_report_date,
                    'period': item["hour"],
                    'revenue_estimate': item["revenueEstimate"],
                    'revenue_actual': item["revenueActual"],
                    'fiscal_year': item['year'],
                    'fiscal_quarter': item['quarter'],
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

        j = 0
        for item in self.symbols_list:
            j += 1

            ticker = item['symbol']
            from_date = item['trade_date']
            to_date = item['trade_date']

            endpoint = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

            response = requests.get(endpoint, headers=headers).json()

            processed_data = []
            try:
                for result in response['results']:
                    if (int(to_unix_time(f'{from_date} {avg_time_start}')) <= int(result['t']) <=
                            int(to_unix_time(f'{to_date} {avg_time_end}'))):
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
            except KeyError:
                logger.info(f"Polygon API data empty (potentially cool down). Iteration fail: {j}")
                break

            raw_prices = []
            for data_point in processed_data:
                raw_prices.append((data_point['high'] + data_point['low']) / 2)

            earnings_report_date = item['earnings_date']
            new_entry = {
                'symbol': ticker,
                'avg_price': round(statistics.mean(raw_prices), ndigits=2),
                'trade_date': from_date,
                'earnings_report_date': earnings_report_date,
                'period': item["period"],
                'revenue_estimate': item["revenue_estimate"],
                'revenue_actual': item["revenue_actual"],
                'fiscal_year': item['fiscal_year'],
                'fiscal_quarter': item['fiscal_quarter'],
            }

            price_averages.append(new_entry)

            i += 1
            logger.info(f'Stock Price Iteration Pass: {i}')
            if i >= self.max_companies:
                break

        return price_averages

    def option_chain_retrieval(self, data_limit, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        correct_strikes = []
        headers = {
            "Authorization": f"Bearer {polygon_api_key}"
        }

        # print(f'Ticker Count for Option Chain Retrieval: {len(self.price_averages)}')  # Reference only

        for item in self.price_averages:
            ticker = item["symbol"]
            endpoint = f"https://api.polygon.io/v3/snapshot/options/{ticker}?limit={data_limit}"

            response = requests.get(endpoint, headers=headers).json()

            raw_strikes = []
            for chain in response['results']:
                raw_strikes.append(chain['details']['strike_price'])

            new_entry = {
                'symbol': ticker,
                'target_strike': closest_number(numbers_set=raw_strikes, target=item["avg_price"]),
                'trade_date': item['trade_date'],
                'target_expiration_date': next_friday(item['trade_date']),
                'strikes_iterated': len(raw_strikes),
                'earnings_report_date': item['earnings_report_date'],
                'period': item["period"],
                'revenue_estimate': item["revenue_estimate"],
                'revenue_actual': item["revenue_actual"],
                'fiscal_year': item['fiscal_year'],
                'fiscal_quarter': item['fiscal_quarter'],
                'average_entry_underlying_price': item['avg_price']
            }
            correct_strikes.append(new_entry)

        return correct_strikes


# SAMPLE USAGE
# simulation = TestCompanies(min_revenue=5_000_000_000, from_date="2023-11-01", to_date="2023-11-29",
#                            report_hour="", data_limit=60)
# print(simulation.symbols_list)
# - which is in the format: [{'symbol': 'SNPS', 'target_strike': 550,
# 'date': '2023-11-29', 'target_expiration_date': '2023-12-01'}]

