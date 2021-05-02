## Long-short signals for Japanese stocks with LightGBM

These notebooks elaborate the code example [Random Forests - A Long-Short Strategy for Japanese Stocks](https://github.com/stefan-jansen/machine-learning-for-trading/tree/master/11_decision_trees_random_forests) in Machine Learning for Algorithmic Trading by Stefan Jansen, which builds a long-short trading strategy that uses a Random Forest ensemble to generate profitable signals for Japanese equities. The example shows how to source and prepare the stock price data, tune the hyperparameters of a Random Forest model, and backtest trading rules based on the models’ signals. The modification to the example are as follows:

- The notebook [create_stooq_data](00_create_stooq_data.ipynb) downloads historical prices for Japanese stocks from STOOQ. It seems that the folder struture of the donwloaded data makes the notebook freeze, which can be prevented by deleting the folder after extracing price history and metadata. Most of data will be stored in csv format as hdf format in the example does not work in google cloud platform.

- [japanese_equity_features](01_japanese_equity_features.ipynb) generates model features such as technical indicators. Technical indicators are calculated by using the package from [Quantopian](https://anaconda.org/quantopian/ta-lib).

- [random_forest_return_signals](02_random_forest_return_signals.ipynb) contains the code to train and tune a LightGBM random forest model. The cross-validation results are saved during iterations as the cross-validation of the random forest takes time. The results are saved in pickle format instead of hdf.

- [alphalens_signals_quality](03_alphalens_signals_quality.ipynb) shows how to evaluate the model predictions using Alphalens.

- [backtesting_with_zipline](04_backtesting_with_zipline.ipynb) evaluates the model predictions using a long-short strategy simulated using Zipline. The notebook contains the procedure how to obtain the data and create a custom Zipline bundle. The scripts for custom bundle in zipline folder are modified from original ones. The notebook uses [zipline](https://github.com/stefan-jansen/zipline-reloaded) package by Stefan Jansen. A few lines of pyfolio codes are modified to address some errors. The round_trips option of create_full_tear_sheet dose not work.

- [trading](05_trading.ipynb) basically combines the two notebooks [random_forest_return_signals](02_random_forest_return_signals.ipynb) and [backtesting_with_zipline](04_backtesting_with_zipline.ipynb), making return prediction and long-short amount for new date by using the LightGBM random forest model and Zipline.


