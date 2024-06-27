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
figure_stock, axes_stock = plt.subplots(
    figsize=(14, 8.7),
    nrows=1,
    ncols=1
)
stock = ['K_stock']
df_m_stock = N * df_m[stock]
df_l_stock = N * df_l[stock]
df_u_stock = N * df_u[stock]
axes_stock.set_ylabel(r'Vaccine stock')
#
plt.fill_between(df_l_stock.index,
    df_l_stock['K_stock'],
    df_u_stock['K_stock'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_stock
)
df_l_stock.plot(
    ax=axes_stock,
    label = "",
    sharex=True,
    legend=False,
    lw=1,
    color='blue'
)
df_u_stock.plot(
    ax=axes_stock,
    label="",
    sharex=True,
    legend=False, 
    lw=1, 
    color='blue'
)
df_m_stock.plot(
    ax=axes_stock,
    label="",
    sharex=True,
    legend=False, 
    lw=2
)
axes_stock.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K')
)
figure_stock.tight_layout()
plt.savefig("stock.svg", dpi=300)
plt.show()
