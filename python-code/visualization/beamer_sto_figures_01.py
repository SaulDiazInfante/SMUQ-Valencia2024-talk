"""
This script returns the plots with the confidence band at 95%
of the symptomatic incidence, dynamics of random stock and its
corresponding calculated vaccination ratio
"""
import pandas as pd
import matplotlib.pyplot as plt
#
plt.style.use("dark_background")
#
DATA_FOLDER = "./data/"
DATA_SUFFIX = "(2024-05-15_20:55).csv"

df_m = pd.read_csv(f"{DATA_FOLDER}df_median{DATA_SUFFIX}")
df_l = pd.read_csv(f"{DATA_FOLDER}df_lower_q{DATA_SUFFIX}")
df_u = pd.read_csv(f"{DATA_FOLDER}df_upper_q{DATA_SUFFIX}")
par = pd.read_json(f"{DATA_FOLDER}parameters_model.json")
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
#
## Incidence figures
#
#
box = dict(facecolor='yellow', pad=5, alpha=0.2)

figure_Is, axes_Is = plt.subplots(
    figsize=(14, 8.7),
    nrows=1,
    ncols=1
)
df_l_states['I_S'].plot(
    ax=axes_Is,
    sharex=True,
    lw=1,
    label="",
    color='red',
    legend=False
)
df_u_states['I_S'].plot(
    ax=axes_Is,
    sharex=True,
    lw=1,
    color='red',
    label="",
    legend=False
)
# Incidence
plt.fill_between(
    df_l_states.index,
    df_l_states['I_S'],
    df_u_states['I_S'],
    fc='pink',
    alpha=0.5,
    figure=figure_Is
)
df_m_states['I_S'].plot(
    ax=axes_Is,
    sharex=True,
    lw=2,
    color='red',
    label="",
    legend=False
)
axes_Is.set_ylabel(r'Symptomatic Incidence $I_S$ (No. cases per day)', bbox=box)
plt.savefig("symptomatic_incidence.svg", dpi=300)
plt.show()
#
# Policy figures
#
figure_policy, axes_policy = plt.subplots(
    figsize=(14, 8.7),
    nrows=2,
    ncols=1
)

stock_policy = ['K_stock', 'action']
df_m_stock_policy = N * df_m[stock_policy]
df_l_stock_policy = N * df_l[stock_policy]
df_u_stock_policy = N * df_u[stock_policy]

axes_policy[0].fill_between(
    df_l_stock_policy.index,
    df_l_stock_policy['K_stock'],
    df_u_stock_policy['K_stock'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_policy
)
axes_policy[0].set_ylabel('Number of vaccine doses $K_t$', bbox=box)
#
#
axes_policy[1].fill_between(
    df_l_stock_policy.index,
    df_l_stock_policy['action'],
    df_u_stock_policy['action'],
    cmap='Dark2',
    alpha=0.5,
    figure=figure_policy,
)
axes_policy[1].set_ylabel('Vaccination rate $\Psi_V$ (Number of jabs per day)', bbox=box)

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

df_m_stock_policy.plot(
    colormap='Dark2',
    subplots=True,
    layout=(2, 1),
    ax=axes_policy,
    label = "median",
    sharex=True,
    legend=False,
    lw=2,
    color="red"
)

figure_policy.tight_layout()
plt.savefig("ci_stock_action.svg", dpi=300)
plt.show()
