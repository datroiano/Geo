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

# should be good enough (might need to revisit this)
