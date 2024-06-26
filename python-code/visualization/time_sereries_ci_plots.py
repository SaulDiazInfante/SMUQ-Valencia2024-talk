from cProfile import label
from matplotlib import figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight')

#TODO: convert to timeseries and plot
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
df_m_states = N * df_m[states]
df_l_states = N * df_l[states]
df_u_states = N * df_u[states]
#
figure_states, axes_states = plt.subplots(
    figsize=(14, 8.7),
    nrows=4,
    ncols=1
)
df_m_states.plot(
    subplots=True,
    layout=(2, 2),
    ax=axes_states, 
    sharex=True,
    label="median",
    lw=1, 
    legend=False
    )
df_l_states.plot(
    subplots=True,
    layout=(2, 2),
    ax=axes_states, 
    sharex=True,
    lw=1,
    label = "",
    legend=False
    )
df_u_states.plot(
    subplots=True,
    layout=(2, 2),
    ax=axes_states, 
    sharex=True,
    lw=1,
    label="",
    legend=False
    )
#plt.legend(False)
plt.show()

figure_policy, axes_policy = plt.subplots(
    figsize=(14, 8.7),
    nrows=2,
    ncols=1
)
figure_policy.tight_layout()
stock_policy = ['K_stock', 'action']
df_m_stock_policy = N * df_m[stock_policy]
df_l_stock_policy = N * df_l[stock_policy]
df_u_stock_policy = N * df_u[stock_policy]

plt.fill_between(df_l_stock_policy.index,
    df_l_stock_policy['K_stock'],
    df_u_stock_policy['K_stock'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_policy
)
df_l_stock_policy.plot(
    subplots=True,
    layout=(2, 1),
    ax=axes_policy,
    label = "",
    sharex=True,
    legend=False,
    lw=1
)
df_u_stock_policy.plot(
    subplots=True,
    layout=(2, 1),
    ax=axes_policy,
    label="",
    sharex=True,
    legend=False, 
    lw=1
)

plt.fill_between(df_l_stock_policy.index,
    df_l_stock_policy['action'],
    df_u_stock_policy['action'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_policy,
)

df_m_stock_policy.plot(
    colormap='Dark2',
    subplots=True,
    layout=(2, 1),
    ax=axes_policy,
    label = "median",
    sharex=True,
    legend=False,
    lw=1
    )
plt.show()