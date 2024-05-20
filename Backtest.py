import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tpqoa

class Backtest():

    def __init__(self, symbol="EUR_USD", start_date="2019-01-01", end_date="2020-01-01", granularity="D", money=10000):
        self.symbol = symbol
        self.starting_balance = money
        self.cur_balance = money
        self.num_units = 0
        self.get_data(start_date, end_date, granularity)
        self.prepare_data()
        self.position = 0

    def get_data(self, start_date, end_date, granularity):
        print(f"Getting data from {start_date} to {end_date} with granularity '{granularity}'")
        api = tpqoa.tpqoa("/Users/pranavpata/Desktop/Projects/Trading Bot/oanda.cfg")
        bids = api.get_history(instrument=self.symbol, start=start_date, end=end_date, granularity=granularity, price="B")
        asks = api.get_history(instrument=self.symbol, start=start_date, end=end_date, granularity=granularity, price="A")
        self.data = pd.DataFrame(index=bids.index)
        self.data['price'] = (bids['c'] + asks['c']) / 2
        self.data['half-spread'] = self.data['price'] - bids['c']
    
    def prepare_data(self):
        self.data['returns'] = np.log(self.data['price'] / self.data['price'].shift(1))
        self.data['cumulative_returns'] = self.data['returns'].cumsum().apply(np.exp)

    def buy_order(self, time_index, units=None, amount=None):
        price = self.data['price'][time_index] + self.data['half-spread'][time_index]
        if amount is not None:
            units = int(amount / price)
        self.cur_balance -= units * price
        self.num_units += units
        print(f"Buying {units} units for {price} at time {self.data.index[time_index]}")
    
    def sell_order(self, time_index, units=None, amount=None):
        price = self.data['price'][time_index] - self.data['half-spread'][time_index]
        if amount is not None:
            units = int(amount / price)
        self.cur_balance += units * price
        self.num_units -= units
        print(f"Selling {units} units for {price} at time {self.data.index[time_index]}")
    
    def go_long(self, time_index, units=None, amount=None):
        if self.position == -1:
            self.buy_order(time_index, units=-self.num_units) # if short position, go neutral first
        if units:
            self.buy_order(time_index, units=units)
        elif amount:
            if amount == "all":
                amount = self.cur_balance
            self.buy_order(time_index, amount=amount) # go long
        self.position = 1

    def go_short(self, time_index, units=None, amount=None):
        if self.position == 1:
            self.sell_order(time_index, units=self.num_units) # if long position, go neutral first
        if units:
            self.sell_order(time_index, units=units)
        elif amount:
            if amount == "all":
                amount = self.cur_balance
            self.sell_order(time_index, amount=amount) # go short
        self.position = -1

    def plot_data(self, column=None):
        plt.plot(self.data.index, self.data['cumulative_returns'])
        if column:
            plt.plot(self.data.index, self.data[column], color='red')
        plt.title(self.symbol)
        plt.show()

    def test_strategy(self):
        raise NotImplementedError
    
    def finish_backtest(self, time_index):
        price = self.data['price'][time_index] - self.data['half-spread'][time_index]
        self.cur_balance += self.num_units * price
        perf = (self.cur_balance - self.starting_balance) / self.starting_balance * 100
        print(f"{perf}% returns with this strategy.")


