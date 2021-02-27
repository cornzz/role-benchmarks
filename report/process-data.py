from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_benchmark_data(path: str) -> List[pd.DataFrame]:
    col_names = ['Invocation', 'Iteration', 'Value', 'Unit', 'Criterion', 'Benchmark',
                 'VM', 'Approach', 'Extra', 'Cores', 'InputSize', 'Var']
    data = pd.read_csv(path, sep='\t', names=col_names, skiprows=4)
    col_drop = ['Invocation', 'Iteration', 'Unit', 'Criterion', 'VM', 'Extra', 'Cores', 'InputSize']
    data.drop(col_drop, axis=1, inplace=True)
    data['Var'] = data['Var'].map(lambda x: round((x / 1000)**2, 2))
    return [x.drop('Benchmark', axis=1) for _, x in data.groupby('Benchmark')]


def separate_baseline(data: pd.DataFrame, mask: str) -> List[pd.DataFrame]:
    return data[data['Approach'] != mask], data[data['Approach'] == mask]


def normalize_data(data: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    bl_mean = baseline.groupby('Var')['Value'].mean()
    data_norm = data.copy().set_index(['Var', 'Approach']).sort_index()
    data_norm['Value'] = data_norm['Value'] / bl_mean
    return data_norm


def mean_and_std(data: pd.DataFrame):
    data = data.copy().groupby(['Var', 'Approach'])
    return data.mean(), data.std()


def plot_data(labels, means, errors, appr, title):
    x = np.arange(len(labels))
    h = [x.to_numpy().flatten() for x in means]
    w = 0.4
    yerr = [x.to_numpy().flatten() for x in errors]
    cs = 2.5
    fig, ax = plt.subplots()

    ax.bar(x=(x - w/2), height=h[0], width=w, yerr=yerr, label=appr[0], capsize=cs)
    ax.bar(x=(x + w/2), height=h[1], width=w, yerr=yerr, label=appr[1], capsize=cs)

    ax.set_ylabel('Runtime factor normalized to Classic 2020')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_title(title)
    # fig.tight_layout()
    plt.savefig(f'{title}.svg')
    plt.show()


df1, df2 = load_benchmark_data('../data/001-2ab4f810/benchmark.data')
# Separate baseline
bl_mask = 'test-objectteams-classic-38'
df1, df1_bl = separate_baseline(df1, bl_mask)
df2, df2_bl = separate_baseline(df2, bl_mask)
# Normalize
df1_norm = normalize_data(df1, df1_bl)
df2_norm = normalize_data(df2, df2_bl)
# Calculate mean and std
df1_mean, df1_std = mean_and_std(df1_norm)
df2_mean, df2_std = mean_and_std(df2_norm)
# Plot data
approaches = df1_mean.index.levels[1]
plot_data(df1_mean.index.levels[0],
          [df1_mean.xs(x, level=1) for x in approaches],
          [df1_std.xs(x, level=1) for x in approaches],
          approaches,
          'Static Context Benchmark')
plot_data(df2_mean.index.levels[0],
          [df2_mean.xs(x, level=1) for x in approaches],
          [df2_std.xs(x, level=1) for x in approaches],
          approaches,
          'Variable Contexts Benchmark')
