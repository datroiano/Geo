from OptionsOperations.__init__ import *
# Example optionsTicker = 'O:AAPL230915C00170000'


def create_options_ticker(ticker, strike, expiration_year, expiration_month, expiration_day, contract_type):
    ticker = str(ticker.upper())
    strike = str(strike)
    expiration_year = str(expiration_year)
    expiration_month = str(expiration_month)
    expiration_day = str(expiration_day)

    if contract_type:
        contract_type = 'C'
    else:
        contract_type = 'P'

    # strike formatting for 1000: 01000000
    # strike formatting for 1000.5: 01000500
    # strike formatting for 170.5: 00170500

    strike_d = decimal.Decimal(strike)
    num_dec = strike_d.as_tuple().exponent
    length_strike = len(strike)
    strike_string_for_insertion = ''

    if num_dec == 0:
        if length_strike == 1:
            # case: 0000*000
            strike_string_for_insertion = f'0000{strike}000'
        elif length_strike == 2:
            # case: 000**000
            strike_string_for_insertion = f'000{strike}000'
        elif length_strike == 3:
            # case: 00***000
            strike_string_for_insertion = f'00{strike}000'
        elif length_strike == 4:
            # case: 0****000
            strike_string_for_insertion = f'0{strike}000'
        elif length_strike == 5:
            # case *****000
            strike_string_for_insertion = f'{strike}000'
        else:
            return ValueError
    elif num_dec == -1:  # case with decimal equals 1 after decimal point
        strike = strike.replace(".", "")
        length_strike = len(strike)
        if length_strike == 1:
            # case 00000*00
            strike_string_for_insertion = f'00000{strike}00'
        elif length_strike == 2:
            # case 0000**00
            strike_string_for_insertion = f'0000{strike}00'
        elif length_strike == 3:
            # case 000***00
            strike_string_for_insertion = f'000{strike}00'
        elif length_strike == 4:
            # case 00****00
            strike_string_for_insertion = f'00{strike}00'
        elif length_strike == 5:
            # case 0*****00
            strike_string_for_insertion = f'0{strike}00'
        elif length_strike == 6:
            # case ******00
            strike_string_for_insertion = f'{strike}00'
    elif num_dec == -2: # case with decimals equalling 2
        strike = strike.replace(".", "")
        length_strike = len(strike)
        if length_strike == 1:
            # case 000000*0
            strike_string_for_insertion = f'000000{strike}0'
        elif length_strike == 2:
            # case 00000**0
            strike_string_for_insertion = f'00000{strike}0'
        elif length_strike == 3:
            # case 0000***0
            strike_string_for_insertion = f'0000{strike}0'
        elif length_strike == 4:
            # case 000****0
            strike_string_for_insertion = f'000{strike}0'
        elif length_strike == 5:
            # case 00*****0
            strike_string_for_insertion = f'00{strike}0'
        elif length_strike == 6:
            # case 0******0
            strike_string_for_insertion = f'0{strike}0'
        elif length_strike == 7:
            # case *******0
            strike_string_for_insertion = f'{strike}0'
    else:
        return ValueError

    # Above logic is equipt to handle any strike 0-99999 with up to two decimal places (enough for most purposes)

    if len(expiration_month) == 1:
        expiration_month = f'0{expiration_month}'
    if len(expiration_year) == 1:
        expiration_year = f'0{expiration_year}'
    if len(expiration_day) == 1:
        expiration_day = f'0{expiration_day}'

    expiry = f'{expiration_year}{expiration_month}{expiration_day}'

    constructed_return = f'O:{ticker}{expiry}{contract_type}{strike_string_for_insertion}'

    return constructed_return


def to_unix_time(datetime_str):
    try:
        # Parse the input datetime string to a datetime object
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

        # Convert the datetime object to Unix timestamp in milliseconds
        unix_time_ms = int(time.mktime(dt_obj.timetuple()) * 1000)
        return str(unix_time_ms)
    except ValueError:
        return "Invalid datetime format. Please provide a datetime in the format '%Y-%m-%d %H:%M:%S'."


def from_unix_time(unix_time_str):
    try:
        # Parse the input Unix timestamp string to an integer
        unix_time_ms = int(unix_time_str)

        # Convert Unix timestamp in milliseconds to a datetime object
        dt_obj = datetime.fromtimestamp(unix_time_ms / 1000.0)

        # Format the datetime object as a string
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime
    except ValueError:
        return "Invalid Unix timestamp format. Please provide a numerical Unix timestamp."

# Example usage:
# unix_time = to_unix_time('2023-09-13 15:30:00')
# formatted_datetime = from_unix_time('1694338500000')


def next_friday(input_date=None):
    if input_date is None:
        today = date.today()
    else:
        today = datetime.strptime(input_date, '%Y-%m-%d').date()

    days_until_friday = (4 - today.weekday()) % 7   # Calculate days until next Friday (0=Monday, 1=Tuesday)
    if days_until_friday == 0:
        days_until_friday = 7  # If today is Friday, move to next Friday
    next_friday_date = today + timedelta(days=days_until_friday)

    # Format the date as 'YYYY-MM-DD'
    formatted_date = next_friday_date.strftime('%Y-%m-%d')
    return formatted_date


def next_third_friday(input_date):
    date_obj = datetime.strptime(input_date, '%Y-%m-%d')
    day_of_week = date_obj.weekday()
    days_until_friday = (4 - day_of_week) % 7
    first_friday = date_obj + timedelta(days=days_until_friday)
    third_friday = first_friday + timedelta(weeks=2)

    if third_friday.month != date_obj.month:
        next_month = date_obj.replace(day=1) + timedelta(days=32)
        third_friday = next_month.replace(day=1)

        while third_friday.weekday() != 4:
            third_friday += timedelta(days=1)

        third_friday += timedelta(weeks=2)

    return third_friday.strftime('%Y-%m-%d')


def closest_number(numbers_set, target):
    closest = None
    min_difference = float('inf')

    for number in numbers_set:
        difference = abs(number - target)
        if difference < min_difference:
            min_difference = difference
            closest = number

    return closest
