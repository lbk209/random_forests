#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

from pathlib import Path
import warnings
import pandas as pd
import os
import pickle

warnings.filterwarnings('ignore')

zipline_root = None
try:
    zipline_root = os.environ['ZIPLINE_ROOT']
except KeyError:
    print('Please ensure a ZIPLINE_ROOT environment variable is defined and accessible '
          '(or alter the script and manually set the path')
    exit()
custom_data_path = Path(zipline_root, 'custom_data')

idx = pd.IndexSlice


def create_split_table():
    df = pd.DataFrame(columns=['sid', 'ratio', 'effective_date'],
                         data=[[1, 1.0, pd.to_datetime('2010-01-01')]])
    df.to_csv(custom_data_path / 'stooq_jp_splits.csv', index=None)

    
def load_prices():
    df = (pd.read_csv(custom_data_path / 'stooq_jp_tse_stocks_prices.csv', parse_dates=['date'])
            .set_index(['ticker','date'])
            .sort_index(level=['ticker','date']))

    return (df.loc[idx[:, '2014': '2019'], :]
            .unstack('ticker')
            .sort_index()
            .tz_localize('UTC')
            .ffill(limit=5)
            .dropna(axis=1)
            .stack('ticker')
            .swaplevel())


def load_symbols(tickers):
    df = pd.read_csv(custom_data_path / 'stooq_jp_tse_stocks_tickers.csv', index_col=0)
    #df = pd.read_csv(custom_data_path / 'stooq_jp_tse_stocks_tickers.csv')
    return (df[df.ticker.isin(tickers)]
            .reset_index(drop=True)
            .reset_index()
            .rename(columns={'index': 'sid'}))


def main():
    prices = load_prices()
    print(prices.info(null_counts=True))
    tickers = prices.index.unique('ticker')

    symbols = load_symbols(tickers)
    print(symbols.info(null_counts=True))
    symbols.to_csv(custom_data_path / 'stooq_jp_sid_equities.csv', index=False)

    dates = prices.index.unique('date')
    start_date = dates.min()
    end_date = dates.max()

    store = {}
    #for sid, symbol in symbols.set_index('sid').symbol.items():
    for sid, symbol in symbols.set_index('sid').ticker.items():
        store[f'jp/{sid}'] = prices.loc[symbol]
    
    fname_pickle = 'stooq_jp_sid_prices.pickle'
    #fname_pickle = 'stooq.pickle'
    with open(custom_data_path / fname_pickle, 'wb') as handle:
        pickle.dump(store, handle)    

    create_split_table()

    
if __name__ == '__main__':
    main()