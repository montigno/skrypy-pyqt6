class keras_gpu_options:
    def __init__(self, allow_growth=True, **options):
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = allow_growth
        for ef in options:
            setattr(config.gpu_options, ef, options[ef])
        sess = tf.Session(config=config)
        set_session(sess)

##############################################################################


class keras_to_numpy():
    """
    Convert keras tensor to ndarray

    Args:
        tensor_in: (tensor)

    Returns:
        out_numpy: (ndarray)

    Note:
        GUI: no
    """
    def __init__(self, tensor_in=[[0.0]]):
        # import tensorflow.keras.backend as K
        # self.nump = K.eval(tensor_in(session=tf.compat.v1.Session()))
        import tensorflow as tf
        from tensorflow.python.keras import backend
        sess = backend.get_session()
        self.nump = sess.run(tensor_in)

    def out_numpy(self: 'array_float'):
        return self.nump

##############################################################################


class keras_datasets_mnist():

    def __init__(self):
        from keras.datasets import mnist
        (self.X_train, self.Y_train), (self.X_test, self.Y_test) = mnist.load_data()

    def X_train(self: 'array_float'):
        return self.X_train

    def Y_train(self: 'array_float'):
        return self.Y_train

    def X_test(self: 'array_float'):
        return self.X_test

    def Y_test(self: 'array_float'):
        return self.Y_test

###############################################################################


class keras_layers_Activation():
    """
    Applies an activation function to an output.

    Args:
        tensorflow_in: (tensor) a tensor input

    Returns:
        out_Activation: (tensor) Activation output

    Note:
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], **options):
        from tensorflow.keras.layers import Activation
        self.act = Activation(**options)(tensorflow_in)

    def out_Activation(self: 'array_float'):
        return self.act

###############################################################################


class keras_layers_Input():
    """
    Input() is used to instantiate a Keras tensor.
    A Keras tensor is a symbolic tensor-like object, which we augment with certain
    attributes that allow us to build a Keras model just by knowing the inputs
    and outputs of the model.
    For instance, if a, b and c are Keras tensors, it becomes possible to do:
    model = Model(input=[a, b], output=c)

    Args:
        shape: A shape tuple (integers), not including the batch size.
                For instance, shape=(32,) indicates that the expected input will
                be batches of 32-dimensional vectors.
                Elements of this tuple can be None;
                'None' elements represent dimensions where the shape is not known.

    Returns:
        input: (tensor) return a tensor

    Note:
        link_web: https://keras.io/api/layers/core_layers/input/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, shape=(0,), **options):
        from tensorflow.keras.layers import Input
        self.lay_input = Input(shape, **options)

    def input(self: 'array_float'):
        return self.lay_input

###############################################################################


class keras_layers_Conv3D():
    """
    3D convolution layer (e.g. spatial convolution over volumes).
    This layer creates a convolution kernel that is convolved with
    the layer input to produce a tensor of outputs.
    If use_bias is True, a bias vector is created and added to the outputs.
    Finally, if activation is not None, it is applied to the outputs as well.
    When using this layer as the first layer in a model,
    provide the keyword argument input_shape
    (tuple of integers or None, does not include the sample axis),
    e.g. input_shape=(128, 128, 128, 1) for 128x128x128 volumes
    with a single channel, in data_format='channels_last'.

    Args:
        tensorflow_in: (tensor) a tensor input
        filters: Integer, the dimensionality of the output space
                    (i.e. the number of output filters in the convolution).
        kernel_size: An integer or tuple/list of 3 integers, specifying the depth,
                    height and width of the 3D convolution window.
                    Can be a single integer to specify the same value for
                        all spatial dimensions.

    Returns:
        out_Conv3D: (tensor) A tensor of rank 5+ representing activation(conv3d(inputs, kernel) + bias).

    Note:
        link_web: https://keras.io/api/layers/convolution_layers/convolution3d/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], filters=3, kernel_size=(3, 3, 3), **options):
        from tensorflow.keras.layers import Conv3D
        self.tf_out = Conv3D(filters, kernel_size, **options)(tensorflow_in)

    def out_Conv3D(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_Conv3DTranspose():
    """
    Transposed convolution layer (sometimes called Deconvolution).
    The need for transposed convolutions generally arises from
    the desire to use a transformation going in the opposite direction
    of a normal convolution, i.e., from something that has the shape of
    the output of some convolution to something that has the shape of
    its input while maintaining a connectivity pattern that is compatible
    with said convolution.
    When using this layer as the first layer in a model, provide the keyword argument
    input_shape (tuple of integers or None, does not include the sample axis),
    e.g. input_shape=(128, 128, 128, 3) for a 128x128x128 volume with 3 channels if
    data_format='channels_last'.

    Args:
        tensorflow_in: (tensor) a tensor input
        filters: Integer, the dimensionality of the output space
                    (i.e. the number of output filters in the convolution).
        kernel_size: An integer or tuple/list of 3 integers,
                        specifying the depth, height and width of
                        the 3D convolution window.
                        Can be a single integer to specify the same value for
                        all spatial dimensions.

    Returns:
        out_Conv3DTranspose: A tensor of rank 5 representing activation
                                (conv3dtranspose(inputs, kernel) + bias).

    Note:
        link_web: https://keras.io/api/layers/convolution_layers/convolution3d_transpose/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], filters=3, kernel_size=(3, 3, 3), **options):
        from tensorflow.keras.layers import Conv3DTranspose
        self.tf_out = Conv3DTranspose(filters, kernel_size, **options)(tensorflow_in)

    def out_Conv3DTranspose(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_Dense():
    """
    Dense implements the operation: output = activation(dot(input, kernel) + bias)
    where activation is the element-wise activation function passed as the activation
    argument, kernel is a weights matrix created by the layer, and bias is a bias
    vector created by the layer (only applicable if use_bias is True).
    These are all attributes of Dense.
    Note: If the input to the layer has a rank greater than 2, then Dense computes
    the dot product between the inputs and the kernel along the last axis of the
    inputs and axis 0 of the kernel (using tf.tensordot). For example, if input has
    dimensions (batch_size, d0, d1), then we create a kernel with shape (d1, units),
    and the kernel operates along axis 2 of the input, on every sub-tensor of
    shape (1, 1, d1) (there are batch_size * d0 such sub-tensors). The output in this
    case will have shape (batch_size, d0, units).
    Besides, layer attributes cannot be modified after the layer has been called once
    (except the trainable attribute). When a popular kwarg input_shape is passed,
    then keras will create an input layer to insert before the current layer.
    This can be treated equivalent to explicitly defining an InputLayer.

    Args:
        units: Positive integer, dimensionality of the output space.

    Returns:
        out_Dense: Dense function

    Note:
        link_web: https://keras.io/api/layers/core_layers/dense/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, units=32, **options):
        from tensorflow.keras.layers import Dense
        self.tf_out = Dense(units, **options)
        print('dense : ', self.tf_out)

    def out_Dense(self: 'str'):
        return self.tf_out

###############################################################################


class keras_layers_MaxPooling3D():
    """
    Max pooling operation for 3D data (spatial or spatio-temporal).
    Downsamples the input along its spatial dimensions (depth, height, and width)
    by taking the maximum value over an input window (of size defined by pool_size)
    for each channel of the input.
    The window is shifted by strides along each dimension.

    Args:
        tensorflow_in: (tensor) a tensor input
        pool_size: Tuple of 3 integers, factors by which to
                    downscale (dim1, dim2, dim3).
                    (2, 2, 2) will halve the size of the 3D input in
                        each dimension.

    Returns:
        out_MaxPooling3D: "(tensor)<br>
                           If data_format='channels_last':
                               5D tensor with shape:
                                   (batch_size, pooled_dim1,
                                   pooled_dim2, pooled_dim3, channels)
                           If data_format='channels_first':
                               5D tensor with shape:
                                   (batch_size, channels, pooled_dim1,
                                   pooled_dim2, pooled_dim3)

    Note:
        link_web: https://keras.io/api/layers/pooling_layers/max_pooling3d/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], pool_size=(2, 2, 2), **options):
        from tensorflow.keras.layers import MaxPooling3D
        self.tf_out = MaxPooling3D(pool_size, **options)(tensorflow_in)

    def out_MaxPooling3D(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_Concatenate():
    def __init__(self, tf_in1=[[0.0]], tf_in2=[[0.0]], axis=-1):
        from tensorflow.keras.layers import concatenate
        self.tf_out = concatenate([tf_in1, tf_in2], axis=axis)
        # self.tf_out = Concatenate(axis=axis)([tf_in1, tf_in2])

    def out_concatenate(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_AveragePooling3D():
    """
    Average pooling operation for 3D data (spatial or spatio-temporal).
    Downsamples the input along its spatial dimensions (depth, height, and width)
    by taking the average value over an input window (of size defined by pool_size)
    for each channel of the input.
    The window is shifted by strides along each dimension.

    Args:
        tensorflow_in: (tensor) a tensor input
        pool_size: tuple of 3 integers, factors by which to downscale (dim1, dim2, dim3).
        (2, 2, 2) will halve the size of the 3D input in each dimension.

    Returns:
        out_AveragePooling3D: (tensor)
                                If data_format='channels_last':
                                    5D tensor with shape:
                                            (batch_size, pooled_dim1, pooled_dim2, pooled_dim3, channels)
                                If data_format='channels_first':
                                    5D tensor with shape:
                                            (batch_size, channels, pooled_dim1, pooled_dim2, pooled_dim3)

    Note:
        link_web: https://keras.io/api/layers/pooling_layers/average_pooling3d/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], pool_size=(2, 2, 2), **options):
        from tensorflow.keras.layers import AveragePooling3D
        self.tf_out = AveragePooling3D(pool_size, **options)(tensorflow_in)

    def out_AveragePooling3D(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_ZeroPadding3D():
    """
    Zero-padding layer for 3D data (spatial or spatio-temporal).

    Args:
        tensorflow_in: (tensor) a tensor input
        padding:
                Int, or tuple of 3 ints, or tuple of 3 tuples of 2 ints.
                If int the same symmetric padding is applied to height and width.
                If tuple of 3 ints; interpreted as two different symmetric padding values
                    for height and width: (symmetric_dim1_pad,
                                           symmetric_dim2_pad,
                                           symmetric_dim3_pad).
                If tuple of 3 tuples of 2 ints;
                    interpreted as ((left_dim1_pad, right_dim1_pad),
                                    (left_dim2_pad, right_dim2_pad),
                                    (left_dim3_pad, right_dim3_pad))

    Returns:
        out_ZeroPadding3D:
                5D tensor with shape;
                    - If data_format is 'channels_last':
                        (batch_size,
                         first_padded_axis,
                         second_padded_axis,
                         third_axis_to_pad, depth)
                    - If data_format is 'channels_first':
                        (batch_size,
                         depth,
                         first_padded_axis,
                         second_padded_axis,
                         third_axis_to_pad)

    Note:
        link_web: https://keras.io/api/layers/reshaping_layers/zero_padding3d/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], padding=(1, 1, 1), **options):
        from tensorflow.keras.layers import ZeroPadding3D
        self.tf_out = ZeroPadding3D(padding, **options)(tensorflow_in)

    def out_ZeroPadding3D(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_BatchNormalization():
    """
    Layer that normalizes its inputs.
    Batch normalization applies a transformation that maintains
    the mean output close to 0 and the output standard deviation close to 1.
    Importantly, batch normalization works differently during training and
    during inference.

    Args:
        tensorflow_in: (tensor) a tensor input

    Returns:
        out_BatchNormalization: (tensor) Same shape as input.

    Note:
        link_web: https://keras.io/api/layers/normalization_layers/batch_normalization/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, tensorflow_in=[[0.0]], **options):
        from tensorflow.keras.layers import BatchNormalization
        self.tf_out = BatchNormalization(**options)(tensorflow_in)

    def out_BatchNormalization(self: 'array_float'):
        return self.tf_out

###############################################################################


class keras_layers_UpSampling3D():
    def __init__(self, tensorflow_in=[[0.0]], **options):
        from tensorflow.keras.layers import UpSampling3D
        self.upSamp = UpSampling3D(**options)(tensorflow_in)

    def out_UpSAmpling3D(self: 'array_float'):
        return self.upSamp

###############################################################################


class keras_models_Model():
    """
    Model groups layers into an object with training and inference features.

    Args:
        inputs:  The input(s) of the model, a keras.Input object or list of keras.
                    Input objects.
        outputs: The output(s) of the model. See Functional API example below.

    Returns:
        model_out: output of the model

    Note:
        link_web: https://keras.io/api/models/model/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, inputs=[[0.0]], outputs=[[0.0]], **options):
        from tensorflow.keras.models import Model
        self.model = Model(inputs=[inputs], outputs=[outputs], **options)

    def model_out(self: 'array_float'):
        return self.model

###############################################################################


class keras_models_Model_compile():
    """
    Configures the model for training.

    Args:
        model_in: the Model group of keras.models.Model

    Returns:
        model_out: keras.models.Model output

    Note:
        link_web: https://www.tensorflow.org/api_docs/python/tf/keras/Model#compile
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, model_in=[[0.0]], **options):
        # from keras.models import Model
        self.model_comp = model_in.compile(**options)
        self.model = model_in

    def model_compile(self: 'array_float'):
        return self.model_comp

    def model_out(self: 'array_float'):
        return self.model

###############################################################################


class keras_models_Model_summary():
    """
    Prints a string summary of the network.

    Args:
        model_in: the Model group of keras.models.Model

    Returns:
        model_out: keras.models.Model output

    Note:
        link_web: https://keras.io/api/models/model/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, model_in=[[0.0]], **options):
        from tensorflow.keras.models import Model
        self.model = model_in.summary(**options)

    def model_out(self: 'array_float'):
        return self.model

###############################################################################


class keras_models_Model_predict():
    """
    Generates output predictions for the input samples.
    Computation is done in batches. This method is designed for performance in
        large scale inputs. For small amount of inputs that fit in one batch,
        directly using __call__ is recommended for faster execution,
        e.g., model(x), or model(x, training=False) if you have layers such as
        tf.keras.layers.BatchNormalization that behaves differently during inference.
    Also, note the fact that test loss is not affected by regularization layers
    like noise and dropout.

    Args:
        model_in: the Model group of keras.models.Model
        x: Input samples. It could be:<br>
             A Numpy array (or array-like), or a list of arrays
             (in case the model has multiple inputs).
             A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
             A tf.data dataset.
             A generator or keras.utils.Sequence instance.
             A more detailed description of unpacking behavior for iterator types
                 (Dataset, generator, Sequence) is given in the Unpacking behavior for
                 iterator-like inputs section of Model.fit.
        batch_size: Integer or None. Number of samples per batch.
                        If unspecified, batch_size will default to 32.
                        Do not specify the batch_size if your data is in the
                        form of dataset, generators, or keras.utils.
                        Sequence instances (since they generate batches).
        verbose: Verbosity mode, 0 or 1.

    Returns:
        predict_out: keras.models.Model output

    Note:
        link_web: https://www.tensorflow.org/api_docs/python/tf/keras/Model#predict
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, model_in=[[0.0]], x=[[0.0]], batch_size=1, verbose=0):
        import numpy as np
        # from keras.models import Model
        self.pred = model_in.predict(np.array(x), batch_size, verbose)

    def predict_out(self: 'array_float'):
        return self.pred

###############################################################################


class keras_models_Model_fit():
    """
    Trains the model for a fixed number of epochs (iterations on a dataset).

    Args:
        model_in: the Model group of keras.models.Model
        model_out: keras.models.Model output
        x: Input data. It could be:
              A Numpy array (or array-like), or a list of arrays
                  (in case the model has multiple inputs).
              A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs)
              A dict mapping input names to the corresponding array/tensors,
                  if the model has named inputs
              A tf.data dataset. Should return a tuple of either (inputs, targets) or
                                                      (inputs, targets, sample_weights).
              A generator or keras.utils.Sequence returning (inputs, targets) or
                                                      (inputs, targets, sample_weights).
              A tf.keras.utils.experimental.DatasetCreator, which wraps a callable that
                  takes a single argument of type tf.distribute.InputContext, and returns a
                  tf.data.Dataset. DatasetCreator should be used when users prefer to specify
                  the per-replica batching and sharding logic for the Dataset.
                  See tf.keras.utils.experimental.DatasetCreator doc for more information.
                  A more detailed description of unpacking behavior for iterator types
                  (Dataset, generator, Sequence) is given below.
                  If using tf.distribute.experimental.ParameterServerStrategy, only
                  DatasetCreator type is supported for x.
        y: Target data. Like the input data x, it could be either Numpy array(s)
            or TensorFlow tensor(s). It should be consistent with x
            (you cannot have Numpy inputs and tensor targets, or inversely).
            If x is a dataset, generator, or keras.utils.
            Sequence instance, y should not be specified
            (since targets will be obtained from x).

    Returns:
        fit_out: output of the model

    Note:
        link_web: https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, model_in=[[0.0]], x=[[0.0]], y=[[0.0]], **options):
        # from keras.models import Model
        self.fit = model_in.fit(x, y, **options)
        self.model = model_in

    def model_fit(self: 'array_float'):
        return self.fit

    def model_out(self: 'array_float'):
        return self.model

###############################################################################


class keras_models_Model_load_model():
    def __init__(self, filepath='path', **options):
        from keras.models import load_model
        self.loaded_model = load_model(filepath, **options)

    def model_out(self: 'array_float'):
        return self.loaded_model

###############################################################################


class keras_Sequential_dyn():
    """
    Sequential groups a linear stack of layers into a tf.keras.Model.
    Sequential provides training and inference features on this model.

    Args:
        layer: layer instance.

    Returns:
        out_Sequential: Sequential function

    Note:
        link_web: https://keras.io/api/models/sequential/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, layer='', **dynamicsInputs):
        from tensorflow.keras import Sequential
        list_layer = [layer]
        for di in dynamicsInputs:
            list_layer.append(dynamicsInputs[di])
        print('list_layer :', list_layer)
        self.model = Sequential(list_layer)

    def out_Sequential(self: 'array_float'):
        return self.model

###############################################################################


class keras_optimizers_Adam():
    """
    Optimizer that implements the Adam algorithm.
    Adam optimization is a stochastic gradient descent method that
    is based on adaptive estimation of first-order and second-order moments.

    Args:
        learning_rate: (tensor) floating point value, or a schedule that
                        is a tf.keras.optimizers.schedules.LearningRateSchedule,
                        or a callable that takes no arguments and returns the actual
                        value to use, The learning rate. Defaults to 0.001.

    Returns:
        adam_out: (tensor)

    Note:
        link_web: https://keras.io/api/optimizers/adam/
        dependencies: keras, tensorflow
        GUI: no
    """
    def __init__(self, learning_rate=1e-5, **options):
        from keras.optimizers import Adam
        self.adam = Adam(lr=learning_rate, **options)

    def adam_out(self: 'array_float'):
        return self.adam

###############################################################################


class keras_utils_to_categorical():
    def __init__(self, y=[[0.0]], **options):
        from tensorflow.keras.utils import to_categorical
        self.to_cat = to_categorical(y, **options)

    def to_categorical(self: 'array_float'):
        return self.to_cat
