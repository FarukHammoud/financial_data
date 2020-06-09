import numpy as np
import matplotlib.pyplot as plt

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

YEARS = share.PERIOD_TYPE_YEAR
HOURS = share.FREQUENCY_TYPE_HOUR
DAYS = share.FREQUENCY_TYPE_DAY
WEEKS = share.FREQUENCY_TYPE_WEEK
MONTHS = share.PERIOD_TYPE_MONTH
YEAR = share.PERIOD_TYPE_YEAR
HOUR = share.FREQUENCY_TYPE_HOUR
DAY = share.FREQUENCY_TYPE_DAY
WEEK = share.FREQUENCY_TYPE_WEEK
MONTH = share.PERIOD_TYPE_MONTH

class FinancialData:

    def __init__(self,company_code):

        self.my_share = share.Share(company_code)

        self.timestamp = []
        self.open = []
        self.close = []
        self.high = []
        self.low = []
        self.volume = []
    
    def get_data(self,period,period_unit,frequency,frequency_unit):
        
        # Try to get data
        sd = None

        try:

            sd = self.my_share.get_historical(period_unit,period,frequency_unit,frequency)
            self.timestamp = np.array(sd['timestamp'])
            self.open = np.array(sd['open'])
            self.close = np.array(sd['close'])
            self.high = np.array(sd['high'])
            self.low = np.array(sd['low'])
            self.volume = np.array(sd['volume'])

        except YahooFinanceError as e:

            print('[FAILED] ',e.message)
            return False
        
        print('[SUCCESS] Data was successefully obtained.')
        return True

    def verify_data(self):

        mask = np.logical_and.reduce((self.timestamp!=None,self.open!=None,self.close!=None,self.high!=None,self.low!=None,self.volume!=None))
        
        self.timestamp = self.timestamp[mask].astype('float64')
        self.open = self.open[mask].astype('float64')
        self.close = self.close[mask].astype('float64')
        self.high = self.high[mask].astype('float64')
        self.low = self.low[mask].astype('float64')
        self.volume = self.volume[mask].astype('float64')

    def log_yield(self):

        return np.log(self.close[1:]/self.close[0:-1])

    def show_volume(self):

        plt.plot(self.volume)
        plt.show()

def plot(data):
    plt.plot(data)
    plt.show()

