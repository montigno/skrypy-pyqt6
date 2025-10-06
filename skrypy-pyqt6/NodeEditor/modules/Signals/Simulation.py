class signal_PWM:
    def __init__(self, sig=[0.0], frequency=30.0):
        from scipy import signal
        import numpy as np

        sig = np.array(sig)
        sample = len(sig)
        amplitude = max(sig)
        t = np.linspace(0, 1, sample, endpoint=False)
        self.pwm = amplitude * signal.square(2 * np.pi * frequency * t, duty=((sig / amplitude) + 1)/2)

    def out_pwm(self: 'list_float'):
        return self.pwm

##############################################################################


class signal_add_noise:
    def __init__(self, x=[0.0], scale=1.0):
        import numpy as np
        x = np.array(x)
        self.noisy_sig = np.add(x, np.random.normal(size=len(x), scale=scale))

    def noisy_signal(self: 'list_float'):
        return self.noisy_sig

##############################################################################
