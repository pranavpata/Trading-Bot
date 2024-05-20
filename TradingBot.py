import pandas as pd
import tpqoa
from datetime import datetime, timedelta

class TradingBot(tpqoa.tpqoa):

    def __init__(self, config_file, symbol, granularity="1min", num_units=10000):
        super.__init__(config_file)
        self.symbol = symbol
        self.position = 0
        self.granularity = granularity
        self.units = num_units
        self.last_time = None
        self.raw_data = None
        self.tick_data = None
    
    def get_most_recent(self, days=5):
        now = datetime.utcnow()
        now = now - timedelta(microseconds=now.microsecond)
        past = now - timedelta(days=days)
        bids = self.get_history(instrument=self.symbol, start=past, end=now,
                                granularity=self.granularity, price="B")
        asks = self.get_history(instrument=self.symbol, start=past, end=now,
                                granularity=self.granularity, price="A")
        df = pd.DataFrame(index=bids.index)
        df[self.symbol] = (bids['c'] + asks['c']) / 2
        df[self.symbol].dropna()
        df = df.resample(self.granularity, label = "right").last().dropna().iloc[:-1]
        self.raw_data = df.copy()
        self.last_time = self.raw_data.index[-1]
    
    def on_success(self, time, bid, ask): # called when real-time data is streamed
        recent_tick = pd.to_datetime(time)
        df = pd.DataFrame({self.symbol:(ask + bid)/2}, 
                          index = [recent_tick])
        self.tick_data = self.tick_data.append(df)
        
        if recent_tick - self.last_time > self.granularity:
            self.resample()
            self.execute_strategy()
            self.execute_trades()
    
    def resample(self):
        self.raw_data = self.raw_data.append(self.tick_data.resample(self.granularity, label="right").last().ffill().iloc[:-1])
        self.tick_data = self.tick_data.iloc[-1:]
        self.last_time = self.raw_data.index[-1]
    
    # find self.data['pred']
    def execute_strategy(self):
        raise NotImplementedError
    
    def execute_trades(self):
        if self.data['pred'].iloc[-1] == 1: # go long
            if self.position == -1:
                self.create_order(self.symbol, self.units * 2) 
            elif self.position == 0:
                self.create_order(self.symbol, self.units)
            self.position = 1
        elif self.data['pred'].iloc[-1] == -1: # go short
            if self.position == 1:
                self.create_order(self.symbol, -self.units * 2)
            elif self.position == 0:
                self.create_order(self.symbol, -self.units)
            self.position = -1
        elif self.data['pred'].iloc[-1] == 0: # go neutral
            if self.position == -1:
                self.create_order(self.symbol, self.units) 
            elif self.position == 1:
                self.create_order(self.symbol, -self.units) 
            self.position = 0
    
    def finish_session(self):
        if self.position != 0: # finish neutral
            self.create_order(self.symbol, units=-self.position * self.units) 
            self.position = 0
        print("Ending Session.")
