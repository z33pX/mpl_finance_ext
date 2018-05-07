# mpl_finance_ext

mpl_finance_ext provides functions to plot and evaluate finance data. 
It supports mainly fife functions:

* Candlestick chart -- `plot_candlestick()`
* Filled OHLC chart  -- `plot_filled_ohlc()`
* Plot other stuff -- `plot()`
* Plot histogram from dict -- `hist_from_dict()`
* Plot bar chart from dict -- `bars_from_dict()`

For `plot_candlestick()` and `plot_filled_ohlc()` signal evaluation is possible. 
That means when you have buy and sell signals provided by an algotrading algorithm 
for example you can plot them in the graph to get a visal picture (same for candlestick patterns).
The yield of buy and sell will be calculated and is shown in the graph as well. All this will be shown in
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

# Some manually picked candlestick pattern
patterns = [
    ['inverted_hammer', 12, 13]
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

Now we plot the RSI_14 data on a separate axis with the `plot()` function:

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


Plot filled OHLC charts
-
`plot_filled_ohlc()` works exactly like `plot_candlestick()`.

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

Signal evaluation
-

As mentioned in earlier examples the signal evaluation can be activated
by defining a list of signals and set the parameter `signals=signals` of
`plot_filled_ohlc()` or `plot_candlestick()`:

```
signals = [
    ('BUY', 12, 0.69), ('SELL', 27, 0.7028),
    ('BUY', 56, 0.6563), ('SELL', 81, 0.6854),
    ('BUY', 106, 0.665), ('SELL', 165, 0.640),
    ('BUY', 183, 0.66), ('SELL', 202, 0.7063),
]
```
Structure of the list: `[ ..., (signal, index, price), ... ]`. 
Signals can be either `'BUY'` or `'SELL'`.

In previous examples you can see that the signals are visualised in form of rectangles.
Instead of rectangles you can activate arrows with `evaluation='arrow_1'`.
It will look like this:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_03.png)

Candlestick pattern evaluation
-

To plot a list of candlestick patterns just set the parameter `cs_patterns=cs_patterns` 
to a valid list of patterns like:

```
patterns = [
    ['inverted_hammer', 12, 13]
]
```

Structure of the list: `[ ... ,['pattern_name', start_index, stop_index], ... ]`

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_04.png)

Bar and histogram charts
-

As shown in example 4 in `examples.py` a histogram will be created with
```
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
    
mfe.hist_from_dict(
    fig=fig,
    axis=ax2,
    data_dict=x,
    bins=50,
    density=1,
    xlabel='Returns',
    ylabel='Probability density'
)
```
and a bar chart with 
```
pattern_history = [
    'berish_hanging_man',
    'bulish_hammer',
    'berish_dark_cloud_cover',
    'bulish_piercing_line',
    'berish_dark_cloud_cover',
    'berish_dark_cloud_cover',
    'bulish_hammer',
    'berish_hanging_man',
    'bulish_hammer',
    'bulish_morning_star',
]

mfe.bars_from_dict(
    fig=fig,
    axis=ax3,
    data_dict=pattern_history,
    xlabel='Amount',
    ylabel='Patterns overall'
)
```
Results:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_05.png)





