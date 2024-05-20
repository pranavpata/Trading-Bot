from TradingBot import *
import numpy as np
from sklearn.linear_model import LinearRegression

class RegressionBot(TradingBot):

    def __init__(self, config_file, symbol):
        super().__init__(config_file, symbol)
        self.linreg = LinearRegression(fit_intercept = True)
    
    def execute_strategy(self):
        df = self.raw_data.copy() 
        df['returns'] = np.log(df[self.symbol]/df[self.symbol].shift())

        df['lag'] = df.returns.shift(1)
        df.dropna(inplace = True)
        self.linreg.fit(df['lag'].to_frame(), df['returns'])
        df['pred'] = self.linreg.predict(df['lag'].to_frame())

        self.data = df.copy()

if __name__ == "__main__":
    bot = RegressionBot("oanda.cfg", "EUR_USD", "1min")
    bot.get_most_recent()
    bot.stream_data(bot.symbol, stop = 100)
    bot.finish_session()
