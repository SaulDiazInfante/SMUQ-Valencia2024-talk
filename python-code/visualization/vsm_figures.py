import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

class vsmFigures:
  
    def __init__(self) -> None:
        self.data_folder = "./python-code/data"
        self.df_ref_sol_path = "./python-code/data/df_solution.csv"
        self.df_ref_par_path = "./python-code/data/parameters_model.json"
        self.time_line = np.empty(1000)
        self.df_ref_sol = pd.DataFrame()
        self.df_ref_par = pd.DataFrame()
        self.time_line_date_in_days = np.empty(1000)
        self.start_date='2021-01-01'
        self.df_states = pd.DataFrame()
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
        self.policy = np.empty(0)


    def load_data(self): 
        self.df_ref_sol = pd.read_csv(self.df_ref_sol_path)
        self.df_ref_par = pd.read_json(self.df_ref_par_path)
        self.time_line = self.df_ref_sol["time"]
        self.start_date='2021-01-01'
        self.time_line_date_in_days = pd.to_datetime(self.start_date) + \
            pd.to_timedelta(self.time_line.values, unit='D')
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
        self.policy = [
               'K_stock',
               'action',
               'opt_policy'
        ]
        self.df_states = self.df_ref_par['N'][0] * self.df_ref_sol[self.states]
        self.df_policy = self.df_ref_sol[self.policy]
        self.df_policy['K_stock'] = self.df_ref_par['N'][0] * self.df_policy['K_stock']
        
        
    def plot_states(self):
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
        
        plt.savefig("det_policy.svg", dpi=300)
        figure_policy.tight_layout()
        return figure_policy, axes_policy

vs = vsmFigures()
vs.load_data()

ax_states, fig_states = vs.plot_states()
ax_policy, fig_policy = vs.plot_policies()
