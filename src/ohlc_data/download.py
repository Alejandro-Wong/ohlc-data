import os
import datetime
import importlib

import ohlc_data
from ohlc_data.get import OHLC
from ohlc_data.authenticate import authenticate_alpaca


def main():
    """
    Script for downloading OHLC data from either Alpaca or Yahoo Finance APIs to a designated folder
    """

    # Symbol list
    symbols = []

    # Acceptable period and interval
    period_accept = ['y','d']
    interval_accept = ['m','h','d']    

    # .env path for alpaca keys
    env_path = os.path.dirname(ohlc_data.__file__)
    ohlc_data_files = [f for f in os.listdir(env_path)]

    # Check for ohlc_csv folder
    print('\n','Checking for ohlc_csv folder...','\n')
    if not os.path.isdir('./ohlc_csv'):
        print('\n',f'ohlc_csv folder not found, creating ohlc_csv folder at {os.getcwd()}','\n')

        timeframes = ['m5','m15','m30','h1','h4','d1']
        os.mkdir('./ohlc_csv')
        for t in timeframes:
            os.mkdir(f'./ohlc_csv/{t}')
        
        print('\n','ohlc_csv folder created','\n')
    else:
        print('ohlc_csv found')

    # Choose Single Ticker or Multi-Ticker
    while True:
        try:
            print('\n')
            single_multi = input('Download data for one symbol (1) or multiple symbols? (2): ')
            if int(single_multi) == 1 or int(single_multi) == 2:
                break
            else:
                print('Invalid choice. Please choose 1 or 2.')
        except ValueError:
            continue

    # Single Ticker chosen
    if int(single_multi) == 1:
        while True:
            try:
                print('\n')
                symbol = input('Enter symbol: ').strip().upper()
                if len(symbol) <= 5:
                    break
                else:
                    print('You may have entered an invalid symbol, try again')
            except ValueError:
                continue

    # Multi-Ticker chosen
    elif int(single_multi) == 2:
        while True:
            try:
                print('\n')
                symbol_list = input('Enter symbols (comma separated): ').strip().upper()
                symbols = [x.strip() for x in symbol_list.split(',')]
                if symbols:
                    break
                else:
                    print('You must enter at least one symbol.')
            except ValueError:
                continue

    # Choose source
    while True:
        try:
            print('\n')
            source = input('Source (1 for alpaca, 2 for yfinance): ')
            if int(source) == 1 and '.env' not in ohlc_data_files:
                authenticate_alpaca(env_path)
                importlib.reload(ohlc_data.get)
                break
            elif int(source) == 1 or int(source) == 2:
                break
            else:
                print('Invalid choice. Please choose 1 or 2.')
        except ValueError:
            print('Invalid Input')
            continue

    # Choose period, interval
    while True:
        try:
            print('\n')
            period = input('Period: ')
            print('\n')
            interval = input('Interval: ')

            # Validity check
            if (
                any(p in period for p in period_accept) and
                any(i in interval for i in interval_accept) and
                len(period) <= 3 and
                len(interval) <= 4
                ):
                break
            else:
                print(
                    'Invalid input. Please check input for correct ticker, period, and interval', '\n',
                    'Valid periods: "y", "d"', '\n',
                    'Valid intervals:  "m", "h", "d"', '\n'
                )
        except ValueError:
            continue

    # Choose start and end date
    while True:
        if 'd' in interval:
            format =  '%Y-%m-%d'
            print('\n')
            start_input = input('Start date (YYYY-MM-DD) Leave blank if none: ')
            print('\n')
            end_input =  input('End date (YYYY-MM-DD) Leave blank if none: ')
        else:
            format = '%Y-%m-%d %H:%M:%S'
            print('\n')
            start_input = input('Start date (YYYY-MM-DD HH:MM:SS) Leave blank if none: ')
            print('\n')
            end_input =  input('End date (YYYY-MM-DD HH:MM:SS) Leave blank if none: ')

        if start_input == '' and end_input == '':
            start_date = None
            end_date = None
            break
        elif  start_input == '' and end_input != '':
            start_date = None
            try:
                end_date = datetime.strptime(end_input, format)
                break
            except ValueError:
                print('Invalid datetime format. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS')
        elif start_input != '' and end_input != '':
            try:
                start_date = datetime.strptime(start_input, format)
                end_date = datetime.strptime(end_input, format)
                break
            except ValueError:
                print('Invalid datetime format. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS')
        else:
            print('Check Start Date and End Date inputs and try again. Something is wrong.')
            continue

    # Download OHLC data, save as CSV
    print('\n')
    print('Downloading OHLC data...','\n')

    subdir = (
        'm5' if interval == '5m' 
        else 'm15' if interval == '15m' 
        else 'm30' if interval == '30m'
        else 'h1' if interval == '1h'
        else 'h4' if interval == '4h'
        else 'd1' if interval == '1d'
        else None # TO DO: create function for creating new folder for new interval
        )

    if int(single_multi) == 2:

        if int(source) == 1:
            for symbol in symbols:
                df = OHLC(symbol, period, interval, start_date, end_date).from_alpaca()
                df.to_csv(f'ohlc_csv/{subdir}/{symbol}_{period}_{interval}.csv')

        elif int(source) == 2:
            for symbol in symbols:
                df = OHLC(symbol, period, interval, start_date, end_date).from_yfinance()
                df.to_csv(f'ohlc_csv/{subdir}/{symbol}_{period}_{interval}.csv')
    
    else:
        if int(source) == 1:
            df = OHLC(symbol, period, interval, start_date, end_date).from_alpaca()
        elif int(source) == 2:
            df = OHLC(symbol, period, interval, start_date, end_date).from_yfinance()

        df.to_csv(f'ohlc_csv/{subdir}/{symbol}_{period}_{interval}.csv')

    print("OHLC data downloaded successfully!")

if __name__ == "__main__":
    main()

