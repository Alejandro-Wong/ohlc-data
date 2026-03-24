from ohlc_data.file_utils import create_ohlc_folder
from ohlc_data.scripts import run_scripts


def main() -> None:
    ohlc_path = './ohlc_csv/'
    create_ohlc_folder(ohlc_path=ohlc_path)
    run_scripts(ohlc_path=ohlc_path)

if __name__ == "__main__":
    main()