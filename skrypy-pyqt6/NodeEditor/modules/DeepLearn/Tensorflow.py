class tensorflow_to_numpy():
    def __init__(self, tensor_in=[[0.0]]):
        import tensorflow as tf
        self.nump = tensor_in.numpy()

    def out_numpy(self: 'array_float'):
        return self.nump

###############################################################################


class tensorflow_gpus_config:
    def __init__(self):
        import tensorflow as tf
        self.gpus = tf.config.list_physical_devices('GPU')
        if self.gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in self.gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.list_logical_devices('GPU')
                print(len(self.gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)
        else:
            self.gpus = ['']

    def gpus_status(self: 'list_str'):
        return self.gpus

###############################################################################


class tensorflow_nn_conv3d():
    def __init__(self, input=[[0.0]], filters=[[0.0]], strides=[1, 1, 1, 1, 1], padding="enumerate(('SAME', 'VALID'))", **options):
        import tensorflow as tf
        self.conv = tf.nn.conv3d(input, filters, strides, padding, **options)

    def conv3d(self: 'array_float'):
        return self.conv
