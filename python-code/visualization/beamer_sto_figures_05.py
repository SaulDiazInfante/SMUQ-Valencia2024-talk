from cProfile import label
from matplotlib import figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import seaborn as sns
plt.style.use("dark_background")

# TODO: convert to timeseries and plot
data_folder = "../data"
df_m = pd.read_csv("../data/df_median.csv")
df_l = pd.read_csv("../data/df_lower_q.csv")
df_u = pd.read_csv("../data/df_upper_q.csv")
par = pd.read_json("../data/parameters_model.json")
time_line = df_m["time"]
start_date='2021-01-01'
time_line_date_in_days = pd.to_datetime(start_date) + \
    pd.to_timedelta(time_line.values, unit='D')
df_m["date"] = time_line_date_in_days
df_l["date"] = time_line_date_in_days
df_u["date"] = time_line_date_in_days

df_m = df_m.set_index('date')
df_l = df_l.set_index('date')
df_u = df_u.set_index('date')
states = [
    # 'S',
    # 'E',
    'I_S',
    # 'I_A',
    'D',    
    # 'R', 
    'V', 
    'X_vac'
    #'K_stock',
    #'action'
]
N = par["N"][0]
#
figure_action, axes_action = plt.subplots(
    figsize=(14, 8.7),
    nrows=1,
    ncols=1
)
action = ['action']
df_m_action = N * df_m[action]
df_l_action = N * df_l[action]
df_u_action = N * df_u[action]
axes_action.set_ylabel(r'Vaccination rate')
#
plt.fill_between(df_l_action.index,
    df_l_action['action'],
    df_u_action['action'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_action
)
df_l_action.plot(
    ax=axes_action,
    label = "",
    sharex=True,
    legend=False,
    lw=1,
    color='blue'
)
df_u_action.plot(
    ax=axes_action,
    label="",
    sharex=True,
    legend=False, 
    lw=1, 
    color='blue'
)
df_m_action.plot(
    ax=axes_action,
    label="",
    sharex=True,
    legend=False, 
    lw=2
)
axes_action.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K')
)
figure_action.tight_layout()
plt.savefig("action.svg", dpi=300)
plt.show()
