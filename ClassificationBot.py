from TradingBot import *
import numpy as np
from sklearn.linear_model import LogisticRegression

class ClassificationBot(TradingBot):

    def __init__(self, config_file, symbol, lags):
        super().__init__(config_file, symbol)
        self.lags = lags
        self.logreg = LogisticRegression(max_iter=100000, multi_class="auto")
    
    def execute_strategy(self):
        df = self.raw_data.copy() 
        df['returns'] = np.log(df[self.symbol]/df[self.symbol].shift())

        df['direction'] = np.sign(df['returns'])
        lags = []
        for lag in range(1, self.lags + 1):
            lagx = f"lag{lag}"
            df[lagx] = df['returns'].shift(lag)
            lags.append(lagx)
        df.dropna(inplace = True)
        self.logreg.fit(df[lags], df['direction'])
        df['pred'] = self.logreg.predict(df[lags])

        self.data = df.copy()

if __name__ == "__main__":
    bot = ClassificationBot("oanda.cfg", "EUR_USD", "1min")
    bot.get_most_recent()
    bot.stream_data(bot.symbol, stop = 100)
    bot.finish_session()
