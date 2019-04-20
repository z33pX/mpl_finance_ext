from matplotlib.collections import LineCollection, PolyCollection
from .config import config


class Candlestick2:

    def __init__(self, ax, opens, highs, lows, closes, alpha, width=4.0):

        self.ax = ax
        self.width = width
        self.alpha = alpha

        self.colorup = config['colors']['green']
        self.colordown = config['colors']['red']

        self.lc = None
        self.bcu = None
        self.bcd = None

        self.__calc_collections(opens, highs, lows, closes)

        self.ax.add_collection(self.lc)
        self.ax.add_collection(self.bcu)
        self.ax.add_collection(self.bcd)

    def set_ydata(self, opens, highs, lows, closes):

        self.lc.remove()
        self.bcu.remove()
        self.bcd.remove()

        self.__calc_collections(opens, highs, lows, closes)

        self.ax.add_collection(self.lc)
        self.ax.add_collection(self.bcu)
        self.ax.add_collection(self.bcd)

    def __calc_collections(self, opens, highs, lows, closes):

        line_colors = list()
        poly_colors_up = list()
        poly_colors_down = list()

        delta = self.width - 0.16
        poly_segments_up = list()
        poly_segments_down = list()
        line_segments = list()

        for i, open, close, high, low in zip(range(len(opens)), opens, closes, highs, lows):
            # print(open, high, low, close)

            if open != -1 and close != -1:
                # Simple modification to draw a line for open == close
                # if open == close:
                #     open -= 0.01 * abs(high - low)

                if open is None or high is None or low is None or close is None:
                    # print(i, open, high, low, close)
                    # Die Daten hier werden nur ganz am Anfang von dyn_arch geschrieben
                    # Die spaeteren Daten werden gar nicht berueckstichtig, weil sie in
                    # set_ydata geschrieben werden
                    continue
                    # line_segments.append(((i, None), (i, None)))
                    # line_colors.append(colorup)

                if close > open:
                    poly_segments_up.append(
                        ((i - delta, open), (i - delta, close),
                         (i + delta, close), (i + delta, open))
                    )
                    poly_colors_up.append(self.colorup)
                    if close < high:
                        line_segments.append(((i, close), (i, high)))
                        line_colors.append(self.colorup)
                    if low < open:
                        line_segments.append(((i, low), (i, open)))
                        line_colors.append(self.colorup)

                else:
                    poly_segments_down.append(
                        ((i - delta, open), (i - delta, close),
                         (i + delta, close), (i + delta, open))
                    )
                    poly_colors_down.append(self.colordown)
                    if open < high:
                        line_segments.append(((i, open), (i, high)))
                        line_colors.append(self.colordown)
                    if low < close:
                        line_segments.append(((i, low), (i, close)))
                        line_colors.append(self.colordown)

        use_aa = 0,  # use tuple here
        self.lc = LineCollection(
            line_segments,
            colors=line_colors,
            linewidths=0.7,
            antialiaseds=use_aa,
            linestyles='solid'
        )

        self.bcu = PolyCollection(
            poly_segments_up,
            facecolors=self.colorup,
            edgecolors=poly_colors_up,
            antialiaseds=use_aa,
            linewidths=0,
        )

        self.bcd = PolyCollection(
            poly_segments_down,
            facecolors=self.colordown,
            edgecolors=poly_colors_down,
            antialiaseds=use_aa,
            linewidths=0,
        )


def candlestick2(
        ax, opens, highs, lows, closes,
        width=4.0, colorup=config['colors']['green'], colordown=config['colors']['red'],
        alpha=0.75, index_fix=True):

    # Functions not supported in macOS
    # colorup = mcolors.to_rgba(colorup, alpha)
    # colordown = mcolors.to_rgba(colordown, alpha)
    line_colors = list()
    poly_colors_up = list()
    poly_colors_down = list()

    count = 0
    delta = width - 0.16
    poly_segments_up = list()
    poly_segments_down = list()
    line_segments = list()
    for i, open, close, high, low in zip(range(len(opens)), opens, closes, highs, lows):
        if index_fix:
            i = opens.index[count]
            count += 1
        if open != -1 and close != -1:
            # Simple modification to draw a line for open == close
            # if open == close:
            #     open -= 0.01 * abs(high - low)

            if close > open:
                poly_segments_up.append(
                    ((i - delta, open), (i - delta, close),
                     (i + delta, close), (i + delta, open))
                )
                poly_colors_up.append(colorup)
                if close < high:
                    line_segments.append(((i, close), (i, high)))
                    line_colors.append(colorup)
                if low < open:
                    line_segments.append(((i, low), (i, open)))
                    line_colors.append(colorup)

            else:
                poly_segments_down.append(
                    ((i - delta, open), (i - delta, close),
                     (i + delta, close), (i + delta, open))
                )
                poly_colors_down.append(colordown)
                if open < high:
                    line_segments.append(((i, open), (i, high)))
                    line_colors.append(colordown)
                if low < close:
                    line_segments.append(((i, low), (i, close)))
                    line_colors.append(colordown)

    use_aa = 0,  # use tuple here
    line_collection = LineCollection(
        line_segments,
        colors=line_colors,
        linewidths=0.7,
        antialiaseds=use_aa,
        linestyles='solid'
    )

    bar_collection_down = PolyCollection(
        poly_segments_down,
        facecolors=config['colors']['red'],
        edgecolors=poly_colors_down,
        antialiaseds=use_aa,
        linewidths=0,
    )

    bar_collection_up = PolyCollection(
        poly_segments_up,
        facecolors=config['colors']['green'],
        edgecolors=poly_colors_up,
        antialiaseds=use_aa,
        linewidths=0,
    )

    if index_fix:
        minx, maxx = closes.index[0], closes.index[-1]
    else:
        minx, maxx = 0, len(line_segments)

    miny = min([low for low in lows if low != -1])
    maxy = max([high for high in highs if high != -1])

    corners = (minx, miny), (maxx, maxy)
    ax.update_datalim(corners)
    ax.autoscale_view()

    ax.add_collection(line_collection)
    ax.add_collection(bar_collection_up)
    ax.add_collection(bar_collection_down)
    return line_collection, bar_collection_up, bar_collection_down
