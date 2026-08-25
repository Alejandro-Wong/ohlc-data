import os
from ohlc_data.ohlc import OHLC


def create_ohlc_folder(ohlc_path: str) -> None:
    """
    Creates ohlc_csv folder and timeframe subfolders 
    """

    # Check for ohlc_csv folder
    print('\nChecking for ohlc_csv folder...\n')
    if not os.path.isdir(ohlc_path):
        print(f'\nohlc_csv folder not found, creating ohlc_csv folder at {os.getcwd()}\n')

        # Create ohlc_csv folder 
        os.mkdir(ohlc_path)
        print('\nohlc_csv folder created\n')
    else:
        print('\nohlc_csv found\n')


def download_and_save(path: str, ticker: str, source: str, period: str | None = None, 
                    interval: str | None = None, start_date: str | None = None, end_date: str | None = None,
                    pre_post: bool = False) -> None:
    """
    Save OHLC data to CSV
    """
    
    if source not in ['yfinance','alpaca']:
        raise ValueError('Incorrect source input. (yfinance or alpaca)')

    period = period or '1y'
    interval = interval or '1d'

    if source == 'yfinance':
        if pre_post != False:
            print('Yfinance does not provide pre/post data')
        df = OHLC(ticker, period, interval, start_date, end_date).from_yfinance()
    else:
        df = OHLC(ticker, period, interval, start_date, end_date).from_alpaca(pre_post=pre_post)

    # Save to CSV
    if start_date and end_date:
        filename = f'{ticker}_{start_date[:4]}{start_date[5:7]}_{end_date[:4]}{end_date[5:7]}_{interval}'
    elif end_date:
        filename = f'{ticker}_{end_date[:4]}{end_date[5:7]}_{period}_{interval}'
    else:
        filename = f'{ticker}_{period}_{interval}'
    
    pm_suffix = '_pm' if pre_post and source == 'alpaca' else ''

    df.to_csv(f'{path}{interval}/{filename}{pm_suffix}.csv')