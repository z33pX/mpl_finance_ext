import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
import pandas as pd
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.patches import BoxStyle
from six.moves import xrange, zip

from angled_box_style import AngledBoxStyle
from candlestick_pattern_evaluation import draw_pattern_evaluation
from signal_evaluation import draw_signal_evaluation
from signal_evaluation import draw_verticals

# Colors:
label_colors = '#ffb200'
background_color = '#020100'

red = '#fe0000'
green = '#00fc01'

# Create angled box style
BoxStyle._style_list["angled"] = AngledBoxStyle


def _candlestick2_ohlc(
        ax, opens, highs, lows, closes,
        width=4.0, colorup='k', colordown='r',
        alpha=0.75, index_fix=True
):

    # _check_input(opens, highs, lows, closes)

    count = 0
    delta = width - 0.15
    barverts = list()
    for i, open, close in zip(xrange(len(opens)), opens, closes):
        if index_fix:
            i = opens.index[count]
            count += 1
        if open != -1 and close != -1:
            barverts.append(
                ((i - delta, open),
                 (i - delta, close),
                 (i + delta, close),
                 (i + delta, open))
            )

    count = 0
    rangesegments = list()
    for i, low, high in zip(xrange(len(lows)), lows, highs):
        if index_fix:
            i = opens.index[count]
            count += 1
        if low != -1:
            rangesegments.append(
                ((i, low), (i, high))
            )

    colorup = mcolors.to_rgba(colorup, alpha)
    colordown = mcolors.to_rgba(colordown, alpha)
    colord = {True: colorup, False: colordown}
    colors = [colord[open < close]
              for open, close in zip(opens, closes)
              if open != -1 and close != -1]

    use_aa = 0,  # use tuple here
    rangecollection = LineCollection(rangesegments,
                                     colors=colors,
                                     linewidths=0.7,
                                     antialiaseds=use_aa,
                                     )

    barcollection = PolyCollection(barverts,
                                   facecolors=colors,
                                   edgecolors=((0, 0, 0, 1), ),
                                   antialiaseds=use_aa,
                                   linewidths=0.0,
                                   )

    if index_fix:
        minx, maxx = closes.index[0], closes.index[-1]
    else:
        minx, maxx = 0, len(rangesegments)

    miny = min([low for low in lows if low != -1])
    maxy = max([high for high in highs if high != -1])

    corners = (minx, miny), (maxx, maxy)
    ax.update_datalim(corners)
    ax.autoscale_view()

    # add these last
    ax.add_collection(rangecollection)
    ax.add_collection(barcollection)
    return rangecollection, barcollection


def _tail(fig, ax, data, plot_columns, kwa):
    name = kwa.get('name', None)
    if name is not None:
        ax.text(
            0.5, 0.95, name, color=label_colors,
            horizontalalignment='center',
            fontsize=10, transform=ax.transAxes,
            zorder=120
        )

    # Plot columns
    if plot_columns is not None:
        for col in plot_columns:
            series = data[col]
            ax.plot(series, linewidth=0.7)
            add_price_flag(
                fig=fig, axis=ax,
                series=data[col],
                color=label_colors
            )

    xhline = kwa.get('xhline1', None)
    if xhline is not None:
        ax.axhline(xhline, color=label_colors, linewidth=0.5)

    xhline2 = kwa.get('xhline2', None)
    if xhline2 is not None:
        ax.axhline(xhline2, color=label_colors, linewidth=0.5)

    xhline_red = kwa.get('xhline_red', None)
    if xhline_red is not None:
        ax.axhline(xhline_red, color=red, linewidth=0.5)

    xhline_green = kwa.get('xhline_green', None)
    if xhline_green is not None:
        ax.axhline(xhline_green, color=green, linewidth=0.5)

    xhline_dashed_1 = kwa.get('xhline_dashed1', None)
    if xhline_dashed_1 is not None:
        ax.axhline(xhline_dashed_1, color=label_colors, linewidth=0.6, linestyle='--')

    xhline_dashed_2 = kwa.get('xhline_dashed2', None)
    if xhline_dashed_2 is not None:
        ax.axhline(xhline_dashed_2, color=label_colors, linewidth=0.6, linestyle='--')

    xhline_dotted_1 = kwa.get('xhline_dotted1', None)
    if xhline_dotted_1 is not None:
        ax.axhline(xhline_dotted_1, color=label_colors, linewidth=0.9, linestyle=':')

    xhline_dotted_2 = kwa.get('xhline_dotted2', None)
    if xhline_dotted_2 is not None:
        ax.axhline(xhline_dotted_2, color=label_colors, linewidth=0.9, linestyle=':')

    fancy_design(ax)
    rotation = kwa.get('xtickrotation', 35)
    plt.setp(ax.get_xticklabels(), rotation=rotation)
    if kwa.get('disable_x_ticks', False):
        labels = [item.get_text() for item in ax.get_xticklabels()]
        empty_string_labels = [''] * len(labels)
        ax.set_xticklabels(empty_string_labels)

    save = kwa.get('save', '')
    if save:
        plt.savefig(save, facecolor=fig.get_facecolor())

    if kwa.get('axis', None) is None and kwa.get('show', True):
        plt.show()
    return fig, ax


def _head(data, kwargs):
    # Prepare data ------------------------------------------
    for col in list(data):
        data[col] = pd.to_numeric(
            data[col], errors='coerce')

    # Build ax ----------------------------------------------
    fig = kwargs.get('fig', None)
    if fig is None:
        fig, _ = plt.subplots(facecolor=background_color)

    ax = kwargs.get('axis', None)
    if ax is None:
        ax = plt.subplot2grid(
            (4, 4), (0, 0),
            rowspan=4, colspan=4,
            facecolor=background_color
        )
    return fig, ax


def _signal_eval(ax, signals, kwargs):
    """
    Plots the signals
    :param ax: Axis
    :param signals: List of patterns with structure:
        [ ..., ['signal', index, price], ...], where
        signal can be either 'BUY' or 'SELL'
    :param kwargs:
        'draw_verticals': Plots vertical lines for each BUY and SELL
        'signl_evaluation': Plot signals
        'signl_evaluation_form': 'rectangles' or 'arrows_1'
        'dots': Plot dots at 'BUY' and 'SELL' points
    :return:
    """
    if signals is not None:
        if kwargs.get('draw_verticals', True):
            draw_verticals(axis=ax, signals=signals)
        if kwargs.get('signal_evaluation', True):
            draw_signal_evaluation(
                axis=ax,
                signals=signals,
                eval_type=kwargs.get('signal_evaluation_form', 'rectangle'),
                dots=kwargs.get('dots', True),
                red=red,
                green=green
            )


def _pattern_eval(data, ax, cs_patterns, kwargs):
    """
    Plots the candlestick patterns
    :param data: Data
    :param ax: Axis
    :param cs_patterns: List of patterns with structure:
        [ ..., ['pattern_name', start_index, stop_index], ...]
    :param kwargs:
        'cs_pattern_evaluation': Enable plotting
    :return:
    """
    if cs_patterns is not None:
        if kwargs.get('cs_pattern_evaluation', True):
            df = data[['open', 'high', 'low', 'close']]
            draw_pattern_evaluation(
                axis=ax,
                data_ohlc=df,
                cs_patterns=cs_patterns,
                red=red,
                green=green
            )


def fancy_design(axis):
    """
    This function changes the design for
        - the legend
        - spines
        - ticks
        - grid
    :param axis: Axis
    """
    legend = axis.legend(
        loc='best', fancybox=True, framealpha=0.3
    )

    legend.get_frame().set_facecolor(background_color)
    legend.get_frame().set_edgecolor(label_colors)

    for line, text in zip(legend.get_lines(),
                          legend.get_texts()):
        text.set_color(line.get_color())

    axis.grid(linestyle='dotted', color=label_colors, alpha=0.3)
    axis.yaxis.label.set_color(label_colors)
    axis.spines['left'].set_color(label_colors)
    axis.spines['right'].set_color(background_color)
    axis.spines['top'].set_color(background_color)
    axis.spines['bottom'].set_color(background_color)
    axis.tick_params(
        axis='y', colors=label_colors,
        which='major', labelsize=10,
        direction='in', length=2,
        width=1
    )

    axis.tick_params(
        axis='x', colors=label_colors,
        which='major', labelsize=10,
        direction='in', length=2,
        width=1
    )


def add_price_flag(fig, axis, series, color):
    """
    Add a price flag at the end of the data
    series in the chart
    :param fig: Figure
    :param axis: Axis
    :param series: Pandas Series
    :param color: Color of the flag
    """
    value = series.tail(1)
    last_index = value.index.tolist()[0]
    trans_offset = mtrans.offset_copy(
        axis.transData, fig=fig, x=0.05, y=0.0, units='inches'
    )

    # Add price text box for candlestick
    value_clean = format(value.values[0], '.6f')
    axis.text(
        last_index, value.values, value_clean,
        size=7, va="center", ha="left",
        transform=trans_offset,
        color=color,
        bbox=dict(
            boxstyle="angled,pad=0.2",
            alpha=0.6, color=color
        )
    )


def plot_candlestick(
        data, signals=None, cs_patterns=None,
        plot_columns=None, **kwargs):
    """
    This function plots a candlestick chart
    :param data: Pandas DataFrame
    :param signals: List of signals with structure
        [(signal, index, price), ... ]. Signal can be 'BUY'
        or 'SELL'
    :param plot_columns: List of columns in the given DataFrame like
        plot_columns=['bband_upper_20', 'bband_lower_20']
    :param kwargs:
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'name': Name of the chart
        'draw_verticals': plots vertical lines for each BUY and SELL
        'signl_evaluation': plot signals
        'signl_evaluation_form': 'rectangles' or 'arrows_1'
        'cs_pattern_evaluation': plot candlestick pattern
        'dots': Plot dots at 'BUY' and 'SELL' points
        'xhline1': Normal horizontal line 1
        'xhline2': Normal horizontal line 1
        'xhline_red': Red horizontal line
        'xhline_green': Green horizontal line
        'xhline_dashed1': Dashed horizontal line 1
        'xhline_dashed2': Dashed horizontal line 2
        'xhline_dotted1': Dotted horizontal line 1
        'xhline_dotted2': Dotted horizontal line 2
        'xtickrotation': Angle of the x ticks
        'disable_x_ticks': Disables the x ticks
        'show': If true the chart will be plt.show'd
        'save': Save the image to a specified path like
            save='path_to_picture.png'
    :return: fig, ax
    """
    fig, ax = _head(data, kwargs)

    # Add candlestick
    _candlestick2_ohlc(
        ax,
        data['open'], data['high'],
        data['low'], data['close'],
        width=0.6,
        colorup='g',
        colordown='r',
        alpha=1
    )

    _signal_eval(ax, signals, kwargs)
    _pattern_eval(data, ax, cs_patterns, kwargs)

    return _tail(fig, ax, data, plot_columns, kwargs)


def plot_filled_ohlc(
        data, signals=None, cs_patterns=None,
        plot_columns=None, **kwargs):
    """
    This function plots a filled ohlc chart
    :param data: Pandas DataFrame
    :param signals: List of signals with structure
        [(signal, index, price), ... ]. Signal can be 'BUY'
        or 'SELL'
    :param plot_columns: List of columns in the given DataFrame like
        plot_columns=['bband_upper_20', 'bband_lower_20']
    :param kwargs:
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'name': Name of the chart
        'draw_verticals': plots vertical lines for each BUY and SELL
        'signl_evaluation': plot signals
        'signl_evaluation_form': 'rectangles' or 'arrows_1'
        'cs_pattern_evaluation': plot candlestick pattern
        'dots': Plot dots at 'BUY' and 'SELL' points
        'xhline1': Normal horizontal line 1
        'xhline2': Normal horizontal line 1
        'xhline_red': Red horizontal line
        'xhline_green': Green horizontal line
        'xhline_dashed1': Dashed horizontal line 1
        'xhline_dashed2': Dashed horizontal line 2
        'xhline_dotted1': Dotted horizontal line 1
        'xhline_dotted2': Dotted horizontal line 2
        'xtickrotation': Angle of the x ticks
        'disable_x_ticks': Disables the x ticks
        'show': If true the chart will be plt.show'd
        'save': Save the image to a specified path like
            save='path_to_picture.png'
    :return: fig, ax
    """
    fig, ax = _head(data, kwargs)

    # Add filled_ohlc
    ax.fill_between(
        data.index,
        data['close'],
        data['high'],
        where=data['close'] <= data['high'],
        facecolor=green,
        interpolate=True,
        alpha=0.35,
        edgecolor=green
    )
    ax.fill_between(
        data.index,
        data['close'],
        data['low'],
        where=data['low'] <= data['close'],
        facecolor=red,
        interpolate=True,
        alpha=0.35,
        edgecolor=red
    )

    _signal_eval(ax, signals, kwargs)
    _pattern_eval(data, ax, cs_patterns, kwargs)

    return _tail(fig, ax, data, plot_columns, kwargs)


def plot(data, plot_columns, **kwargs):
    """
    This function provides a simple way to plot time series
    for example data['close'].
    :param data: Pandas DataFrame object
    :param plot_columns: Name of the columns to plot
    :param kwargs:
        'fig': Figure.
        'axis': Axis. If axis is not given the chart will
            plt.plot automatically
        'name': Name of the chart
        'xhline1': Normal horizontal line 1
        'xhline2': Normal horizontal line 1
        'xhline_red': Red horizontal line
        'xhline_green': Green horizontal line
        'xhline_dashed1': Dashed horizontal line 1
        'xhline_dashed2': Dashed horizontal line 2
        'xhline_dotted1': Dotted horizontal line 1
        'xhline_dotted2': Dotted horizontal line 2
        'xtickrotation': Angle of the x ticks
        'disable_x_ticks': Disables the x ticks
        'show': If true the chart will be plt.show'd
        'save': Save the image to a specified path like
            save='path_to_picture.png'
    :return: fig, ax
    """
    fig, ax = _head(data, kwargs)
    return _tail(fig, ax, data, plot_columns, kwargs)
