from Backtest import *
from sklearn.linear_model import LinearRegression

class RegressionBacktest(Backtest):

    def __init__(self, symbol="EUR_USD", start_date="2019-01-01", end_date="2020-01-01", granularity="D", money=10000):
        super().__init__(symbol, start_date, end_date, granularity, money)

    def test_strategy(self):
        data = self.data.copy().dropna()
        data['lag'] = data.returns.shift(1)
        data.dropna(inplace = True)

        linreg = LinearRegression(fit_intercept = True)
        linreg.fit(data['lag'].to_frame(), data['returns'])
        data['pred'] = linreg.predict(data['lag'].to_frame())

        for time_index in range(len(data)-1):
            pred = np.sign(data['pred'][time_index])
            if  pred == -1: # long signal
                if self.position in [0, -1]:
                    self.go_long(time_index, amount = "all")
            elif pred == 1: # short signal
                if self.position in [0, 1]:
                    self.go_short(time_index, amount = "all")
        self.finish_backtest(time_index+1)
