"""
    Main function to obtain the figures
"""
import os
from sys import path
from vsm_animation import VsmAnimator
from vsm_figures import VsmFigures


# import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

path.append('/home/saul/Insync/sauld@cimat.mx/Google Drive/UNISON/Ponencias/2024/SMUQ-Valencia2024-talk/python-code/visualization')

wd = os.getcwd()
wd = wd + '/data/'
path.append(wd)


# print(wd)
# os.chdir('..')

fig = plt.figure()
vs_fig = VsmFigures(fig)
vs_fig.load_data()
N = vs_fig.df_ref_par['N'][0]
x_lim = vs_fig.df_ref_sol.index.max()
y_lim = N * vs_fig.df_ref_sol['I_S'].max()
ax_states, fig_states = vs_fig.plot_states()
ax_policy, fig_policy = vs_fig.plot_policies()
fig, ax1, ax2, ax3, ax4 = vs_fig.dash_plot()
vs_an = VsmAnimator(fig, ax1, ax2, ax3, ax4, x_lim, y_lim)
vs_an.load_data()
vs_an.record_animation()
