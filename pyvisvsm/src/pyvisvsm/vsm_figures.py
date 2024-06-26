import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

class VsmFigures(object):
    """_summary_
    Class for reproduce figures: States, policies and dashboards.
    """

    def __init__(self, fig, data_dir="./data/") -> None:
        self.fig = fig
        sns.set_theme(context="paper")
        self.data_folder = data_dir
        self.df_ref_sol_path = data_dir + "df_solution.csv"
        self.df_ref_par_path = data_dir + "parameters_model.json"
        self.time_line = np.empty(1000)
        self.df_ref_sol = pd.DataFrame()
        self.df_ref_par = pd.DataFrame()
        self.time_line_date_in_days = np.empty(1000)
        self.start_date = '2021-01-01'
        self.df_states = pd.DataFrame()
        self.df_policy = pd.DataFrame()
        self.states = [
            'S',
            'E',
            'I_S',
            # 'I_A',
            'D',
            # 'R',
            'V',
            'X_vac',
            #   'K_stock',
            #   'action'
        ]
        self.policy = [
            'K_stock',
            'action',
            'opt_policy'
        ]

        self.y_k_t_lim = 0.0
        self.y_a_t_lim = 0.0
        self.y_op_t_lim = 0.0
        self.x_0_date = np.empty(1, dtype=object)
        self.x_f_date = np.empty(1, dtype=object)
        self.y_i_s_lim = 0.0

    def load_data(self):
        """_summary_
        """
        self.df_ref_sol = pd.read_csv(self.df_ref_sol_path)
        self.df_ref_par = pd.read_json(self.df_ref_par_path)
        self.time_line = self.df_ref_sol["time"]
        self.start_date = '2021-01-01'
        self.time_line_date_in_days = (
            pd.to_datetime(self.start_date)
            + pd.to_timedelta(
                self.time_line.values,
                unit='D'
            )
        )
        self.df_ref_sol["date"] = self.time_line_date_in_days
        self.df_ref_sol = self.df_ref_sol.set_index('date')
        self.states = [
            'S',
            'E',
            'I_S',
            #'I_A',
            'D',
            #'R',
            'V',
            'X_vac',
            #   'K_stock',
            #   'action'
        ]

        N = self.df_ref_par['N'][0]
        self.df_states = N * self.df_ref_sol.loc[:, self.states]
        self.df_policy = self.df_ref_sol[self.policy]
        self.df_policy.loc[:, 'K_stock'] = N * self.df_policy.loc[:, 'K_stock']
        self.df_policy.loc[:, 'action'] = N * self.df_policy.loc[:, 'action']
        self.x_0_date = self.df_ref_sol.index.min()
        self.x_f_date = self.df_ref_sol.index.max()
        self.y_k_t_lim = self.df_policy['K_stock'].max()
        self.y_a_t_lim = 1.2 * self.df_policy['action'].max()
        self.y_op_t_lim = 1.2
        self.y_i_s_lim = 1.1 * N * self.df_ref_sol['I_S'].max()

    def plot_states(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        figure_states, axes_states = plt.subplots(
            figsize=(14, 8.7),
            nrows=2,
            ncols=3
        )
        self.df_states.plot(
            subplots=True,
            layout=(2, 2),
            ax=axes_states,
            sharex=True,
            label="deterministic",
            lw=1,
            legend=False
        )
        axes_states[0, 0].set_ylabel(r'$S$')
        axes_states[0, 1].set_ylabel(r'$E$')
        axes_states[0, 2].set_ylabel(r'$I_S$')
        axes_states[1, 0].set_ylabel(r'$D$')
        axes_states[1, 1].set_ylabel(r'$V$')
        axes_states[1, 2].set_ylabel(r'$X_{vac}$')

        plt.savefig("det_states.svg", dpi=300)
        figure_states.tight_layout()
        return figure_states, axes_states

    def plot_policies(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        figure_policy, axes_policy = plt.subplots(
            figsize=(14, 8.7),
            nrows=3,
            ncols=1
        )

        self.df_policy.plot(
            subplots=True,
            layout=(3, 1),
            ax=axes_policy,
            sharex=True,
            label="deterministic",
            lw=1,
            legend=False
        )
        axes_policy[0].set_ylabel(r'$K_{stock}$')
        axes_policy[1].set_ylabel(r'$a_t$')
        axes_policy[2].set_ylabel(r'$\pi ^{\star}$')
        figure_policy.tight_layout()
        plt.savefig("det_policy.svg", dpi=300)
        return figure_policy, axes_policy

    def dash_plot(self):
        """_summary_

        Returns:
        _type_: _description_
        """

        fig = plt.figure(figsize=(12.11, 7.7))
        ax1 = plt.subplot2grid((3, 9), (0, 0), colspan=3)
        ax2 = plt.subplot2grid((3, 9), (1, 0), colspan=3)
        ax3 = plt.subplot2grid((3, 9), (2, 0), colspan=3)
        ax4 = plt.subplot2grid(
            (3, 9), (0, 4), colspan=5, rowspan=3
        )
        ax1.plot(self.df_policy.index, self.df_policy['K_stock'])
        ax1.tick_params(labelbottom=False)
        ax2.plot(self.df_policy.index, self.df_policy['action'])
        ax2.tick_params(labelbottom=False)

        ax1.set_ylabel(r'$K_{stock}(t) \ $ (vaccine-jabs)')
        ax2.set_ylabel(r'$a_t \ $ vaccine-jabs/day')
        ax3.set_ylabel(r'$\pi ^{\star}$ current stock fraction')
        plt.draw()
        ax3.plot(
            self.df_policy.index, self.df_policy['opt_policy']
        )

        ax3_labels = ax3.get_xticks()
        ax3.set_xticks(ax3_labels)
        ax3.set_xticklabels(
            ax3.get_xticklabels(),
            rotation=45, ha='right'
        )
        ax3.set_xlabel(r'date')
        ax4.plot(self.df_states.index, self.df_states['I_S'])
        ax4.set_ylabel(r'$I_S$ New confirmed cases')
        ax4.set_xlabel(r'date')
        ax4_labels = ax4.get_xticks()
        ax4.set_xticks(ax4_labels)
        ax4.set_xticklabels(
            ax4.get_xticklabels(),
            rotation=45, ha='right'
        )
        fig.tight_layout()
        plt.savefig("dash_plot.svg", dpi=300)
        return fig, ax1, ax2, ax3, ax4
