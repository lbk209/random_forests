#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'LBK'

from pathlib import Path
import warnings
import pandas as pd
import os
import pickle

warnings.filterwarnings('ignore')

try:
    zipline_root = os.environ['ZIPLINE_ROOT']
except KeyError:
    print('Please ensure a ZIPLINE_ROOT environment variable is defined and accessible '
          '(or alter the script and manually set the path')
    zipline_root = None
    exit()
custom_data_path = Path(zipline_root, 'custom_data')


def create_split_table():
    df = pd.DataFrame(columns=['sid', 'ratio', 'effective_date'],
                         data=[[1, 1.0, pd.to_datetime('2010-01-01')]])
    df.to_csv(custom_data_path / 'stooq_jp_splits.csv', index=None)

    
def load_prices(start='2017', end='2019'):
    idx = pd.IndexSlice
    df = (pd.read_csv(custom_data_path / 'stooq_jp_tse_stocks_prices.csv', parse_dates=['date'])
            .set_index(['ticker','date'])
            .sort_index(level=['ticker','date']))
    return (df.loc[idx[:, start:end], :]
            .unstack('ticker')
            .sort_index()
            .tz_localize('UTC')
            .ffill(limit=5)
            .dropna(axis=1)
            .stack('ticker')
            .swaplevel())


def load_symbols(tickers):
    df = pd.read_csv(custom_data_path / 'stooq_jp_tse_stocks_tickers.csv', index_col=0)
    return (df[df.ticker.isin(tickers)]
            .reset_index(drop=True)
            .reset_index()
            .rename(columns={'index': 'sid'}))


def load(start='2017', end='2019'):
    prices = load_prices(start, end)
    print(prices.info(null_counts=True))
    tickers = prices.index.unique('ticker')

    symbols = load_symbols(tickers)
    print(symbols.info(null_counts=True))
    symbols.to_csv(custom_data_path / 'stooq_jp_sid_equities.csv', index=False)

    dates = prices.index.unique('date')
    start_date = dates.min()
    end_date = dates.max()

    store = {}
    for sid, symbol in symbols.set_index('sid').ticker.items():
        store[f'jp/{sid}'] = prices.loc[symbol]
    
    fname_pickle = 'stooq_jp_sid_prices.pickle'
    with open(custom_data_path / fname_pickle, 'wb') as handle:
        pickle.dump(store, handle)    

    create_split_table()

    
if __name__ == '__main__':
    load()