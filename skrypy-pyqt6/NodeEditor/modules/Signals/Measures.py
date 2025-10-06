class signal_rms():
    def __init__(self, y=[0.0]):
        import math
        ms = 0.0
        for i in range(0, len(y)):
            ms = ms + y[i]**2
        ms = ms / len(y)
        self.__rms = math.sqrt(ms)

    def rms(self: 'float'):
        return self.__rms
