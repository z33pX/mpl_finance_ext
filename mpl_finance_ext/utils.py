import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
import numpy as np

from .config import config
from matplotlib.patches import Polygon
from matplotlib.patches import BoxStyle
from .angled_box_style import AngledBoxStyle
from .cs_evaluation import draw_pattern_evaluation
from .signal_evaluation import draw_signal_evaluation
from .signal_evaluation import draw_verticals

# Create angled box style
BoxStyle._style_list["angled"] = AngledBoxStyle


def plot_lines(axis, lines, linestyle='--', color=config['colors']['sets'][0]):
    """
    Plots vertical lines
    :param axis: Axis
    :param lines:
        [{'start': [x, y], 'stop': [x, y], 'color':..., 'linewidth':...,
            'alpha':..., 'linestyle':...,}, ...]
    :param linestyle: Can be '-', '--', '-.', ':'
    :param color: Color
    """

    for line in lines:
        start = line.get('start')
        stop = line.get('stop')
        color = line.get('color', color)
        linewidth = line.get('linewidth', 0.8)
        alpha = line.get('alpha', 0.8)
        linestyle = line.get('linestyle', linestyle)
        axis.plot([start[0], stop[0]], [start[1], stop[1]], color=color,
                  linewidth=linewidth, alpha=alpha, linestyle=linestyle)


def plot_vlines(axis, vlines, linestyle='--', color=config['colors']['sets'][0]):
    """
    Plots a vertical line
    :param axis: Axis
    :param vlines:
        [index_1, index_2, ...] or
        [{'index':..., 'color':..., 'linewidth':...,
            'alpha':..., 'linestyle':...,}, ...]
    :param linestyle: Can be '-', '--', '-.', ':'
    :param color: Color
    """

    for vline in vlines:
        if isinstance(vline, int):
            axis.axvline(
                vline, color=color,
                linewidth=0.8, alpha=0.8, linestyle=linestyle
            )
        else:
            index = vline.get('index')
            color = vline.get('color', color)
            linewidth = vline.get('linewidth', 0.8)
            alpha = vline.get('alpha', 0.8)
            linestyle = vline.get('linestyle', linestyle)
            axis.axhline(
                index, color=color,
                linewidth=linewidth, alpha=alpha, linestyle=linestyle
            )


def plot_hlines(axis, hlines, linestyle='--', color=config['colors']['sets'][0]):
    """
    Plots a vertical line
    :param axis: Axis
    :param hlines:
        [index_1, index_2, ...] or
        [{'index':..., 'color':..., 'linewidth':...,
            'alpha':..., 'linestyle':...,}, ...]
    :param linestyle: Can be '-', '--', '-.', ':'
    :param color: Color
    """

    for hline in hlines:
        if isinstance(hline, int):
            axis.axhline(
                hline, color=color,
                linewidth=0.8, alpha=0.8, linestyle=linestyle
            )
        else:
            index = hline.get('index')
            color = hline.get('color', color)
            linewidth = hline.get('linewidth', 0.8)
            alpha = hline.get('alpha', 0.8)
            linestyle = hline.get('linestyle', linestyle)
            axis.axhline(
                index, color=color,
                linewidth=linewidth, alpha=alpha, linestyle=linestyle
            )


def plot_vspans(axis, vspans, color=config['colors']['labels'], alpha=0.25):
    """
    Plots a vertical span
    :param axis: Axis
    :param vspans: List of spans: [[start index, end index], ...]
    :param color: Color
    :param alpha: Alpha
    :return:
    """

    for span in vspans:
        axis.axvspan(
            span[0], span[1],
            facecolor=color,
            alpha=alpha
        )


def plot_hspans(axis, hspans, color=config['colors']['labels'], alpha=0.25):
    """
    Plots a vertical span
    :param axis: Axis
    :param hspans: List of spans: [[start index, end index], ...]
    :param color: Color
    :param alpha: Alpha
    :return:
    """

    for hspan in hspans:
        axis.axhspan(
            hspan[0], hspan[1],
            facecolor=color,
            alpha=alpha
        )


def add_text_box(fig, ax, text, x_p, y_p):
    x = ax.get_xlim()
    y = ax.get_ylim()
    text_x = int(x[0]) / 100 * x_p
    text_y = int(y[1]) / 100 * y_p

    trans_offset = mtrans.offset_copy(
        ax.transData,
        fig=fig,
        x=0.0,
        y=0.0,
        units='inches'
    )

    ax.text(text_x, text_y, text, ha='left', va='center',
              transform=trans_offset, color='#535353',
              bbox=dict(alpha=0.4, color=config['colors']['labels']))


def gradient_fill(ax, data, color):
    """
    Gradient fill
    :param ax: Axis
    :param data: pandas Series
    :param color: color
    """

    line, = ax.plot(data, linewidth=0.7, color=color)

    # From https://stackoverflow.com/questions/29321835/is-it-possible-to-get-color-gradients-
    #           under-curve-in-matplotlib?answertab=votes#tab-top
    data.dropna(inplace=True)
    x = data.index
    y = data.values

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha

    z = np.empty((300, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(color)
    z[:, :, :3] = rgb
    z[:, :, -1] = np.linspace(0, alpha, 300)[:, None]

    xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = np.column_stack([x, y])
    xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
    clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)


def tail(fig, ax, kwa, data, columns):

    # Lines:
    lines = kwa.get('lines', None)
    if lines is not None:
        plot_lines(
            axis=ax, lines=lines
        )

    # Vertical span and lines:
    vlines = kwa.get('vlines', None)
    if vlines is not None:
        plot_vlines(
            axis=ax, vlines=vlines
        )

    # Vertical span and lines:
    hlines = kwa.get('hlines', None)
    if hlines is not None:
        plot_hlines(
            axis=ax, hlines=hlines
        )

    vspans = kwa.get('vspans', None)
    if vspans is not None:
        plot_vspans(
            axis=ax, vspans=vspans
        )

    hspans = kwa.get('hspans', None)
    if hspans is not None:
        plot_hspans(
            axis=ax, hspans=hspans
        )

    # Names, title, labels
    name = kwa.get('name', None)
    if name is not None:
        ax.text(
            0.5, 0.95, name, color=config['colors']['labels'],
            horizontalalignment='center',
            fontsize=10, transform=ax.transAxes,
            zorder=120
        )

    xlabel = kwa.get('xlabel', None)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    ylabel = kwa.get('ylabel', None)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    title = kwa.get('title', None)
    if title is not None:
        ax.set_title(title, color=config['colors']['labels'])

    # Plot columns
    enable_flags = kwa.get('flags', True)
    last_index = data.index.values[-1] if \
        kwa.get('flags_position_correction', True) else None

    g_fill = kwa.get('gradient_fill', False)

    if columns:
        for i, col in enumerate(columns):
            series = data[col]
            color = config['colors']['sets'][i % len(
                config['colors']['sets'])]

            if g_fill:
                gradient_fill(ax=ax, data=series, color=color)
            else:
                ax.plot(series, linewidth=0.7, color=color)

            if enable_flags:
                add_price_flag(
                    fig=fig, axis=ax,
                    series=data[col],
                    color=color,
                    last_index=last_index
                    )

    main_spine = kwa.get('main_spine', 'left')
    legend = kwa.get('legend', True)
    fancy_design(ax, main_spine=main_spine, legend=legend)

    rotation = kwa.get('xtickrotation', 35)
    plt.setp(ax.get_xticklabels(), rotation=rotation)

    if kwa.get('disable_xticks', False):
        ax.tick_params(
            axis='x',           # changes apply to the x-axis
            which='both',       # both major and minor ticks are affected
            bottom=False,       # ticks along the bottom edge are off
            top=False,          # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off

    xticks = kwa.get('xticks', None)
    if xticks is not None:
        ax.set_xticklabels(xticks.values)

    save = kwa.get('save', '')
    if save:
        plt.savefig(save, facecolor=fig.get_facecolor())

    ax_1 = kwa.get('axis', None)
    ax_t = kwa.get('twin_axis', None)

    if (ax_1 is None and ax_t is None) and \
            kwa.get('show', True):
        plt.show()
    return fig, ax


def head(kwargs):

    fig = kwargs.get('fig', None)
    if fig is None:
        fig, _ = plt.subplots(facecolor=config['colors']['background'])

    ax = kwargs.get('axis', None)
    if ax is None:
        ax = plt.subplot2grid(
            (4, 4), (0, 0),
            rowspan=4, colspan=4,
            facecolor=config['colors']['background']
        )
    return fig, ax


def signal_eval(ax, signals, kwargs):
    """
    Plots the signals
    :param ax: Axis
    :param signals: List of patterns with structure:
        [ ..., ['signal', index, price], ...], where
        signal can be either 'BUY' or 'SELL'
    :param kwargs:
        'draw_verticals': Plots vertical lines
            for each BUY and SELL
        'signal_evaluation': Plot signals
        'signal_evaluation_type': 'rectangles' or
            'arrows_1'
        'dots': Plot dots at 'BUY' and 'SELL' points
        'disable_losing_trades': Disable losing trades
        'disable_winning_trades': Disable winning trades
    """

    if signals is not None:
        if kwargs.get('draw_verticals', False):
            draw_verticals(axis=ax, signals=signals)
        if kwargs.get('signal_evaluation', True):
            draw_signal_evaluation(
                axis=ax,
                signals=signals,
                eval_type=kwargs.get(
                    'signal_evaluation_type',
                    'rectangle'),
                dots=kwargs.get('dots', True),
                red=config['colors']['red'],
                green=config['colors']['green'],
                disable_losing_trades=kwargs.get(
                    'disable_losing_trades', False),
                disable_winning_trades=kwargs.get(
                    'disable_winning_trades', False)
            )


def pattern_eval(data, ax, cs_patterns, kwargs):
    """
    Plots the candlestick patterns
    :param data: Data
    :param ax: Axis
    :param cs_patterns: List of patterns with structure:
        [ ..., ['pattern_name', start_index,
            stop_index], ...]
    :param kwargs:
        'cs_pattern_evaluation': Enables plotting
    """

    if cs_patterns is not None:
        if kwargs.get('cs_pattern_evaluation', True):
            df = data[['Open', 'High', 'Low', 'Close']]
            draw_pattern_evaluation(
                axis=ax,
                data_ohlc=df,
                cs_patterns=cs_patterns,
                red=config['colors']['red'],
                green=config['colors']['green']
            )


def fancy_design(axis, main_spine='left', legend=True, grid_x=True,
                 grid_y=True, legend_loc='best'):
    """
    This function changes the design for
        - the legend
        - spines
        - ticks
        - grid
    :param grid_y: Enable y
    :param grid_x: Enable x
    :param main_spine: main spine
    :param axis: Axis
    :param legend: Activate legend
    :param legend_loc: Location of legend
    """
    if legend:
        legend = axis.legend(
            loc=legend_loc, fancybox=True, framealpha=0.3
        )

        legend.get_frame().set_facecolor(config['colors']['background'])
        legend.get_frame().set_edgecolor(config['colors']['labels'])

        for line, text in zip(legend.get_lines(),
                              legend.get_texts()):
            text.set_color(line.get_color())

    if grid_x:
        axis.grid(linestyle='dotted', axis='x', color=config['colors']['grid'], alpha=0.7)
    else:
        axis.grid(None, axis='x')

    if grid_y:
        axis.grid(linestyle='dotted', axis='y', color=config['colors']['grid'], alpha=0.7)
    else:
        axis.grid(None, axis='y')

    axis.yaxis.label.set_color(config['colors']['yaxis_labels'])
    axis.xaxis.label.set_color(config['colors']['xaxis_labels'])

    for spine in axis.spines:
        if spine == main_spine:
            axis.spines[spine].set_color(config['colors']['main_spine'])
        else:
            axis.spines[spine].set_color(config['colors']['background'])
    axis.tick_params(
        axis='y', colors=config['colors']['yaxis_params'],
        which='major', labelsize=10,
        direction='in', length=2,
        width=1
    )

    axis.tick_params(
        axis='x', colors=config['colors']['xaxis_params'],
        which='major', labelsize=10,
        direction='in', length=2,
        width=1
    )


def add_price_flag(fig, axis, series, color, last_index=None):
    """
    Add a price flag at the end of data series in the chart
    :param fig: Figure
    :param axis: Axis
    :param series: Pandas Series
    :param color: Color of the flag
    :param last_index: Last index
    """

    series = series.dropna()
    value = series.tail(1)

    try:
        index = value.index.tolist()[0]
        if last_index is not None:
            axis.plot(
                [index, last_index], [value.values[0], value.values[0]],
                color=color, linewidth=0.6, linestyle='--', alpha=0.6
            )
        else:
            last_index = index

        trans_offset = mtrans.offset_copy(
            axis.transData, fig=fig,
            x=0.05, y=0.0, units='inches'
        )

        # Add price text box for candlestick
        value_clean = format(value.values[0], '.6f')
        axis.text(
            last_index, value.values, value_clean,
            size=7, va="center", ha="left",
            transform=trans_offset,
            color=config['colors']['price_flag'],
            bbox=dict(
                boxstyle="angled,pad=0.2",
                alpha=0.6, color=color
            )
        )

    except IndexError:
        pass
