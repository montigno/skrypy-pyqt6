class antspy_create_warped_grid():
    """
    Deforming a grid is a helpful way to visualize a deformation field.
    This function enables a user to define the grid parameters
    and apply a deformable map to that grid.

    ANTsR function: `createWarpedGrid`

    Arguments
    ---------
    image : ANTsImage
        input image

    grid_step : scalar
        width of grid blocks

    grid_width : scalar
        width of grid lines

    grid_directions : tuple of booleans
        directions in which to draw grid lines, boolean vector

    fixed_reference_image : ANTsImage (optional)
        reference image space

    transform : list/tuple of strings (optional)
        vector of transforms

    foreground : scalar
        intensity value for grid blocks

    background : scalar
        intensity value for grid lines

    Returns
    -------
    ANTsImage

    Example
    -------
    >>> import ants
    >>> fi = ants.image_read( ants.get_ants_data( 'r16' ) )
    >>> mi = ants.image_read( ants.get_ants_data( 'r64' ) )
    >>> mygr = ants.create_warped_grid( mi )
    >>> mytx = ants.registration(fixed=fi, moving=mi, type_of_transform = ('SyN') )
    >>> mywarpedgrid = ants.create_warped_grid( mygr, grid_directions=(False,True),
                            transform=mytx['fwdtransforms'], fixed_reference_image=fi )
    """
    def __init__(self, image='path', grid_step=10, grid_width=2, grid_directions=(True, True), foreground=1, background=0, **options):
        pass
