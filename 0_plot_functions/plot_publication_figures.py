import numpy as np
import matplotlib.pyplot as plt

def plot_dual_axis_percentiles(left_axis_data, right_axis_data=None, x_col='y_um', 
                               x_config=None, percentiles=[25, 50, 75], 
                               figsize=(8, 6), font_size=8):
    """
    Plot percentile data with optional dual y-axes.

    Parameters:
    -----------
    left_axis_data : list of dict
        Each dict contains: 'df', 'y_col', and optionally 'label', 'color', 'ylabel', 
        'ylim', 'yticks'
    right_axis_data : list of dict or None
        Same structure as left_axis_data. If None, creates single axis plot.
    x_col : str
        Column name for x-axis
    x_config : dict or None
        Dict with 'xlabel', 'xlim', 'xticks' for x-axis configuration
    percentiles : list
        List of percentiles to calculate [lower, median, upper]
    figsize : tuple
        Figure size (width, height)
    font_size : int
        Font size for labels and ticks
    """

    def calculate_percentiles(df, x_col, y_col, percentiles):
        return df.groupby(x_col)[y_col].agg([
            ('lower', lambda x: np.percentile(x.dropna(), percentiles[0])),
            ('median', lambda x: np.percentile(x.dropna(), percentiles[1])),
            ('upper', lambda x: np.percentile(x.dropna(), percentiles[2]))
        ]).reset_index().sort_values(x_col)

    def plot_on_axis(ax, data_list, x_col, percentiles, font_size, is_right=False, color_axis=False):
        for i, data in enumerate(data_list):
            df = data['df']
            y_col = data['y_col']
            color = data.get('color', f'C{i}')
            label = data.get('label', y_col)

            # Validate column exists
            if y_col not in df.columns:
                raise ValueError(f"Column '{y_col}' not found in dataframe")

            # Calculate percentiles
            perc = calculate_percentiles(df, x_col, y_col, percentiles)
            x_vals = perc[x_col].values

            # Plot
            ax.fill_between(x_vals, perc['lower'].values, perc['upper'].values, 
                           alpha=0.2, color=color)
            ax.plot(x_vals, perc['median'].values, '-', lw=1.5, color=color, label=label)

        # Apply first dataset's axis settings
        data = data_list[0]
        ylabel = data.get('ylabel', data['y_col'])
        ylim = data.get('ylim', None)
        yticks = data.get('yticks', None)

        # Color axis only if color_axis is True AND single dataset
        axis_color = color if (color_axis and len(data_list) == 1) else 'black'

        ax.set_ylabel(ylabel, color=axis_color, fontsize=font_size)
        ax.tick_params(axis='y', labelcolor=axis_color, labelsize=font_size)

        if is_right:
            ax.spines['right'].set_color(axis_color)
        else:
            ax.spines['left'].set_color(axis_color)

        if ylim:
            ax.set_ylim(*ylim)
        if yticks is not None:
            ax.set_yticks(yticks)

    # Create figure
    fig, ax1 = plt.subplots(figsize=figsize)

    # Plot left axis - color only if dual axis
    color_left = right_axis_data is not None
    plot_on_axis(ax1, left_axis_data, x_col, percentiles, font_size, 
                 is_right=False, color_axis=color_left)

    # Configure x-axis
    if x_config is None:
        x_config = {}

    xlabel = x_config.get('xlabel', x_col)
    xlim = x_config.get('xlim', None)
    xticks = x_config.get('xticks', None)

    ax1.set_xlabel(xlabel, fontsize=font_size)
    ax1.tick_params(axis='x', labelsize=font_size)
    if xlim:
        ax1.set_xlim(*xlim)
    if xticks is not None:
        ax1.set_xticks(xticks)

    # Plot right axis if provided
    if right_axis_data is not None:
        ax2 = ax1.twinx()
        plot_on_axis(ax2, right_axis_data, x_col, percentiles, font_size, 
                     is_right=True, color_axis=True)
        ax2.spines['top'].set_visible(False)

        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=font_size, 
                  frameon=False, loc='upper right')
    else:
        ax1.legend(fontsize=font_size, frameon=False, loc='upper right')
        ax1.spines['right'].set_visible(False)

    ax1.spines['top'].set_visible(False)

    plt.tight_layout()

    return fig, ax1
