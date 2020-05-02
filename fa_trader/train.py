from datetime import datetime

import fire
import pandas as pd

from fa_trader.load import load_csvs
from fa_trader.preprocess import build_x_dataframe, build_y_dataframe


def train(model='svm'):
    start = datetime.now()
    trades = load_csvs()
    X, meta = build_x_dataframe(trades)
    y = build_y_dataframe(X)
    runtime = (datetime.now() - start).seconds
    print(runtime)
    pd.options.display.width = 0
    print(X.head(5))


if __name__ == "__main__":
    fire.Fire(train)
