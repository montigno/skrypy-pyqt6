class matplotlib_plot():
    def __init__(self, y_data=[0.0], x=[0.0], **options):
        import matplotlib.pyplot as plt
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is not None:
            plt.ion()

        if 'style_use' in options.keys():
            plt.style.use(options['style_use'])
            del options['style_use']

        plot_options = {key[5:]: options[key] for key in options if 'plot_' in key}
        set_options = {key[4:]: options[key] for key in options if 'set_' in key}

        fig, ax = plt.subplots()

        if 'dot_style' in options.keys():
            ax.plot(x, y_data, options['dot_style'], **plot_options)
        else:
            ax.plot(x, y_data, **plot_options)

        if 'axvline' in options.keys():
            mk = options['axvline']
            if not isinstance(mk[0], tuple):
                mk = (mk,)
            for i in mk:
                ax.axvline(x=i[0], color=i[1], linestyle=i[2], linewidth=i[3], label=i[0])
            del options['axvline']
        ax.set(**set_options)
        if 'window_title' in options.keys():
            plt.get_current_fig_manager().set_window_title(options['window_title'])
        plt.tight_layout()
        plt.show()

##############################################################################


class matplotlib_multiple_curves():
    def __init__(self, y_data=[[0.0]], x=[[0.0]], **options):
        import matplotlib.pyplot as plt
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is not None:
            plt.ion()

        n = len(y_data)

        plot_options = {key[5:]: options[key] for key in options if 'plot_' in key}
        set_options = {key[4:]: options[key] for key in options if 'set_' in key}

        if 'style_use' in options.keys():
            plt.style.use(options['style_use'])

        fig, ax = plt.subplots()

        for i, y_lst in enumerate(y_data):
            if len(x) == n:
                x_dup = x[i]
            else:
                x_dup = x
            sub_plot_options = {key: plot_options[key][i] for key in plot_options}
            if 'dot_style' in options.keys():
                ax.plot(x_dup, y_lst, options['dot_style'][i], **sub_plot_options)
            else:
                ax.plot(x_dup, y_lst, **sub_plot_options)

        if 'axvline' in options.keys():
            mk = options['axvline']
            if not isinstance(mk[0], tuple):
                mk = (mk,)
            for i in mk:
                ax.axvline(x=i[0], color=i[1], linestyle=i[2], linewidth=i[3], label=i[0])
            del options['axvline']

        ax.set(**set_options)
        if 'plot_label' in options.keys():
            ax.legend()
        if 'window_title' in options.keys():
            plt.get_current_fig_manager().set_window_title(options['window_title'])
        plt.tight_layout()
        plt.show()

##############################################################################


class matplotlib_multiple_plots():
    def __init__(self, y_data=[[0.0]], x=[[0.0]], **options):
        import matplotlib.pyplot as plt
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is not None:
            plt.ion()

        n = len(y_data)

        plot_options = {key[5:]: options[key] for key in options if 'plot_' in key}
        set_options = {key[4:]: options[key] for key in options if 'set_' in key}

        if 'style_use' in options.keys():
            plt.style.use(options['style_use'])

        fig, ax = plt.subplots(n)

        for i, y_lst in enumerate(y_data):
            sub_plot_options = {key: plot_options[key][i] for key in plot_options}
            if len(x) == n:
                x_dup = x[i]
            else:
                x_dup = x
            ax[i].plot(x_dup, y_lst, **sub_plot_options)
            sub_set_options = {key: set_options[key][i] for key in set_options}
            if 'axvline' in options.keys():
                mk = options['axvline']
                if not isinstance(mk[0], tuple):
                    mk = (mk,)
                for i in mk:
                    ax[i].axvline(x=i[0], color=i[1], linestyle=i[2], linewidth=i[3], label=i[0])
                del options['axvline']
            ax[i].set(**sub_set_options)
            if 'plot_label' in options.keys():
                ax[i].legend()
        if 'window_title' in options.keys():
            plt.get_current_fig_manager().set_window_title(options['window_title'])
        plt.tight_layout()
        plt.show()
