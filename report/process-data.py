import sys
from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns


def load_benchmark_data(path: str) -> List[pd.DataFrame]:
    # Read data
    col_names = ['Invocation', 'Iteration', 'Value', 'Unit', 'Criterion', 'Benchmark',
                 'VM', 'Approach', 'Extra', 'Cores', 'InputSize', 'Var']
    data = pd.read_csv(path, sep='\t', names=col_names, skiprows=4)
    print(f'Run time: {data["Value"].sum() / 1000 / 60} minutes')
    # Drop first iterations
    data = data[data['Iteration'] != 1]
    # Drop unnecessary columns
    col_drop = ['Invocation', 'Iteration', 'Unit', 'Criterion', 'VM', 'Extra', 'Cores', 'InputSize']
    data.drop(col_drop, axis=1, inplace=True)
    # Map innerIterations values
    data['Var'] = data['Var'].map(lambda x: round((x / 1000)**2, 2))
    data = data.set_index(['Var', 'Approach']).sort_index()
    # Return separate df for each benchmark
    return [x.drop('Benchmark', axis=1) for _, x in data.groupby('Benchmark')]


def mean_and_errors(data: pd.DataFrame) -> List[pd.DataFrame]:
    grouped = data.groupby(['Var', 'Approach'])
    return grouped.mean(), grouped.std(ddof=0)


def separate_baseline(data: pd.DataFrame, mask: str) -> List[pd.DataFrame]:
    bl = data.xs(mask, level=1, drop_level=False)
    return data.drop(bl.index), bl


def normalize_data(data: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    bl_mean = baseline.groupby(level=0).mean()
    return data / bl_mean


def configure_plt_style():
    plt.style.use('ggplot')
    plt.rcParams['font.family'] = 'Open Sans'
    # sns.set(style='ticks', palette='Set2')


def plot_data(labels: pd.Index, means: list[pd.DataFrame], errors: list[pd.DataFrame],
              appr: pd.Index, title: str, filename: str):
    appr = appr.map({'test-objectteams-classic-38': 'Classic 2020',
                     'test-objectteams-indy-38': 'Polymorphic Dispatch Plans',
                     'test-objectteams-indy-38-deg': 'PDP w/ Degradation'})
    x = np.arange(len(labels)) * 1.5
    y = [x.to_numpy().flatten() - 1 for x in means]
    w = 1.2 / len(appr)
    yerr = [x.to_numpy().flatten() for x in errors]
    error_kw = {'elinewidth': 0.8, 'capsize': 10 / len(appr)}
    label_fs, tick_label_fs = 10, 8
    fig, ax = plt.subplots(figsize=(7, 5))

    if len(appr) == 2:
        ax.bar(x=(x - w/2), height=y[0], width=w, bottom=1, yerr=yerr[0], label=appr[0], error_kw=error_kw)
        ax.bar(x=(x + w/2), height=y[1], width=w, bottom=1, yerr=yerr[1], label=appr[1], error_kw=error_kw)
        ax.set_ylabel('Run time factor normalized to Classic 2020', fontsize=label_fs)
    else:
        ax.bar(x=(x - w), height=y[0], width=w, yerr=yerr[0], label=appr[0], error_kw=error_kw, log=True)
        ax.bar(x=x,       height=y[1], width=w, yerr=yerr[1], label=appr[1], error_kw=error_kw, log=True)
        ax.bar(x=(x + w), height=y[2], width=w, yerr=yerr[2], label=appr[2], error_kw=error_kw, log=True)
        ax.set_ylabel('Run time in ms', fontsize=label_fs)

    ax.set_xlabel('Millions of iterations', fontsize=label_fs)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.tick_params(labelsize=tick_label_fs)
    ax.legend(loc=10, bbox_to_anchor=(0., 1., 1., .102), ncol=len(appr),
              fontsize='small', frameon=False, borderaxespad=0.)
    ax.set_title(title, pad=30)
    fig.tight_layout()
    plt.savefig(f'{folder}/{filename}.pdf')
    plt.show()


if len(sys.argv) > 1:
    folder = f'../data/{sys.argv[1]}'
else:
    with open('../data/latest') as f:
        folder = f'../data/{f.read().split("/")[-1]}'

df1, df2 = load_benchmark_data(f'{folder}/benchmark.data')
# Calculate mean and std
df1_mean, df1_std = mean_and_errors(df1)
df2_mean, df2_std = mean_and_errors(df2)
# Plot data
configure_plt_style()
iter_vars = df1.index.levels[0]
approaches = df1.index.levels[1]
titles = ['Static Context Benchmark', 'Variable Contexts Benchmark']
filenames = ['benchmark_static', 'benchmark_variable',
             'benchmark_static_normalized', 'benchmark_variable_normalized']
plot_data(iter_vars,
          [df1_mean.xs(x, level=1) for x in approaches],
          [df1_std.xs(x, level=1) for x in approaches],
          approaches,
          titles[0],
          filenames[0])
plot_data(iter_vars,
          [df2_mean.xs(x, level=1) for x in approaches],
          [df2_std.xs(x, level=1) for x in approaches],
          approaches,
          titles[1],
          filenames[1])

# Separate baseline
bl_mask = 'test-objectteams-classic-38'
df1, df1_bl = separate_baseline(df1, bl_mask)
df2, df2_bl = separate_baseline(df2, bl_mask)
# Normalize
df1_norm = normalize_data(df1, df1_bl)
df2_norm = normalize_data(df2, df2_bl)
# Calculate mean and std
df1_norm_mean, df1_norm_std = mean_and_errors(df1_norm)
df2_norm_mean, df2_norm_std = mean_and_errors(df2_norm)
# Plot normalized data
approaches = approaches.drop(bl_mask)
plot_data(iter_vars,
          [df1_norm_mean.xs(x, level=1) for x in approaches],
          [df1_norm_std.xs(x, level=1) for x in approaches],
          approaches,
          titles[0],
          filenames[2])
plot_data(iter_vars,
          [df2_norm_mean.xs(x, level=1) for x in approaches],
          [df2_norm_std.xs(x, level=1) for x in approaches],
          approaches,
          titles[1],
          filenames[3])
