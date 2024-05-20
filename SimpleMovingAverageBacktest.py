from Backtest import *

class SimpleMovingAverageBacktest(Backtest):

    def __init__(self, short_window, long_window, symbol="EUR_USD", start_date="2019-01-01", end_date="2020-01-01", granularity="D", money=10000):
        super().__init__(symbol, start_date, end_date, granularity, money)
        self.short_window = short_window
        self.long_window = long_window
    
    def test_strategy(self):
        data = self.data.copy().dropna()
        data['short_moving_average'] = data['price'].rolling(self.short_window).mean()
        data['long_moving_average'] = data['price'].rolling(self.long_window).mean()
        data.dropna(inplace = True)

        for time_index in range(len(data)-1):
            if data["short_moving_average"].iloc[time_index] > data["long_moving_average"].iloc[time_index]: # long signal
                if self.position in [0, -1]:
                    self.go_long(time_index, amount = "all")
            elif data["short_moving_average"].iloc[time_index] < data["long_moving_average"].iloc[time_index]: # short signal
                if self.position in [0, 1]:
                    self.go_short(time_index, amount = "all")
        self.finish_backtest(time_index+1)
