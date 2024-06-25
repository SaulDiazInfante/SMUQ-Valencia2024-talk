"""Main function to obtain the figures"""
import sys
import os
import numpy as np
wd = os.getcwd()
sys.path.append('wd')
from vsm_figures import VsmFigures
from vsm_animation import VsmAnimator
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from matplotlib.animation import FFMpegWr
import seaborn as sns
# print(wd)
os.chdir('..')
wd = os.getcwd()
#print(wd)
fig = plt.figure()
wd = wd + '/data/'
vs_fig = VsmFigures(fig, wd)
vs_fig.load_data()

ax_states, fig_states = vs_fig.plot_states()
ax_policy, fig_policy = vs_fig.plot_policies()
fig, ax1, ax2, ax3, ax4 = vs_fig.dash_plot()
N = vs_fig.df_ref_par['N'][0]
x_lim = vs_fig.df_ref_sol.index.max()
y_lim = N * vs_fig.df_ref_sol['I_S'].max()
vs_an = VsmAnimator(fig, ax1, ax2, ax3, ax4, x_lim, y_lim, wd)
vs_an.load_data()

anim = animation.FuncAnimation(
    fig,
    vs_an,
    init_func=vs_an.start,
    frames=len(vs_an.df_ref_sol.index),
    interval=1,
     repeat=False
)

# metadata = dict(title='duffing oscillator', artist='SDIV')
# writer = FFMpegWriter(fps=16, metadata=metadata)
# anim.save('duffing_animation.mp4', writer=writer)


# with writer.saving(fig, "duffing_animation.mp4", 100):
#     for idx, t in enumerate(df_current_sol['time']):
#         print(idx, t)
#         ud.__call__(idx)
#         writer.grab_frame()
