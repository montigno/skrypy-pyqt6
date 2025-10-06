class matplotlib_coherence_of_two_signals:
    '''
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py
    '''
    def __init__(self, s1=[0.0], s2=[0.0]):
        import matplotlib.pyplot as plt
        import numpy as np

        # Fixing random state for reproducibility
        np.random.seed(19680801)
        dt = 0.01
        t = np.arange(0, 30, dt)
        nse1 = np.random.randn(len(t))  # white noise 1
        nse2 = np.random.randn(len(t))  # white noise 2

        s1n = s1 + nse1
        s2n = s2 + nse2

        fig, axs = plt.subplots(2, 1, layout='constrained')
        axs[0].plot(t, s1, t, s2)
        axs[0].set_xlim(0, 2)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('s1 and s2')
        axs[0].grid(True)

        cxy, f = axs[1].cohere(s1, s2, NFFT=256, Fs=1. / dt)
        axs[1].set_ylabel('Coherence')

        plt.show()
