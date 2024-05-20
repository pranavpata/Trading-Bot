from TradingBot import *
import numpy as np

class ContrarianBot(TradingBot):

    def __init__(self, config_file, symbol, window):
        super().__init__(config_file, symbol)
        self.window = window
    
    def execute_strategy(self):
        df = self.raw_data.copy() 
        df['returns'] = np.log(df[self.symbol]/df[self.symbol].shift())
        df['pred'] = -np.sign(df['returns'].rolling(self.window).mean())     
        self.data = df.copy()

if __name__ == "__main__":
    bot = ContrarianBot("oanda.cfg", "EUR_USD", "1min", window=10)
    bot.get_most_recent()
    bot.stream_data(bot.symbol, stop = 100)
    bot.finish_session()
