"""_summary

"""

import pandas as pd
import matplotlib.pyplot as plt

#
plt.style.use("dark_background")
#

DATA_FOLDER = "./data"
df_m = pd.read_csv("./data/df_median.csv")
df_l = pd.read_csv("./data/df_lower_q.csv")
df_u = pd.read_csv("./data/df_upper_q.csv")
par = pd.read_json("./data/parameters_model.json")
time_line = df_m["time"]
START_DATE='2021-01-01'
time_line_date_in_days = pd.to_datetime(START_DATE) + \
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
N = par["N"][0] / 1e03
df_m_states = N * df_m[states]
df_l_states = N * df_l[states]
df_u_states = N * df_u[states]
#
#
## Incidence figures cumsum()
#
#
figure_Is, axes_Is = plt.subplots(
    figsize=(14, 8.7),
    nrows=1,
    ncols=1
)
axes_Is.set_ylabel(r'Cumulative Incidence')
df_l_states['I_S'].cumsum().plot(
    ax=axes_Is,
    sharex=True,
    lw=1,
    color='red',
    label="",
    legend=False
)
df_u_states['I_S'].cumsum().plot(
    ax=axes_Is, 
    sharex=True,
    lw=1,
    color='red',
    label="",
    legend=False
)
# Incidence
plt.fill_between(df_l_states.index,
    df_l_states['I_S'].cumsum(),
    df_u_states['I_S'].cumsum(),
    fc='pink',
    alpha=0.5,
    figure=figure_Is
)
df_m_states['I_S'].cumsum().plot(
    ax=axes_Is,
    sharex=True,
    lw=2,
    color='red',
    label="",
    legend=False
)
axins = axes_Is.inset_axes([0.3, 0.7, 0.1, 0.161])
axins.plot(
    df_m_states['I_S'].index,
    df_m_states['I_S'].cumsum(),
    color='red'
)
axins.plot(
    df_m_states['I_S'].index,
    df_l_states['I_S'].cumsum(),
    color='red'
)
axins.plot(
    df_m_states['I_S'].index,
    df_u_states['I_S'].cumsum(),
    color='red'
)
axins.fill_between(df_l_states.index,
    df_l_states['I_S'].cumsum(),
    df_u_states['I_S'].cumsum(),
    fc='pink',
    alpha=0.5,
    figure=figure_Is
)
x1 = pd.Timestamp('2021-10-01 12:28:48')
x2 = pd.Timestamp('2021-11-17 00:00:00')
y1, y2 = 1.6e5, 2.4e5
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
# axins.set_yticklabels([])
axes_Is.indicate_inset_zoom(axins, edgecolor="white")
plt.savefig("cumulative_symptomatic_incidence.svg", dpi=300)
plt.show()
