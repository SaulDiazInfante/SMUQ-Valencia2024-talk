"""_summary_
"""
import pandas as pd
import matplotlib.pyplot as plt

#
plt.style.use("dark_background")
#
DATA_FOLDER = "../data"
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
N = par["N"][0]
df_m_states = N * df_m[states]
df_l_states = N * df_l[states]
df_u_states = N * df_u[states]
#
figure_states, axes_states = plt.subplots(
    figsize=(14, 8.7),
    nrows=2,
    ncols=2
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
    
axes_states[0][0].fill_between(
    df_u_states.index,
    df_l_states['I_S'],
    df_u_states['I_S'],
    cmap='Dark2',
    alpha=0.5
)
axes_states[0][1].fill_between(
    df_u_states.index,
    df_l_states['D'],
    df_u_states['D'],
    cmap='Dark2',
    alpha=0.5
)
axes_states[1][0].fill_between(
    df_u_states.index,
    df_l_states['V'],
    df_u_states['V'],
    cmap='Dark2',
    alpha=0.5
)
axes_states[1][1].fill_between(
    df_u_states.index,
    df_l_states['X_vac'],
    df_u_states['X_vac'],
    cmap='Dark2',
    alpha=0.5
)
axes_states[0][0].set_ylabel(r'$I_S$')
axes_states[0][1].set_ylabel(r'$D$')
axes_states[1][0].set_ylabel(r'$V$')
axes_states[1][1].set_ylabel(r'$X_{vac}$')
plt.savefig("ci_states.svg", dpi=300)
plt.show()
