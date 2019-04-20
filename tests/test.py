# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mpl_finance_ext as mfe


# The following indicator functions are copied (but modified) from
# the pandas-technical-indicators repository by Crypto-toolbox:
# https://github.com/Crypto-toolbox/pandas-technical-indicators


def relative_strength_index(df, n):
    """Calculate Relative Strength Index(RSI) for given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = df.index[0]
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = float(df.loc[i + 1, 'High']) - float(df.loc[i, 'High'])
        DoMove = float(df.loc[i, 'Low']) - float(df.loc[i + 1, 'Low'])
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)

    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())

    # rsi = pd.Series(PosDI / (PosDI + NegDI), name='RSI_' + str(n))
    rsi = pd.DataFrame(PosDI / (PosDI + NegDI), columns=['RSI_' + str(n)])
    rsi = rsi.set_index(df.index)
    df = df.join(rsi)
    return df


def bollinger_bands(df, n, std):
    """
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """

    ave = df['Close'].rolling(window=n, center=False).mean()
    sd = df['Close'].rolling(window=n, center=False).std()
    upband = pd.Series(ave + (sd * std), name='bband_upper_' + str(n))
    dnband = pd.Series(ave - (sd * std), name='bband_Lower_' + str(n))
    ave = pd.Series(ave, name='bband_ave_' + str(n))

    df = df.join(pd.concat([upband, dnband, ave], axis=1))
    return df


def moving_average(df, n):
    """Calculate the moving average for the given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
    df = df.join(MA)
    return df


def exponential_moving_average(df, n):
    """
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    EMA = pd.Series(df['Close'].ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
    df = df.join(EMA)
    return df


def test_1(df):
    # Example 1)
    # In this example we plot the candlestick chart plus
    # some indicators and rsi on a seperate axis:

    # Structure: [(signal, index, price), ... ].
    # Signal can be 'BUY' or 'SELL'
    signals = [
        ('BUY', 12, 0.69), ('SELL', 27, 0.7028),
        ('BUY', 56, 0.6563), ('SELL', 81, 0.6854),
        ('BUY', 106, 0.665), ('SELL', 165, 0.640),
        ('BUY', 183, 0.66), ('SELL', 202, 0.7063),
    ]

    # Create fig
    fig, _ = plt.subplots(facecolor=mfe.cb)

    # Create first axis
    ax0 = plt.subplot2grid(
        (8, 4), (0, 0), rowspan=4, colspan=4, facecolor=mfe.cb)

    # Add content to the first axis.
    mfe.plot_candlestick(
        fig=fig,
        axis=ax0,
        data=df,
        title='BTC_XRP_5min',
        signals=signals,
        columns=[
            'bband_upper_20', 'bband_Lower_20',
            'MA_36', 'EMA_8'
        ],
        disable_xticks=False,
    )

    # Just to show what is possible
    # mfe.plot_volume(
    #     twin_axis=ax0,
    #     fig=fig,
    #     data=df
    # )

    # Create second axis
    ax1 = plt.subplot2grid(
        (8, 4), (4, 0), rowspan=4, colspan=4, sharex=ax0,
        facecolor=mfe.cb)

    # Add content to the second axis.
    # 1) RSI 14
    mfe.plot(
        axis=ax1,
        fig=fig,
        data=df,
        name='RSI 2',
        columns=['RSI_14'],
        hlines=[
            {'index': 0.8, 'color': 'red'},
            {'index': 0.2, 'color': 'green'}
        ]
    )

    plt.show()


def test_2(df):

    # One manually picked candlestick pattern
    patterns = [
        ['inverted_hammer', 12, 13]
    ]
    # 'bu_' infornt of the name paints it green, 'be_' red
    # Example: 'bu_inverted_hammer'

    # And we add some Support and Resistance lines
    lines = [
        {'start': [3.5, 0.711], 'stop': [20, 0.711]},
        {'start': [10, 0.688], 'stop': [20, 0.688]}
    ]

    mfe.plot_candlestick(
        data=df,
        name='BTC_XRP_5min',
        cs_patterns=patterns,
        columns=[
            'bband_upper_20', 'bband_Lower_20',
            'MA_36', 'EMA_8'
        ],
        draw_verticals=False,
        lines=lines,
        # save='BTC_XRP_5min_candlestick.png'
    )


def test_3():
    # Read and prepare data
    df = pd.read_csv('stocks.csv', index_col=False).tail(1000)
    date = df['Date']
    df = df.drop(['Date'], axis=1)

    # List of vlines:
    # [index_1, index_2, ...] or
    # [{'index':..., 'color':..., 'linewidth':..., 'alpha':..., 'linestyle':...,}, ...]
    vlines = [50, 150]

    # List of hlines:
    # [index_1, index_2, ...] or
    # [{'index':..., 'color':..., 'linewidth':..., 'alpha':..., 'linestyle':...,}, ...]
    hlines = [
        {'index': 3.5, 'color': 'red', 'linewidth': 0.8, 'alpha': 0.8, 'linestyle': ':'},
        {'index': 4, 'color': 'red', 'linewidth': 0.8, 'alpha': 0.8, 'linestyle': ':'}
    ]

    # List of lines
    # [{'start': [x, y], 'stop': [x, y], 'color':..., 'linewidth':..., 'alpha':..., 'linestyle':...,}, ...]
    lines=[
        {'start': [50, 3.5], 'stop': [150, 4]},
        {'start': [50, 4], 'stop': [150, 3.5]}
    ]

    mfe.plot(df / df.iloc[0], columns=['AMZN', 'AMD', 'GOOGL'],
        xticks=date,
        gradient_fill=True,
        xlabel='Date',
        ylabel='Price',
        title='Stocks',
        vspans=[[50, 150]],    # List of vspans: [[start index, end index], ...]
        hspans=[[3.5, 4]],     # List of hspans: [[start index, end index], ...]
        vlines=vlines,
        hlines=hlines,
        lines=lines
    )


if __name__ == "__main__":
    # Load dataset -----------------------------------------------
    df = pd.read_csv('BTC_XRP_5min.csv', index_col=0)

    # Calculate indicators ---------------------------------------
    df = relative_strength_index(df=df, n=14)
    df = bollinger_bands(df=df, n=20, std=4)
    df = exponential_moving_average(df=df, n=8)
    df = moving_average(df=df, n=36)

    # Examples ---------------------------------------------------
    test_1(df=df.head(250))

    test_2(df=df.head(20))

    test_3()
