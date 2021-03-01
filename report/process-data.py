import sys
from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns


def load_benchmark_data(path: str) -> List[pd.DataFrame]:
    col_names = ['Invocation', 'Iteration', 'Value', 'Unit', 'Criterion', 'Benchmark',
                 'VM', 'Approach', 'Extra', 'Cores', 'InputSize', 'Var']
    data = pd.read_csv(path, sep='\t', names=col_names, skiprows=4)
    col_drop = ['Invocation', 'Iteration', 'Unit', 'Criterion', 'VM', 'Extra', 'Cores', 'InputSize']
    data.drop(col_drop, axis=1, inplace=True)
    data['Var'] = data['Var'].map(lambda x: round((x / 1000)**2, 2))
    data = data.set_index(['Var', 'Approach']).sort_index()
    return [x.drop('Benchmark', axis=1) for _, x in data.groupby('Benchmark')]


def separate_baseline(data: pd.DataFrame, mask: str) -> List[pd.DataFrame]:
    bl = data.xs(mask, level=1, drop_level=False)
    return data.drop(bl.index), bl


def normalize_data(data: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    bl_mean = baseline.groupby('Var')['Value'].mean()
    data_norm = data.copy()
    data_norm['Value'] = data_norm['Value'] / bl_mean
    return data_norm


def mean_and_std(data: pd.DataFrame):
    data = data.copy().groupby(['Var', 'Approach'])
    return data.mean(), data.std(ddof=0)


def configure_plt_style():
    plt.style.use('ggplot')
    # sns.set(style='ticks', palette='Set2')


def plot_data(labels, means_df1, errors_df1, means_df2, errors_df2, appr, titles, filename):
    appr = appr.map({'test-objectteams-classic-38': 'Classic 2020',
                     'test-objectteams-indy-38': 'Polymorphic Dispatch Plans',
                     'test-objectteams-indy-38-deg': 'PDP w/ Degradation'})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 6))
    plot_sub(ax1, labels, means_df1, errors_df1, appr, titles[0], True)
    plot_sub(ax2, labels, means_df2, errors_df2, appr, titles[1], False)
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc=10, bbox_to_anchor=(0., 1., 1., .01), ncol=len(appr),
               fontsize='small', frameon=False, borderaxespad=0.)
    fig.tight_layout()
    plt.savefig(f'{folder}/{filename}.pdf', bbox_inches='tight', pad_inches=0)
    plt.show()


def plot_sub(ax, labels, means, errors, appr, title, ylabel):
    title_fs, label_fs, tick_label_fs = 11, 8, 8
    x = np.arange(len(labels)) * 1.5
    h = [x.to_numpy().flatten() for x in means]
    w = 0.4
    yerr = [x.to_numpy().flatten() for x in errors]
    error_kw = {'elinewidth': 0.5, 'capsize': 1.5}
    if len(appr) == 2:
        ax.bar(x=(x - w/2), height=h[0], width=w, yerr=yerr[0], label=appr[0], error_kw=error_kw)
        ax.bar(x=(x + w/2), height=h[1], width=w, yerr=yerr[1], label=appr[1], error_kw=error_kw)
        if ylabel:
            ax.set_ylabel('Run time factor normalized to Classic 2020', fontsize=label_fs)
    else:
        ax.bar(x=(x - w), height=h[0], width=w, yerr=yerr[0], label=appr[0], error_kw=error_kw, log=True)
        ax.bar(x=x,       height=h[1], width=w, yerr=yerr[1], label=appr[1], error_kw=error_kw, log=True)
        ax.bar(x=(x + w), height=h[2], width=w, yerr=yerr[2], label=appr[2], error_kw=error_kw, log=True)
        if ylabel:
            ax.set_ylabel('Run time in ms', fontsize=label_fs)

    ax.set_xlabel('Millions of iterations', fontsize=label_fs)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.tick_params(labelsize=tick_label_fs)
    t = ax.set_title(title, fontsize=title_fs)


try:
    folder = f'../data/{sys.argv[1]}'
except IndexError:
    with open('../data/latest') as f:
        folder = f'../data/{f.read().split("/")[-1]}'

df1, df2 = load_benchmark_data(f'{folder}/benchmark.data')
# Calculate mean and std
df1_mean, df1_std = mean_and_std(df1)
df2_mean, df2_std = mean_and_std(df2)
# Plot data
configure_plt_style()
iter_vars = df1.index.levels[0]
approaches = df1.index.levels[1]
subfig_titles = ['Static Context', 'Variable Contexts']
plot_data(iter_vars,
          [df1_mean.xs(x, level=1) for x in approaches],
          [df1_std.xs(x, level=1) for x in approaches],
          [df2_mean.xs(x, level=1) for x in approaches],
          [df2_std.xs(x, level=1) for x in approaches],
          approaches,
          subfig_titles,
          'benchmark')

# Separate baseline
bl_mask = 'test-objectteams-classic-38'
df1, df1_bl = separate_baseline(df1, bl_mask)
df2, df2_bl = separate_baseline(df2, bl_mask)
# Normalize
df1_norm = normalize_data(df1, df1_bl)
df2_norm = normalize_data(df2, df2_bl)
# Calculate mean and std
df1_norm_mean, df1_norm_std = mean_and_std(df1_norm)
df2_norm_mean, df2_norm_std = mean_and_std(df2_norm)
# Plot normalized data
approaches = approaches.drop(bl_mask)
plot_data(iter_vars,
          [df1_norm_mean.xs(x, level=1) for x in approaches],
          [df1_norm_std.xs(x, level=1) for x in approaches],
          [df2_norm_mean.xs(x, level=1) for x in approaches],
          [df2_norm_std.xs(x, level=1) for x in approaches],
          approaches,
          subfig_titles,
          'benchmark_normalized')
