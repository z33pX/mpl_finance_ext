# mpl_finance_ext

mpl_finance_ext provides simple functions to plot and evaluate algorithms for trading.
It supports mainly these functions:

* Candlestick chart -- `plot_candlestick()`
* Plot lines -- `plot()`
* Plot voume -- `plot_volume()`

For `plot_candlestick()` signal evaluation is possible. 
That means when you have buy and sell signals provided by an trading algorithm you can visualize them.
The return for each trade is plotted the graph as well. Look at the examples below (Find the code in tests/test.py).

We start by loading data and calculate some example indicators:

```
if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv('BTC_XRP_5min.csv', index_col=0)

    # Calculate indicators
    df = relative_strength_index(df=df, n=14)
    df = bollinger_bands(df=df, n=20, std=4)
    df = exponential_moving_average(df=df, n=8)
    df = moving_average(df=df, n=36)

    # Start tests
    test_1(df=df)

    test_2(df=df.head(20))

    test_3()
```

Plot candlestick charts (test_1)
-
After we prepared data we create a figure and an axis we plot 
candlesticks + signals and indicators on the first axis and the rsi 
on a second one.

```
# Prepare some signals
# Structure: [(signal, index, price), ... ].
# signal can be either 'BUY' or 'SELL'
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
```

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_1.png)

For further explanations for the parameters please look into the function descriptions. 

Candlestick pattern evaluation (test_2)
-

To plot a list of candlestick patterns just set the parameter `cs_patterns` 
to a valid list of patterns like. Structure of the list: `[ ... ,['pattern_name', start_index, stop_index], ... ]`

```
# One manually picked candlestick pattern:
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
```

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_2.png)

Plot (test_3)
-

In this example we plot stock data. Additionally we'll see what functions else are available

```
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
```

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_3.png)

Change colors
-
Change colors by edeting the config file:

```
{
  "colors": {
    "labels": "#bcbdbe",
    "background": "#283136",
    "red": "#db206c",
    "green": "#69a431",
    "sets": ["#ffb93b", "#ff32f7", "#69a431", "#c17113", "#0d8382"],
    "grid": "#666666",
    "yaxis_labels": "#d3d3d3",
    "xaxis_labels": "#d3d3d3",
    "yaxis_params": "#d3d3d3",
    "xaxis_params": "#d3d3d3",
    "main_spine": "#666666",
    "price_flag": "#283136",
    "signal_eval_label": "#bcbdbe"

  }
}
```
