class afni_AlignEpiAnatPy:
    """
    Note:
        GUI: no
        dependencies: Nipype,afni
        link_web: (click Ctrl + U)
    """
    def __init__(self, anat='path', epi_base="enumerate(('0', 'mean', 'median', 'max'))", in_file='path', **options):
        from nipype.interfaces.afni import AlignEpiAnatPy
        al_ea = AlignEpiAnatPy()
        al_ea.inputs.anat = anat
        al_ea.inputs.epi_base = epi_base
        al_ea.inputs.in_file = in_file
        for ef in options:
            setattr(al_ea.inputs, ef, options[ef])
        al_ea.cmdline
        self.res = al_ea.run()

    def anat_al_mat(self: 'path'):
        return self.res.outputs.anat_al_mat

    def anat_al_orig(self: 'path'):
        return self.res.outputs.anat_al_orig

    def epi_al_mat(self: 'path'):
        return self.res.outputs.epi_al_mat

    def epi_al_orig(self: 'path'):
        return self.res.outputs.epi_al_orig

    def epi_al_tlrc_mat(self: 'path'):
        return self.res.outputs.epi_al_tlrc_mat

    def epi_reg_al_mat(self: 'path'):
        return self.res.outputs.epi_reg_al_mat

    def epi_tlrc_al(self: 'path'):
        return self.res.outputs.epi_tlrc_al

    def epi_vr_al_mat(self: 'path'):
        return self.res.outputs.epi_vr_al_mat

    def epi_vr_motion(self: 'path'):
        return self.res.outputs.epi_vr_motion

    def skullstrip(self: 'path'):
        return self.res.outputs.skullstrip

##############################################################################


class afni_Autobox:
    """
    Note:
        GUI: no
        dependencies: Nipype,afni
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import Autobox
        at = Autobox()
        at.inputs.in_file = in_file
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def x_min(self: "int"):
        return self.res.outputs.x_min

    def x_max(self: "int"):
        return self.res.outputs.x_max

    def y_min(self: "int"):
        return self.res.outputs.y_min

    def y_max(self: "int"):
        return self.res.outputs.y_max

    def z_min(self: "int"):
        return self.res.outputs.z_min

    def z_max(self: "int"):
        return self.res.outputs.z_max

    def out_file(self: "path"):
        return self.res.outputs.out_file

##############################################################################


class afni_Automask():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import Automask
        automask = Automask()
        automask.inputs.in_file = in_file
        for ef in options:
            setattr(automask.inputs, ef, options[ef])
        self.res = automask.run()

    def brain_file(self: 'path'):
        return self.res.outputs.brain_file

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Calc():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file_a='path', expr='a*b', **options):
        from nipype.interfaces.afni import Calc
        calc = Calc()
        calc.inputs.in_file_a = in_file_a
        calc.inputs.expr = expr
        for ef in options:
            setattr(calc.inputs, ef, options[ef])
        self.res = calc.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Despike():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import Despike
        despike = Despike()
        despike.inputs.in_file = in_file
        for ef in options:
            setattr(despike.inputs, ef, options[ef])
        self.res = despike.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Fourier():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', lowpass=0.005, highpass=0.1, **options):
        from nipype.interfaces import afni
        fourier = afni.Fourier()
        fourier.inputs.in_file = in_file
        fourier.inputs.lowpass = lowpass
        fourier.inputs.highpass = highpass
        for ef in options:
            setattr(fourier.inputs, ef, options[ef])
        self.res = fourier.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Resample():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import Resample
        at = Resample()
        at.inputs.in_file = in_file
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Seg():
    """
    Note:
        dependencies: Nipype, AFNI
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', mask='AUTO', **options):
        from nipype.interfaces.afni.preprocess import Seg
        seg = Seg()
        seg.inputs.in_file = in_file
        seg.inputs.mask = mask
        for ef in options:
            setattr(seg.inputs, ef, options[ef])
        self.res = seg.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_SkullStrip():
    """
    Note:
        dependencies: Nipype, AFNI
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import SkullStrip
        skullstrip = SkullStrip()
        skullstrip.inputs.in_file = in_file
        for ef in options:
            setattr(skullstrip.inputs, ef, options[ef])
        skullstrip.cmdline
        self.res = skullstrip.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_Unifize():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import Unifize
        unifize = Unifize()
        unifize.inputs.in_file = in_file
        for ef in options:
            setattr(unifize.inputs, ef, options[ef])
        self.res = unifize.run()

    def scale_file(self: 'path'):
        return self.res.outputs.scale_file

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class afni_ZCutUp():
    """
    Note:
        GUI: no
        dependencies: Nipype, AFNI
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.afni import ZCutUp
        zcutup = ZCutUp()
        zcutup.inputs.in_file = in_file
        for ef in options:
            setattr(zcutup.inputs, ef, options[ef])
        self.res = zcutup.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file
