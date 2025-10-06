class monai_config_print_config():
    def __init__(self, **options):
        from monai.config import print_config
        self.print_out = print_config()

###############################################################################


class monai_transforms_LoadImaged():
    def __init__(self, keys=["image", "label"], **options):
        from monai.transforms import LoadImaged
        self.loadImg = LoadImaged(keys, **options)

    def out_loadimaged(self: 'str'):
        return self.loadImg

##############################################################################


class monai_transforms_compose():
    """
    Compose provides the ability to chain a series of callables together in a
    sequential manner.
    Each transform in the sequence must take a single argument and return a single value.
    Compose can be used in two ways:
        With a series of transforms that accept and return a single ndarray /
            tensor / tensor-like parameter.
        With a series of transforms that accept and return a dictionary that
            contains one or more parameters. Such transforms must have pass-through
            semantics that unused values in the dictionary must be copied to
            the return dictionary.
            It is required that the dictionary is copied between input and output
            of each transform.
    If some transform takes a data item dictionary as input, and returns a sequence
    of data items in the transform chain, all following transforms will be applied
    to each item of this list if map_items is True (the default).
    If map_items is False, the returned sequence is passed whole to the next
    callable in the chain.
    For example:
        A Compose([transformA, transformB, transformC], map_items=True)(data_dict)
        could achieve the following patch-based transformation on the data_dict input:
            1. transformA normalizes the intensity of ‘img’ field in the data_dict.
            2. transformB crops out image patches from the ‘img’ and ‘seg’ of data_dict,
               and return a list of three patch samples:
                    {'img': 3x100x100 data, 'seg': 1x100x100 data, 'shape': (100, 100)}
                                         applying transformB
                                             ---------->
                    [{'img': 3x20x20 data, 'seg': 1x20x20 data, 'shape': (20, 20)},
                     {'img': 3x20x20 data, 'seg': 1x20x20 data, 'shape': (20, 20)},
                     {'img': 3x20x20 data, 'seg': 1x20x20 data, 'shape': (20, 20)},]

            3. transformC then randomly rotates or flips ‘img’ and ‘seg’ of each dictionary
            item in the list returned by transformB.
    The composed transforms will be set the same global random seed if user called set_determinism().
    When using the pass-through dictionary operation, you can make use of
    monai.transforms.adaptors.adaptor to wrap transforms that don’t conform to the requirements.
    This approach allows you to use transforms from otherwise incompatible libraries
    with minimal additional work.

    Args:
        Transforms: (Union[Sequence[Callable], Callable, None]) – sequence of callables.

    Returns:
        out_compose: callable

    Note:
        link_web: https://docs.monai.io/en/stable/transforms.html#compose
        dependencies: monai
        GUI: no
    """
    def __init__(self, transforms=[''], **options):
        from monai.transforms import compose
        self.comp = compose(*transforms, **options)

    def out_compose(self: 'str'):
        return self.comp

##############################################################################


class monai_transforms_EnsureChannelFirstd():
    """
    Dictionary-based wrapper of monai.transforms.EnsureChannelFirst.

    Args:
        keys: (Union[Collection[Hashable], Hashable]) – keys of the corresponding
                items to be transformed.
                See also: monai.transforms.compose.MapTransform

    Returns:
        out_ensureChannelFirstd: callable

    Note:
        link_web: https://docs.monai.io/en/stable/transforms.html#ensurechannelfirstd
        dependencies: monai
        GUI: no
    """
    def __init__(self, keys=['image'], **options):
        from monai.transforms import EnsureChannelFirstd
        self.ens = EnsureChannelFirstd(keys, **options)

    def out_ensureChannelFirstd(self: 'str'):
        return self.ens

##############################################################################


class monai_utils_set_determinism():
    def __init__(self, **options):
        from monai.utils import set_determinism
        set_determinism(**options)
