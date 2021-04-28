#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'LBK'

from pathlib import Path
import os
import numpy as np
import pandas as pd

pd.set_option('display.expand_frame_repr', False)
#np.random.seed(42)

try:
    zipline_root = os.environ['ZIPLINE_ROOT']
except KeyError:
    print('Please ensure a ZIPLINE_ROOT environment variable is defined and accessible '
          '(or alter the script and manually set the path')
    zipline_root = None
    exit()
custom_data_path = Path(zipline_root, 'custom_data')


def load_equities():
    # see stooq_preprocessing.py for the csv
    return pd.read_csv(custom_data_path / 'stooq_jp_sid_equities.csv')


def ticker_generator():
    """
    Lazily return (sid, ticker, name) tuple
    """
    return (v for v in load_equities().values)


def data_generator():
    for sid, symbol, asset_name in ticker_generator():
        # see stooq_preprocessing.py for the csv
        prices_dict = pd.read_pickle(custom_data_path / 'stooq_jp_sid_prices.pickle')
        df = prices_dict[f'jp/{sid}']

        start_date = df.index[0]
        end_date = df.index[-1]

        first_traded = start_date.date()
        auto_close_date = end_date + pd.Timedelta(days=1)
        exchange = 'XTKS'

        yield (sid, df), symbol, asset_name, start_date, end_date, first_traded, auto_close_date, exchange


def metadata_frame():
    dtype = [
        ('symbol', 'object'),
        ('asset_name', 'object'),
        ('start_date', 'datetime64[ns]'),
        ('end_date', 'datetime64[ns]'),
        ('first_traded', 'datetime64[ns]'),
        ('auto_close_date', 'datetime64[ns]'),
        ('exchange', 'object'), ]
    return pd.DataFrame(np.empty(len(load_equities()), dtype=dtype))


def stooq_jp_to_bundle(interval='1d'):
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir
               ):
        metadata = metadata_frame()

        def daily_data_generator():
            return (sid_df for (sid_df, *metadata.iloc[sid_df[0]]) in data_generator())
        daily_bar_writer.write(daily_data_generator(), show_progress=True)
        
        exchange = {'exchange': 'XTKS', 'canonical_name': 'XTKS', 'country_code': 'JP'}
        exchange_df = pd.DataFrame(exchange, index = [0])
      
        asset_db_writer.write(equities=metadata.dropna(), exchanges=exchange_df)
        adjustment_writer.write(splits=pd.read_csv(custom_data_path / 'stooq_jp_splits.csv'))
    return ingest
