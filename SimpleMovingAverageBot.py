from TradingBot import *
import numpy as np

class SimpleMovingAverageBot(TradingBot):

    def __init__(self, config_file, symbol, short_window, long_window):
        super().__init__(config_file, symbol)
        self.short_window = short_window
        self.long_window = long_window
    
    def execute_strategy(self):
        df = self.raw_data.copy() 
        df['short_window'] = df[self.symbol].rolling(self.short_window).mean()
        df['long_window'] = df[self.symbol].rolling(self.long_window).mean()
        df['pred'] = np.where(df['short_window'] > df['long_window'], 1, -1)
        self.data = df.copy()

if __name__ == "__main__":
    bot = SimpleMovingAverageBot("oanda.cfg", "EUR_USD", "1min", short_window=10, long_window=100)
    bot.get_most_recent()
    bot.stream_data(bot.symbol, stop = 100)
    bot.finish_session()
