from collections import defaultdict
from typing import Dict, List, Set, Tuple

import pandas as pd
from pandas import DataFrame, Series

from fa_trader import FATrade


# --- grouping --- #

def group_by_contract(trades: Set[FATrade]) -> Dict[str, List[FATrade]]:
    g = defaultdict(list)
    for t in trades:
        g[str(t)].append(t)
    return g


def group_by_ticker_date(trades: Set[FATrade]) -> Dict[str, List[FATrade]]:
    g = defaultdict(list)
    for t in trades:
        g[t.ticker_date].append(t)
    return g


# --- features --- #

def average_dte(trade_group: List[FATrade]) -> int:
    # volume weighted average
    return sum(t.dte.days * t.volume for t in trade_group) // sum(t.volume for t in trade_group)


def average_spot(trade_group: List[FATrade]) -> float:
    # volume weighted average
    return sum(t.spot * t.volume for t in trade_group) / sum(t.volume for t in trade_group)


def average_price(trade_group: List[FATrade]) -> float:
    # volume weighted average
    return sum(t.price * t.volume for t in trade_group) / sum(t.volume for t in trade_group)


def total_vol(trade_group: List[FATrade]) -> int:
    return sum(t.volume for t in trade_group)


def average_vol(trade_group: List[FATrade]) -> int:
    return sum(t.volume for t in trade_group) // len(trade_group)


def max_vol(trade_group: List[FATrade]) -> int:
    return max(t.volume for t in trade_group)


def total_premium(trade_group: List[FATrade]) -> int:
    return sum(t.premium for t in trade_group)


def average_premium(trade_group: List[FATrade]) -> int:
    return sum(t.premium for t in trade_group) // len(trade_group)


def max_premium(trade_group: List[FATrade]) -> int:
    return max(t.premium for t in trade_group)


def total_oi(trade_group: List[FATrade]) -> int:
    return sum(t.oi for t in trade_group)


def sector(trade_group: List[FATrade]) -> str:
    return trade_group[0].sector


def unusual(trade_group: List[FATrade]) -> int:
    return sum(1 for t in trade_group if t.unusual)


def num_trades(trade_group: List[FATrade]) -> int:
    return len(trade_group)


def day_of_month(trade_group: List[FATrade]) -> int:
    return sum(t.day_of_month * t.volume for t in trade_group) // sum(t.volume for t in trade_group)


def day_of_week(trade_group: List[FATrade]) -> str:
    return max((t for t in trade_group), key=lambda t: t.volume).day_of_week


def month_of_year(trade_group: List[FATrade]) -> int:
    return trade_group[0].month_of_year


def minute_of_day(trade_group: List[FATrade]) -> int:
    return sum(t.minute_of_day * t.volume for t in trade_group) // sum(t.volume for t in trade_group)


def av_percent_otm(trade_group: List[FATrade]) -> float:
    return sum(t.percent_otm * t.volume for t in trade_group) / sum(t.volume for t in trade_group)


# --- meta --- #

def max_premium_strike(trade_group: List[FATrade]) -> float:
    return max((t for t in trade_group), key=lambda t: t.premium).strike


def max_premium_exp(trade_group: List[FATrade]) -> str:
    return max((t for t in trade_group), key=lambda t: t.premium).expiry.strftime('%m/%d')


def build_x_dataframe(trades: Set[FATrade]) -> Tuple[DataFrame, DataFrame]:
    """
    Main function of this module. Runs arbitrary transforms, then converts to a (numeric) dataframe
    :param trades: Set of FATrades from load.py
    :return: Vectorized data, ready for training
    """
    def fill_feature(feature, func, m=False) -> None:
        for i, v in zip(X.index, map(func, contracts.values())):
            (meta if m else X).at[i, feature] = v

    # group contracts by ticker and date, and initialize dataframes
    contracts = group_by_ticker_date(trades)
    x_features = ['dte', 'total_vol', 'av_vol', 'max_vol', 'total_prem', 'av_prem', 'max_prem',
                  'oi', 'spot', 'price', 'sector', 'unusual', 'num_trades', 'dom', 'dow', 'mod', 'moy',
                  'av_percent_otm']
    meta_columns = ['max_prem_exp', 'max_prem_strike']
    X = pd.DataFrame(index=tuple(contracts.keys()), columns=x_features)
    meta = pd.DataFrame(index=tuple(contracts.keys()), columns=meta_columns)

    # fill in features
    fill_feature('dte', average_dte)
    fill_feature('total_vol', total_vol)
    fill_feature('av_vol', average_vol)
    fill_feature('max_vol', max_vol)
    fill_feature('total_prem', total_premium)
    fill_feature('av_prem', average_premium)
    fill_feature('max_prem', max_premium)
    fill_feature('oi', total_oi)
    fill_feature('spot', average_spot)
    fill_feature('price', average_price)
    fill_feature('sector', sector)
    fill_feature('unusual', unusual)
    fill_feature('num_trades', num_trades)
    fill_feature('dom', day_of_month)
    fill_feature('dow', day_of_week)
    fill_feature('mod', minute_of_day)
    fill_feature('moy', month_of_year)
    fill_feature('av_percent_otm', av_percent_otm)

    # meta
    fill_feature('max_prem_exp', max_premium_strike, m=True)
    fill_feature('max_prem_strike', max_premium_exp, m=True)

    return X, meta


def build_y_dataframe(X: pd.DataFrame) -> Series:
    """
    Build a binary target series from X. F
    :param X:
    :return:
    """
    pass


if __name__ == "__main__":
    pass
