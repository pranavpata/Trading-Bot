from Backtest import *
from sklearn.linear_model import LogisticRegression

class ClassificationBacktest(Backtest):

    def __init__(self, lags, symbol="EUR_USD", start_date="2019-01-01", end_date="2020-01-01", granularity="D", money=10000):
        super().__init__(symbol, start_date, end_date, granularity, money)
        self.lags = lags

    def test_strategy(self):
        data = self.data.copy().dropna()
        data['direction'] = np.sign(data['returns'])
        lags = []
        for lag in range(1, self.lags + 1):
            lagx = f"lag{lag}"
            data[lagx] = data['returns'].shift(lag)
            lags.append(lagx)
        data.dropna(inplace = True)

        logreg = LogisticRegression(max_iter=100000, multi_class="auto")
        logreg.fit(data[lags], data['direction'])
        data['pred'] = logreg.predict(data[lags])

        for time_index in range(len(data)-1):
            pred = data['pred'][time_index]
            if  pred == 1: # long signal
                if self.position in [0, -1]:
                    self.go_long(time_index, amount = "all")
            elif pred == -1: # short signal
                if self.position in [0, 1]:
                    self.go_short(time_index, amount = "all")
        self.finish_backtest(time_index+1)
