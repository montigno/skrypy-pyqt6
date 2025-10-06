class signal_filter_butter:
    def __init__(self, data=[0.0], cutoff=2.0, fs=30.0, order=2, type="enumerate(('low', 'high'))"):
        from scipy.signal import butter, filtfilt

        nyq = 0.5 * fs  # Nyquist Frequency
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype=type, analog=False)
        self.y = filtfilt(b, a, data)

    def out_filtered(self: 'list_float'):
        return self.y

##############################################################################


class signal_filter_moving_averages:
    def __init__(self, data_in=[0.0], window_size=5):
        import numpy as np
        self.res = np.copy(data_in)
        for i in range(1, len(data_in)-1):
            L_g = min(i, window_size)
            L_d = min(len(data_in)-i-1, window_size)
            Li = min(L_g, L_d)
            self.res[i] = np.sum(data_in[i-Li:i+Li+1]) / (2*Li+1)

    def mov_average(self: 'list_float'):
        return self.res

##############################################################################
