import csv
from os import listdir
from os.path import join, abspath, dirname
from typing import Set

from fa_trader import FATrade

DATA_DIR = join(dirname(dirname(abspath(__file__))), 'fa-data')


def load_csvs() -> Set[FATrade]:
    """
    Build a set (unique) of trades from the data directory where you should keep all your FA exports
    :return: set of FATrade objects
    """
    trades = set()  # use a set so we don't have to care about overlapping exports
    for filename in listdir(DATA_DIR):
        if filename.endswith('.csv'):
            with open(join(DATA_DIR, filename)) as f:
                reader = csv.reader(f, delimiter=',')
                next(reader)  # skip header columns
                for row in reader:
                    trades.add(FATrade(*row))  # the order of the constructor params matches the csv rows
    return trades


if __name__ == "__main__":
    print(load_csvs())
