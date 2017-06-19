'''These code are the homework 5 and are mainly from professor Dixson's lecture '''
# backtest.py
from abc import ABCMeta, abstractmethod
class Strategy(object):
    """Strategy is an abstract base class providing an interface for
    all subsequent (inherited) trading strategies.

    The goal of a (derived) Strategy object is to output a list of signals,
    which has the form of a time series indexed pandas DataFrame.

    In this instance only a single symbol/instrument is supported."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_signals(self):
        """An implementation is required to return the DataFrame of symbols
        containing the signals to go long, short or hold (1, -1 or 0)."""
        raise NotImplementedError("Should implement generate_signals()!")


# backtest.py
class Portfolio(object):
    """An abstract base class representing a portfolio of
    positions (including both instruments and cash), determined
    on the basis of a set of signals provided by a Strategy."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_positions(self):
        """Provides the logic to determine how the portfolio
        positions are allocated on the basis of forecasting
        signals and available cash."""
        raise NotImplementedError("Should implement generate_positions()!")

    @abstractmethod
    def backtest_portfolio(self):
        """Provides the logic to generate the trading orders
        and subsequent equity curve (i.e. growth of total equity),
        as a sum of holdings and cash, and the bar-period returns
        associated with this curve based on the 'positions' DataFrame.

        Produces a portfolio object that can be examined by
        other classes/functions."""
        raise NotImplementedError("Should implement backtest_portfolio()!")


# ma_cross.py
import matplotlib.pyplot as plt
import numpy as np
import quandl
import pandas as pd

class MovingAverageCrossStrategy(Strategy):
    """
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average."""

    def __init__(self, symbol, bars, short_window=100, long_window=400):
        self.symbol = symbol
        self.bars = bars

        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Returns the DataFrame of symbols containing the signals
        to go long, short or hold (1, -1 or 0)."""
        signals = pd.DataFrame(index=self.bars.index)
        signals['signal'] = 0.0

        # Create the set of short and long simple moving averages over the
        # respective periods
        signals['short_mavg'] = pd.rolling_mean(bars['Open'], self.short_window, min_periods=1)
        signals['long_mavg'] = pd.rolling_mean(bars['Open'], self.long_window, min_periods=1)

        # Create a 'signal' (invested or not invested) when the short moving average crosses the long
        # moving average, but only for the period greater than the shortest moving average window
        signals['signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:]
                                                         > signals['long_mavg'][self.short_window:], 1.0, 0.0)

        signals['positions'] = signals['signal'].diff()
        return signals


# ma_cross.py
class MarketOnClosePortfolio(Portfolio):
    """Encapsulates the notion of a portfolio of positions based
    on a set of signals as provided by a Strategy.

    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio."""

    def __init__(self, symbol, bars, r_benchmark, signals, initial_capital=100000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()
        self.r_benckmark = r_benchmark
        self.rp = []

    def generate_positions(self):
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions[self.symbol] = 100 * signals['signal']  # This strategy buys 100 shares
        return positions

    def backtest_portfolio(self):
        bars_back_port = pd.DataFrame(index=self.bars.index).fillna(0.0)
        bars_back_port[self.symbol] = self.bars['Close']
        portfolio = self.positions * bars_back_port # holding
        pos_diff = self.positions.diff() # buy or sell

        '''
         # primary method without preventing low cash condition
        portfolio['holdings'] = (self.positions * bars_back_port).sum(axis=1)
        portfolio['cash'] = self.initial_capital - (pos_diff * bars_back_port).sum(axis=1).cumsum()

        '''#preventing low cash condition
        #####################################################
        # when cash is below 25000
        # compute and judgement elements one by one each time
        portfolio['holdings'] = (0.)
        portfolio['cash'] = (0.)
        portfolio['holdings'][0] = self.positions[self.symbol][0] * bars_back_port[self.symbol][0]
        portfolio['cash'][0] = self.initial_capital

        for i in range(1, len(bars_back_port[self.symbol])):
            portfolio['holdings'][i] = self.positions[self.symbol][i] * bars_back_port[self.symbol][i]
            portfolio['cash'][i] = portfolio['cash'][i - 1] - (self.positions[self.symbol][i] -
                                                               self.positions[self.symbol][i - 1]) * \
                                                              bars_back_port[self.symbol][i]
            if portfolio['cash'][i] <= 25000.:  # check whether cash amount falls below $25,000.
                try:
                    if self.positions[self.symbol][i + 1] == 1.:
                        self.positions[self.symbol][i + 1] = 0.0
                except IndexError:
                    print("Jsut out of index, the code is right")
        ###########################################################

        portfolio['positions'] = self.positions
        portfolio['signal'] = self.signals['signal']
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        self.rp = portfolio['returns']
        return portfolio

    def sharpe_ratio(self):
        excess_return = self.r_benckmark['Close'] - self.rp  # r_portfolio-rb
        sharpe_ratio = excess_return.mean() / excess_return.std()
        return sharpe_ratio


if __name__ == '__main__':
    # Obtain daily bars of AAPL from Yahoo Finance for the period
    # 1st Jan 2010 to 1st Jan 2015 - This is an example from ZipLine
    symbol = 'TWTR'
    quandl.ApiConfig.api_key = '71Ku6zWzNeHExTydVgst'
    bars = quandl.get("YAHOO/%s" % symbol, collapse="daily", start_date="2010-1-1", end_date="2015-11-8")

    quandl.ApiConfig.api_key = '71Ku6zWzNeHExTydVgst'
    r_benchmark = quandl.get("YAHOO/INDEX_GSPC", collapse="daily", start_date="2010-1-1", end_date="2015-11-8",
                             transform="rdiff")

    # Create a Moving Average Cross Strategy instance with a short moving
    # draw different short windows and long windows
    j=0; best_signals=[]
    for l in range(100, 450, 50): # increment of long window size
        i=0
        for s in range(5, 55, 5): # increment of short window size
            mac = MovingAverageCrossStrategy(symbol, bars, short_window=s, long_window=l)
            signals = mac.generate_signals()
            # Create a portfolio of symbol company, with $100,000 initial capital
            portfolio = MarketOnClosePortfolio(symbol, bars, r_benchmark, signals, 100000.0)
            positions = portfolio.generate_positions()
            # print positions.head().tail()
            returns = portfolio.backtest_portfolio()
            sharpe_ratio = portfolio.sharpe_ratio()
            best_signals.append([sharpe_ratio, s, l])
            print(sharpe_ratio, 'sharpe ratio')

            # Plot two charts to assess trades and equity curve
            fig = plt.figure()
            fig.set_size_inches(18.5, 10.5)
            fig.patch.set_facecolor('white')  # Set the outer colour to white
            plt.title("sharpe ratio is %s, short window and long window are %s and %s" % (sharpe_ratio, s, l))
            ax1 = fig.add_subplot(211, ylabel='Price in $')

            # Plot the AAPL closing price overlaid with the moving averages
            bars['Open'].plot(ax=ax1, color='r', lw=2.)
            signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)  # selling signal long is above short line

            # Plot the "buy" trades against symbol company
            ax1.plot(signals.ix[signals.positions == 1.0].index,
                     signals.short_mavg[signals.positions == 1.0],
                     '^', markersize=10, color='m')

            # Plot the "sell" trades against symbol company
            ax1.plot(signals.ix[signals.positions == -1.0].index,
                     signals.short_mavg[signals.positions == -1.0],
                     'v', markersize=10, color='k')

            # Plot the equity curve in dollars
            ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
            returns['total'].plot(ax=ax2, lw=2.)

            # Plot the "buy" and "sell" trades against the equity curve
            ax2.plot(returns.ix[signals.positions == 1.0].index,
                     returns.total[signals.positions == 1.0],
                     '^', markersize=10, color='m')
            ax2.plot(returns.ix[signals.positions == -1.0].index,
                     returns.total[signals.positions == -1.0],
                     'v', markersize=10, color='k')
            # Plot the figure
            fig.show()
            fig.savefig("ma_cross with %s short window, %s long window.png" % (s, l), dpi=100)
            i += 1
        j += 1
    m = max(np.array(best_signals)[:, 0])
    final_position = [i for i, x in enumerate(np.array(best_signals)[:, 0]) if x == m]
    final_result = best_signals[final_position[0]]
    print("The best sharp ratio is %s, when short windowsize and short window size are %s and %s"
          % (final_result[0], final_result[1],final_result[2]))
# end of the code