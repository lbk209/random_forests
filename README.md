## Long-short signals for Japanese stocks with LightGBM

This repo elaborates [Random Forests - A Long-Short Strategy for Japanese Stocks](https://github.com/stefan-jansen/machine-learning-for-trading/tree/master/11_decision_trees_random_forests) in Machine Learning for Algorithmic Trading by Stefan Jansen. It builds a long-short trading strategy that uses a Random Forest ensemble to generate profitable signals for large-cap Japanese equities over the last three years. It will sources and prepares the stock price data, tunes the hyperparameters of a Random Forest model, and backtests trading rules based on the models’ signals.

- The notebook [create_stooq_data](00_create_stooq_data.ipynb) downloads historical prices for Japanese stocks from STOOQ.

#### [create_stooq_data](00_create_stooq_data.ipynb)

#### [japanese_equity_features](01_japanese_equity_features.ipynb)
#### [random_forest_return_signals](02_random_forest_return_signals.ipynb)
#### [alphalens_signals_quality](03_alphalens_signals_quality.ipynb)
#### [backtesting_with_zipline](04_backtesting_with_zipline.ipynb)
#### [trading](05_trading.ipynb)

## Code Example: Long-short signals for Japanese stocks with LightGBM

In [Chapter 9](../09, we used cointegration tests to identify pairs of stocks with a long-term equilibrium relationship in the form of a common trend to which their prices revert. 

In this chapter, we will use the predictions of a machine learning model to identify assets that are likely to go up or down so that we can enter market-neutral long and short positions accordingly. The approach is similar to our initial trading strategy that used linear regression in Chapter 7, Linear Models, and Chapter 8, Strategy Workflow: End-to-End Algo Trading.

Instead of the scikit-learn random forest implementation, we will use the [LightGBM](https://lightgbm.readthedocs.io/en/latest/) package that has been primarily designed for gradient boosting. One of several advantages is LightGBM’s ability to efficiently encode categorical variables as numeric features rather than using one-hot dummy encoding (Fisher 1958). We’ll provide a more detailed introduction in the next chapter, but the code samples should be easy to follow as the logic is similar to the scikit-learn version.








## Code Example: Long-short signals for Japanese stocks with LightGBM

In [Chapter 9](../09, we used cointegration tests to identify pairs of stocks with a long-term equilibrium relationship in the form of a common trend to which their prices revert. 

In this chapter, we will use the predictions of a machine learning model to identify assets that are likely to go up or down so that we can enter market-neutral long and short positions accordingly. The approach is similar to our initial trading strategy that used linear regression in Chapter 7, Linear Models, and Chapter 8, Strategy Workflow: End-to-End Algo Trading.

Instead of the scikit-learn random forest implementation, we will use the [LightGBM](https://lightgbm.readthedocs.io/en/latest/) package that has been primarily designed for gradient boosting. One of several advantages is LightGBM’s ability to efficiently encode categorical variables as numeric features rather than using one-hot dummy encoding (Fisher 1958). We’ll provide a more detailed introduction in the next chapter, but the code samples should be easy to follow as the logic is similar to the scikit-learn version.

### Custom Zipline Bundle

- The directory [custom_bundle](00_custom_bundle) contains instruction on how to obtain the data and create a custom Zipline bundle.

### Feature Engineering

- The notebook [japanese_equity_features](04_japanese_equity_features.ipynb) shows how to generate model features.

### LightGBM Random Forest Model Tuning

- The notebook [random_forest_return_signals](05_random_forest_return_signals.ipynb) contains the code to train and tune a [LightGBM](https://lightgbm.readthedocs.io/en/latest/) random forest model

### Signal Evaluation with Alphalens

- The notebook [alphalens_signals_quality](06_alphalens_signals_quality.ipynb) shows how to evaluate the model predictions using [Alphalens](https://github.com/quantopian/alphalens).

### Backtest with Zipline

- The notebook [backtesting_with_zipline](07_backtesting_with_zipline.ipynb) evaluates the model predictions using a long-short strategy simulated using [Zipline](https://zipline.ml4trading.io/).

 
