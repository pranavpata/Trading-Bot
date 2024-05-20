from Backtest import *

class ContrarianBacktest(Backtest):

    def __init__(self, window, symbol="EUR_USD", start_date="2019-01-01", end_date="2020-01-01", granularity="D", money=10000):
        super().__init__(symbol, start_date, end_date, granularity, money)
        self.window = window

    def test_strategy(self):
        data = self.data.copy().dropna()
        data['rolling_returns'] = data['returns'].rolling(self.window).mean()
        data.dropna(inplace = True)

        for time_index in range(len(data)-1):
            if data['rolling_returns'].iloc[time_index] <= 0: # long signal
                if self.position in [0, -1]:
                    self.go_long(time_index, amount = "all")
            elif data['rolling_returns'].iloc[time_index] > 0: # short signal
                if self.position in [0, 1]:
                    self.go_short(time_index, amount = "all")
        self.finish_backtest(time_index+1)
