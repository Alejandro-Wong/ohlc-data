
import os
import importlib
from simple_term_menu import TerminalMenu

import ohlc_data
from ohlc_data.get import OHLC
from ohlc_data.authenticate import authenticate_alpaca
from ohlc_data.utils import validate_date

def main():
    """
    Creates ohlc_csv folder and timeframe subfolders, walks user through prompts to download
    OHLC data from Alpaca or Yahoo Finance APIs to appropriate folders
    """

    df = None 
    symbols = []

    # Acceptable period and interval
    period_accept = ['y','d']
    interval_accept = ['m','h','d']    

    # Valid Datetime formats
    start_date = None
    end_date = None
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'

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
    
    # Download data for one or multiple tickers
    symbols_options = ['One symbol','Multiple symbols']
    symbols_menu = TerminalMenu(symbols_options)

    print('\n')
    print("Download data for: ")
    print('\n')

    symbols_select = symbols_menu.show()
    symbols_selected = symbols_options[symbols_select]
    print(symbols_selected)

    # Single Ticker chosen
    if symbols_selected == 'One symbol':
        while True:
            print('\n')
            symbol = input('Enter symbol: ').strip().upper()
            if len(symbol) <= 5:
                break
            else:
                print('You may have entered an invalid or unsupported symbol, try again')

    # Multi-Ticker chosen
    elif symbols_selected == 'Multiple symbols':
        while True:
            print('\n')
            symbol_list = input('Enter symbols (separate symbols with single space, not case-sensitive): ').strip().upper()

            if not symbol_list:
                print('\n')
                print('You must enter at least one symbol.')
                continue
            
            symbol_split = symbol_list.split(' ')
            symbols = [symbol.strip() for symbol in symbol_split if symbol.strip()]

            length_check = [len(symbol.strip()) <= 5 for symbol in symbols]
            if False in length_check:
                print('\n')
                print('At least one symbol might have been input incorrectly, make sure to separate each symbol with a space')
                continue
            else:
                break

    # Source
    print('\n')
    print('Choose source: ')
    print('\n')

    source_options = ['Alpaca', 'Yfinance']
    source_menu = TerminalMenu(source_options)
    source_select = source_menu.show()
    source_selected = source_options[source_select]
    
    while True:
        if source_selected == 'Alpaca' and '.env' not in ohlc_data_files:
            authenticate_alpaca(env_path)
            importlib.reload(ohlc_data.get)
            break
        else:
            break

    # Choose period
    while True:
        print('\n')
        period = input('Period: ')

        if period:
            if period[-1] in period_accept and len(period) <= 4:
                break
            else:
                print('\n')
                print('Invalid input','\n','Valid periods: [number]y or [number]d')
                continue
        else:
            break
    
    # Choose interval
    print('\n')
    print('Interval: ')
    print('\n')

    interval_options = ['5m', '15m', '30m', '1h', '4h', '1d']
    interval_menu = TerminalMenu(interval_options)
    interval_select = interval_menu.show()
    interval_selected = interval_options[interval_select]

    # End date/datetime optional if period    
    if period:
        if 'd' in interval_selected:
            while True:
                print('\n')
                end_input = input('End date (YYYY-MM-DD) (Optional) : ')
                if end_input and not validate_date(end_input, date_format):
                    print('Invalid date, ensure YYYY-MM-DD format')
                    continue
                else:
                    end_date = end_input
                    break
        else:
            while True:
                print('\n')
                end_input = input('End Datetime (YYYY-MM-DD HH:MM:SS) (Optional) : ')
                if end_input and not validate_date(end_input, datetime_format):
                    print('Invalid datetime, ensure YYYY-MM-DD HH:MM:SS')
                    continue
                else:
                    end_date = end_input
                    break







        
    


if __name__ == "__main__":
    main()
