class numpy_threshold():
    def __init__(self, image=[[0.0]], threshold=10.0, direction="enumerate(('low', 'high'))"):
        import numpy as np
        self.img = np.array(image)
        if direction == 'low':
            self.img[self.img <= threshold] = 1.0
            self.img[self.img > threshold] = 0.0
        else:
            self.img[self.img < threshold] = 0.0
            self.img[self.img >= threshold] = 1.0

    def img_threshold(self: 'array_float'):
        return self.img
