import os
import ast
from ast import AST
import json
import importlib

import yfinance as yf
from datetime import datetime
from simple_term_menu import TerminalMenu
from typing import cast

import ohlc_data
from ohlc_data.ohlc import OHLC
from ohlc_data.authenticate import authenticate_alpaca


def dropdown(prompt:str, options: list[str], show_selection: bool=True) -> list[str]:
    """
    Dropdown menu to select from two or more choices
    Returns selected choice
    """
    print('\n')
    print(prompt)

    menu_options = options
    menu = TerminalMenu(menu_options)
    menu_select = cast(slice, menu.show())
    menu_selected = menu_options[menu_select]

    if show_selection == True:
        print(menu_selected)
    
    return menu_selected


def validate_date(date: str, format_str: str):
    """
    Validate whether date string is in appropriate datetime format
    """
    try: 
        datetime.strptime(date, format_str)
        return True
    except ValueError:
        return False
    

def validate_ticker(ticker: str):
    """
    Validate whether ticker exists on American stock exchange
    """
    check = yf.Ticker(ticker).history(period='1d', interval='1d')
    if check.empty:
        return False
    else:
        return True
                
                
def custom_period(intraday=False) -> tuple[str, str]:
    """
    Allows user to input a custom date range when retrieving OHLC data from 
    selected API.

    Intraday=True for intraday data, must include time into range

    Returns start date and end date
    """
    start_date = None
    end_date = None
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'

    if intraday == True:
        while True:
            start_input = input('Start Datetime (YYYY-MM-DD HH:MM:SS) : ')
            if not validate_date(start_input, datetime_format):
                print('Invalid datetime, ensure YYYY-MM-DD HH:MM:SS')
                continue
            else:
                start_date = start_input
                break

        while True:
            end_input = input('End Datetime (YYYY-MM-DD HH:MM:SS) : ')
            if not validate_date(end_input, datetime_format):
                print('Invalid datetime, ensure YYYY-MM-DD HH:MM:SS')
                continue
            else:
                end_date = end_input
                break
    else:
        while True:
            print('\n')
            start_input = input('Start date (YYYY-MM-DD): ')
            if not validate_date(start_input, date_format):
                print('Invalid date, ensure YYYY-MM-DD format')
                continue
            else:
                start_date = start_input
                break

        while True:
            print('\n')
            end_input = input('End date (YYYY-MM-DD): ')
            if not validate_date(end_input, date_format):
                print('Invalid date, ensure YYYY-MM-DD format')
                continue
            else:
                end_date = end_input
                break
    
    return start_date, end_date



module_path = os.path.dirname(ohlc_data.__file__)
prev_ticker_path = f'{module_path}/multi_tickers.json'


def tickers_to_json(tickers: str | list) -> None:
    """
    Saves dictionary of list of tickers to json, or
    adds to existing json.
    """

    if not os.path.isfile(f'{prev_ticker_path}'): 
        tickers_dict = {}
        tickers_dict[str(datetime.today())] = str(tickers)
        with open(f'{prev_ticker_path}', 'w') as f:
            json.dump(tickers_dict, f)
    else:
        with open(f'{prev_ticker_path}', 'r') as f:
            data = json.load(f)
            if str(tickers) not in data.values():
                data[str(datetime.today())] = str(tickers)
    
        with open(f'{prev_ticker_path}', 'w') as f:
            json.dump(data, f, indent=4)


def enter_multi_ticker() -> list:
    """
    Enter multiple tickers manually, returns list   
    """
    while True:
        print('\n')
        ticker_list = input('Enter tickers (separate tickers with single space, not case-sensitive): ').strip().upper()

        if not ticker_list:
            print('\n')
            print('You must enter at least one ticker.')
            continue
        
        ticker_split= ticker_list.split(' ')
        tickers = [ticker.strip() for ticker in ticker_split if ticker.strip()]
        ticker_check = [validate_ticker(ticker) for ticker in tickers]

        if False in ticker_check:
            print('\n')
            print('At least one ticker might have been input incorrectly, make sure to separate each ticker with a space')
            continue
        else:
            break

    return tickers


def ticker_select() -> str | list[str]:
    """
    Full ticker select script
    """

    ticker_selected = dropdown('Download data for: ', ['Single ticker', 'Multiple tickers'])

    # Single Ticker chosen
    if ticker_selected == 'Single ticker':
        while True:
            print('\n')
            ticker = input('Enter ticker: ').strip().upper()
            
            if validate_ticker(ticker):
                return ticker
                
            else:
                print('You may have entered an invalid or unsupported ticker, try again')
        

    # Multi-Ticker chosen
    elif ticker_selected == 'Multiple tickers':

        # check for json
        if os.path.isfile(f'{module_path}/multi_tickers.json'):
            manual_or_list = dropdown("", ["Enter tickers manually", "Select from previous tickers"])

            if manual_or_list == "Select from previous tickers":
                with open(f'{prev_ticker_path}', 'r') as f:
                    data = json.load(f)
                previous_tickers = cast(AST, dropdown("Previous tickers: ", [t_list for t_list in data.values()]))
                tickers = ast.literal_eval(previous_tickers)
            else:
                tickers = enter_multi_ticker()

        # no json
        else:
            tickers = enter_multi_ticker()

        # save tickers to json
        tickers_to_json(tickers=tickers)

        return tickers

    else:
        raise ValueError("Error encountered while selecting ticker")
    

def source_select():
    """
    Select source for OHLC download: Alpaca or Yfinance
    """
    # .env path for alpaca keys
    env_path = os.path.dirname(ohlc_data.__file__)
    ohlc_data_files = [f for f in os.listdir(env_path)]

    # Choose source
    source_selected = dropdown('Choose source: ', ['Alpaca','Yfinance'])

    # Authentication
    while True:
        if source_selected == 'Alpaca' and '.env' not in ohlc_data_files:
            authenticate_alpaca(env_path)
            importlib.reload(ohlc_data)
            break
        else:
            break

    return source_selected




