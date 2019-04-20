from .candlestick2_ohlc import candlestick2
from .utils import *


def plot_candlestick(
        data, signals=None, cs_patterns=None,
        columns=list(), **kwargs):
    """
    This function plots a candlestick chart
    :param data: Pandas DataFrame
    :param signals: List of signals with structure
        [(signal, index, price), ... ]. Signal can be 'BUY'
        or 'SELL'
    :param cs_patterns: List of candlestick patterns with structure
    patterns = [... , ['pattern_name', start_index, stop_index], ... ]
    :param columns: List of columns in the given DataFrame like
        columns=['bband_upper_20', 'bband_Lower_20']
    :param kwargs:
        'cs_pattern_evaluation': Enables plotting
        'draw_verticals': Plots vertical lines
            for each BUY and SELL
        'signal_evaluation': Plot signals
        'signal_evaluation_type': 'rectangles' or
            'arrows_1'
        'dots': Plot dots at 'BUY' and 'SELL' points
        'disable_losing_trades': Disable losing trades
        'disable_winning_trades': Disable winning trades
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'xticks': Set x tick labels
        'name': Name of the chart
        'flags': Enable flags
        'flags_position_correction': Correct position of flags
        'lines': List of lines
            [{'start': [x, y], 'stop': [x, y], 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'hlines': List of horizontal lines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vlines': List of vlines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vspans': List of vspans: [[start index, end index], ...]
        'hspans': List of hspans: [[start index, end index], ...]
        'xlabel': x label
        'ylabel': x label
        'title': title
        'legend': Activate legend
        'disable_xticks': Disables the x ticks
        'show': If true the chart will be plotted
        'save': Save the image to a specified path with
            save='path_to_picture.png' for example
    :return: fig, ax
    """
    fig, ax = head(kwargs=kwargs)

    # Add candlestick
    candlestick2(
        ax,
        data['Open'], data['High'],
        data['Low'], data['Close'],
        width=0.6,
        colorup=config['colors']['green'],
        colordown=config['colors']['red'],
        alpha=1
    )

    signal_eval(ax, signals, kwargs)
    pattern_eval(data, ax, cs_patterns, kwargs)

    return tail(
        fig=fig,
        ax=ax,
        kwa=kwargs,
        data=data,
        columns=columns
    )


def plot_volume(data, **kwargs):
    """
    This function provides a simple way to plot volume data.
    :param data: Pandas DataFrame
    :param columns: Name of the columns to plot
    :param kwargs:
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'twin_axis': To plot price data and volume in the same chart
        'col_name': defines the column with colume data
        'xticks': Set x tick labels
        'name': Name of the chart
        'flags': Enable flags
        'flags_position_correction': Correct position of flags
        'lines': List of lines
            [{'start': [x, y], 'stop': [x, y], 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'hlines': List of horizontal lines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vlines': List of vlines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vspans': List of vspans: [[start index, end index], ...]
        'hspans': List of hspans: [[start index, end index], ...]
        'xlabel': x label
        'ylabel': x label
        'title': title
        'legend': Activate legend
        'disable_xticks': Disables the x ticks
        'show': If true the chart will be plotted
        'save': Save the image to a specified path with
            save='path_to_picture.png' for example
    :return: fig, ax
    """

    fig = kwargs.get('fig', None)
    if fig is None:
        fig, _ = plt.subplots(facecolor=config['colors']['background'])

    ax = kwargs.get('axis', None)
    ax_t = kwargs.get('twin_axis', None)
    if ax is None and ax_t is None:
        ax = plt.subplot2grid(
            (4, 4), (0, 0),
            rowspan=4, colspan=4,
            facecolor=config['colors']['background']
        )

    elif ax_t is not None:
        ax = ax_t.twinx()  # instantiate a second axes that shares the same x-axis

    col_name = kwargs.get('col_name', 'Volume')

    barlist = ax.bar(
        data.index, data[col_name],
        align='center'
    )

    for i, row in data.iterrows():
        if row['Open'] <= row['Close']:
            barlist[i].set_color(config['colors']['green'])
        else:
            barlist[i].set_color(config['colors']['red'])

    kwargs['legend'] = False

    return tail(
        fig=fig,
        ax=ax,
        kwa=kwargs,
        data=data,
        columns=[]
    )


def plot(data, columns, **kwargs):
    """
    This function provides a simple way to plot time series data.
    :param data: Pandas DataFrame
    :param columns: Name of the columns to plot
    :param kwargs:
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'xticks': Set x tick labels
        'name': Name of the chart
        'flags': Enable flags
        'flags_position_correction': Correct position of flags
        'lines': List of lines
            [{'start': [x, y], 'stop': [x, y], 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'hlines': List of horizontal lines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vlines': List of vlines:
            [index_1, index_2, ...] or
            [{'index':..., 'color':..., 'linewidth':...,
                'alpha':..., 'linestyle':...,}, ...]
        'vspans': List of vspans: [[start index, end index], ...]
        'hspans': List of hspans: [[start index, end index], ...]
        'xlabel': x label
        'ylabel': x label
        'title': title
        'legend': Activate legend
        'disable_xticks': Disables the x ticks
        'show': If true the chart will be plotted
        'save': Save the image to a specified path with
            save='path_to_picture.png' for example
    :return: fig, ax
    """
    fig, ax = head(kwargs=kwargs)

    return tail(
        fig=fig,
        ax=ax,
        kwa=kwargs,
        data=data,
        columns=columns
    )
