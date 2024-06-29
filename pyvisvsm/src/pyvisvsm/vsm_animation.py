import sys
import numpy as np
# sys.path.append('visualization')
from vsm_figures import VsmFigures
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import animation
from alive_progress import alive_bar


class VsmAnimator(VsmFigures):
    """_summary_

    Args:
        VsmFigures (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(
        self,
        data_dir="./data/"
    ):
        """_summary_
        Parameters
        ----------
        data_dir : str
            Path to data.
        
        Returns
        -------
        
        Examples
        --------
        >>> 
        vs = VsmAnimator()
        """

        super(VsmAnimator, self).__init__(data_dir)
        self.fig = plt.figure(figsize=(12.11, 7.7))
        self.ax1 = plt.subplot2grid((3, 9), (0, 0), colspan=3)
        self.ax2 = plt.subplot2grid((3, 9), (1, 0), colspan=3)
        self.ax3 = plt.subplot2grid((3, 9), (2, 0), colspan=3)
        self.ax4 = plt.subplot2grid(
            (3, 9), (0, 4), colspan=5, rowspan=3
        )
        self.metadata = dict(title='Vaccine Stock Management', artist='SDIV')
        self.ax1.tick_params(labelbottom=False)
        self.ax2.tick_params(labelbottom=False)

        self.ax1.set_ylabel(r'$K_{stock}(t) \ $ (vaccine-jabs)')
        self.ax2.set_ylabel(r'$a_t \ $ vaccine-jabs/day')
        self.ax3.set_ylabel(r'$\pi ^{\star}$ current stock fraction')
        self.load_data()
        self.ax1.set_xlim(self.x_0_date, self.x_f_date)
        self.ax2.set_xlim(self.x_0_date, self.x_f_date)
        self.ax3.set_xlim(self.x_0_date, self.x_f_date)
        self.ax4.set_xlim(self.x_0_date, self.x_f_date)

        ax3_labels = self.ax3.get_xticks()
        self.ax3.set_xticks(ax3_labels)
        self.ax3.set_xticklabels(
            self.ax3.get_xticklabels(),
            rotation=45, ha='right'
        )
        self.ax3.set_xlabel(r'date')
        self.ax4.set_ylabel(r'$I_S$ New confirmed cases')
        self.ax4.set_xlabel(r'date')

        ax4_labels = self.ax4.get_xticks()
        self.ax4.set_xticks(ax4_labels)
        self.ax4.set_xticklabels(
            self.ax4.get_xticklabels(),
            rotation=45, ha='right'
        )

        self.ax1.set_ylabel(r'$K_{stock}(t)$')
        self.ax1.set_xlabel(r'$date$')
        self.ax1.set_title('Policy')

        self.ax2.set_ylabel(r'$a_t$ action')
        self.ax2.set_xlabel(r'$date$')

        self.ax3.set_ylabel(r'$y(t)$')
        self.ax3.set_xlabel(r'$x(t)$')

        ax3_labels = self.ax3.get_xticks()
        self.ax3.set_xticks(ax3_labels)
        self.ax3.set_xticklabels(
            self.ax3.get_xticklabels(),
            rotation=45, ha='right'
        )

        self.line1, = self.ax1.plot([], [], 'k-')
        self.line2, = self.ax2.plot([], [], 'k-')
        self.line3, = self.ax3.plot([], [], 'k-')
        self.line4, = self.ax4.plot([], [], 'k-')

        self.filled_marker_style = dict(
            marker='o',
            markersize=10,
            color='darkgrey',
            markerfacecolor='tab:blue',
            markerfacecoloralt='lightsteelblue',
            markeredgecolor='black',
            fillstyle='left'
        )

    def __call__(self, idx):
        """_summary_

        Args:
            idx (_type_): _description_
        """
        self.ax1.clear()
        self.ax1.plot(
            self.df_policy.index[0:idx],
            self.df_policy['K_stock'][0:idx]
        )
        self.ax1.plot(
            self.df_policy.index[idx],
            self.df_policy['K_stock'].iloc[idx],
            marker='o',
            ms=5
        )
        # self.ax1.set_ylabel(r'$K_{stock}$')
        self.ax1.set_xlim(self.x_0_date, self.x_f_date)
        self.ax1.set_ylim(0, self.y_k_t_lim)

        self.ax2.clear()
        self.ax2.plot(
            self.df_policy.index[0:idx],
            self.df_policy['action'].iloc[0:idx])
        self.ax2.set_xlim(self.x_0_date, self.x_f_date)
        self.ax2.set_ylim(0, self.y_a_t_lim)
        self.ax2.plot(
            self.df_policy.index[idx],
            self.df_policy['action'].iloc[idx],
            marker='o',
            ms=5
        )

        self.ax3.clear()
        self.ax3.plot(
            self.df_policy.index[0:idx],
            self.df_policy['opt_policy'].iloc[0:idx]
        )
        self.ax3.set_xlim(self.x_0_date, self.x_f_date)
        self.ax3.set_ylim(0, self.y_op_t_lim)
        self.ax3.plot(
            self.df_policy.index[idx],
            self.df_policy['opt_policy'].iloc[idx],
            marker='o',
            ms=5
        )
        ax3_labels = self.ax3.get_xticks()
        self.ax3.set_xticks(ax3_labels)
        self.ax3.set_xticklabels(
            self.ax3.get_xticklabels(),
            rotation=90, ha='right'
        )

        # self.ax3.set_ylabel(r'$\pi$ faction of total stock')

        # self.ax4.set_ylabel(r'$I_S$ New reported cases')
        self.ax4.clear()
        self.ax4.set_xlim(self.x_0_date, self.x_f_date)
        self.ax4.set_ylim(0, self.y_i_s_lim)
        self.ax4.plot(
            self.df_states.index[0:idx],
            self.df_states['I_S'].iloc[0:idx]
        )
        self.ax4.plot(
            self.df_states.index[idx],
            self.df_states['I_S'].iloc[idx],
            marker='o',
            ms=5
        )
        ax4_labels = self.ax4.get_xticks()
        self.ax4.set_xticks(ax4_labels)
        self.ax4.set_xticklabels(
            self.ax4.get_xticklabels(),
            rotation=45, ha='right'
        )

    def start(self) -> list:
        """_summary_

        Returns:
            _type_: _description_
        """
        lines = [self.line1, self.line2, self.line3, self.line4]
        return lines

    def record_animation(self, video_file='VSMAnimation'):
        """_summary_
        """
        anim = animation.FuncAnimation(
            self.fig,
            self,
            init_func=self.start,
            interval=1,
            save_count=32,
            frames=range(len(self.df_ref_sol.index)),
            repeat=False
        )
        metadata = self.metadata
        writer = animation.FFMpegWriter(fps=32, metadata=metadata)
        writergif = animation.PillowWriter(fps=128)

        str_tag = pd.Timestamp.now()
        str_tag = str(str_tag)
        str_tag.strip()
        str_tag.replace(' ', '_')
        str_tag = video_file+str_tag + ".mp4"
        print(str_tag)
        # anim.save(str_tag, writer=writer)
        # anim.save('animation.gif', writer=writergif)
        pbar = tqdm(
            desc='rec',
            total=len(self.df_ref_sol.index)
        )

        with writer.saving(self.fig, str_tag, 100):
            for idx in range(len(self.df_ref_sol.index)):
                #         # print(idx, t)
                self.__call__(idx)
                writer.grab_frame()
                pbar.update(idx)
