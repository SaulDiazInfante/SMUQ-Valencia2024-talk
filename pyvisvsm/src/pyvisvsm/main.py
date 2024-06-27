"""
    Main function to obtain the figures
"""
import matplotlib.pyplot as plt
from pyvisvsm.pyvisvsm import VsmFigures, VsmAnimator


fig = plt.figure()
vs_fig = VsmFigures(fig)
vs_fig.load_data()
ax_states, fig_states = vs_fig.plot_states()
ax_policy, fig_policy = vs_fig.plot_policies()
fig, ax1, ax2, ax3, ax4 = vs_fig.dash_plot()
plt.show()
vs_an = VsmAnimator(fig, ax1, ax2, ax3, ax4)
vs_an.load_data()
vs_an.record_animation()
