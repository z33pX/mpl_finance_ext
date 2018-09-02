# mpl_finance_ext

mpl_finance_ext provides functions to plot and evaluate finance data. 
It is a tool for experimenting with algorithms for algotrading.
It supports mainly these functions:

* Candlestick chart -- `plot_candlestick()`
* Filled OHLC chart  -- `plot_filled_ohlc()`
* Plot other stuff -- `plot()`
* Plot histogram -- `hist()`
* Plot bar chart -- `bars()`
* Scatter plot -- `scatter()`
* 3D scatter plot -- `scatter_3d()`

For `plot_candlestick()` and `plot_filled_ohlc()` signal evaluation is possible. 
That means when you have buy and sell signals provided by an algotrading algorithm 
for example you can plot them in the graph to get a visal picture (same for candlestick patterns).
The yield of buy and sell will be calculated and is shown in the graph as well. All this will be shown in
a few examples below. All following code is provided in `examples/examples.py`.

First we load the data and calculate some example indicators:

```
# Load dataset
data = pd.read_csv('BTC_XRP_5min.csv', index_col=0)

# Calculate indicators
data = relative_strength_index(df=data, n=14)
data = bollinger_bands(df=data, n=20, std=4)
data = exponential_moving_average(df=data, n=8)
data = moving_average(df=data, n=36)

# Now we set some signals and patterns
# Some manually picked signals
signals = [
    ('BUY', 12, 0.69), ('SELL', 27, 0.7028),
    ('BUY', 56, 0.6563), ('SELL', 81, 0.6854),
    ('BUY', 106, 0.665), ('SELL', 165, 0.640),
    ('BUY', 183, 0.66), ('SELL', 202, 0.7063),
]

# One manually picked candlestick pattern
patterns = [
    ['inverted_hammer', 12, 13]
]
```

Plot candlestick charts
-
After we prepared the data we create a figure and an axis and plot 
the candlesticks plus some indicators on one axis and the rsi 
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
# 4) Exponential Moving Average 8
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
    disable_x_ticks=True
)
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
    name='RSI_14',
    plot_columns=['RSI_14'],
    axis=ax1,
    fig=fig,
    xhline_red=0.8,
    xhline_green=0.2,
    gradient_fill=True
)

plt.show()
```

The result looks like this:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_01.png)

For further explanations for the parameters please look into the function descriptions. 


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
by defining a list of signals and set parameter `signals=signals` of
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

As shown in example 4 in `examples.py` a histogram will be created like
```
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
    
mfe.hist(
    fig=fig,
    axis=ax2,
    data_dict=x,
    bins=50,
    density=1,
    xlabel='Returns',
    ylabel='Probability density'
)
```
and a bar chart like 
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

mfe.bar(
    fig=fig,
    axis=ax3,
    data_dict=pattern_history,
    xlabel='Amount',
    ylabel='Patterns overall'
)
```
Results:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_05.png)

Plot
-

in this example we plot some stock data in two lines of code:

```
    df = pd.read_csv('stocks.csv', index_col=0).tail(1000)
    mfe.plot(df / df.iloc[0], gradient_fill=True)
```

Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_07.png)


3D Scatter
-

- `data`: The data structure is a list of tripls like `[(x, y, z), (x, y, z)]`.
- `threshold`: Defines the threshold of the classification.
- `class_conditions`: This list contains the class values of the triples. If the value is less than the
threshold value it is considered class a otherwise class b. The list must have the same length as the data list.

Example:
```
data = list()
class_conditions = list()
samples = 30

# Create some data
for i in range(samples):
    data.append((i, i, i))
    if i < samples / 2:
        class_conditions.append(1)
    else:
        class_conditions.append(2)

# Graph everything
mfe.scatter_3d(
    data=data,
    class_conditions=class_conditions,
    threshold=1,
    show=True,
    xlabel='X',
    ylabel='Y',
    zlabel='Z'
)
```
Result:

![](https://github.com/z33pX/mpl_finance_ext/blob/master/pic_06.png)


