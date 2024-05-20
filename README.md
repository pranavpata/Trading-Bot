# Trading Bot

This project was divided into two main steps:

## Backtesting Trading Strategies

I first created a backtesting framework that could be used with a variety of strategies. The general principles of getting/preparing data, buying/selling orders, and taking short/long positions are the same in any strategy, so I abstracted all the functionality into a base class called Backtest.py. The specific strategies are then backtested within each respective sub-class that only needs to implement the specific strategy's needs. I looked at some traditional strategies like a contrarian strategy, as well some ML-powered strategies like a strategy powered by regression.

## Creating Trading Bots

Similar to backtesting, I created a general class called TradingBot.py that contained the functionality that most trading bots would need. I then created sub-classes of trading bots that traded according to a specific strategy. These bots use the given strategy along with real-time data to make more informed trading decisions.
