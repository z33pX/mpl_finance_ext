# mpl_finance_ext

mpl_finance_ext provides functions to plot and evaluate finance data. 
It supports mainly three functions:

* Candlestick chart -- `plot_candlestick()`
* Filled OHLC chart  -- `plot_filled_ohlc()`
* Plot other stuff -- `plot()`

For every function signal evaluation is possible. That means when you have buy and sell signals
provided by an algotrading algorithm for example you can plot them in the graph to get a visal picture.
The yield of buy and sell will be calculated and is explained in the graph as well. All this will be shown in
a few examples below. All following code is provided in `examples.py`.

First we load the data and calculate some example indicators:

```
# Load dataset
data = pd.read_csv('BTC_XRP_5min.csv', index_col=0)

# Calculate indicators
data = relative_strength_index(df=data, n=14)
data = bollinger_bands(df=data, n=20, std=4)
data = exponential_moving_average(df=data, n=8)
data = moving_average(df=data, n=36)

# Now we set some signals
# Structure: [(signal, index, price), ... ].
# Signal can be 'BUY' or 'SELL'

# Some manually picked examples
signals = [
    ('BUY', 12, 0.69), ('SELL', 27, 0.7028),
    ('BUY', 56, 0.6563), ('SELL', 81, 0.6854),
    ('BUY', 106, 0.665), ('SELL', 165, 0.640),
    ('BUY', 183, 0.66), ('SELL', 202, 0.7063),
]
```

Plot candlestick charts
-
After we prepared the data we create a figure and an axis and plot 
the candlesticks plus some indicators in one chart and the rsi 
on a seperate axis:

```
# Create fig
fig, _ = plt.subplots(facecolor=mfe.background_color)

# Create first axis
ax0 = plt.subplot2grid(
    (8, 4), (0, 0),
    rowspan=4, colspan=4,
    facecolor=mfe.background_color
)

# Add content to the first axis.
# 1) Candlestick chart
# 2) Bollinger Bands 20
# 3) Moving Average 36
# 4) Exponential Moving Average
_, _ = mfe.plot_candlestick(
    fig=fig,
    axis=ax0,
    data=data,
    name='BTC_XRP_5min',
    signals=signals,
    plot_columns=[
        'bband_upper_20', 'bband_lower_20',
        'MA_36', 'EMA_8'
    ],
    draw_verticals=False,
    draw_evaluation=True,
    evaluation='rectangle',
    disable_x_ticks=True,
```

Now we plot the RSI_14 data in a separate chart with the `plot()` function:

```
# Create second axis
ax1 = plt.subplot2grid(
    (8, 4), (4, 0),
    rowspan=4, colspan=4, sharex=ax0,
    facecolor=mfe.background_color
)

# Add content to the second axis.
# 1) RSI 14
mfe.plot(
    data=data,
    name='Chart 2',
    plot_columns=['RSI_14'],
    axis=ax1,
    fig=fig,
    xhline_red=0.8,
    xhline_green=0.2,
)

plt.show()

```

The result looks like this:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_01.png)

For further explanations for the parameters please look into the function description. 


Plot filled OHLC chart
-
It works exactly like the `plot_candlestick()`function.

```
fig, ax = mfe.plot_filled_ohlc(
    data=data,
    name='BTC_XRP_5min',
    signals=signals,
    plot_columns=[
        'bband_upper_20', 'bband_lower_20',
        'MA_36', 'EMA_8'
    ],
    draw_verticals=False,
    draw_evaluation=True,
    evaluation='rectangle',
    # save='BTC_XRP_5min_filled.png'
    )
```

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_02.png)
