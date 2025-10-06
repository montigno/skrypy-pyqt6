class ants_AI:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, fixed_image='path', moving_image='path',
                 metric=('Mattes', 32, 'Regular', 1), **options):
        from nipype.interfaces.ants import AI
        at = AI()
        at.inputs.fixed_image = fixed_image
        at.inputs.moving_image = moving_image
        at.inputs.metric = metric
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_transform(self: "path"):
        return self.res.outputs.output_transform

###############################################################################


class ants_ANTS:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, fixed_image='path', moving_image='path',
                 metric="enumerate(('CC','MI', 'SMI', 'PR', 'SSD', 'MSQ', 'PSE'))",
                 metric_weight=[1.0],
                 output_transform_prefix='out',
                 radius=[5],
                 transformation_model="enumerate(('Diff', 'Elast', 'Exp', 'Greedy Exp', 'SyN'))",
                 **options):
        from nipype.interfaces.ants import ANTS
        ants = ANTS()
        if not isinstance(metric, list):
            metric = [metric]
        ants.inputs.fixed_image = fixed_image
        ants.inputs.moving_image = moving_image
        ants.inputs.metric = metric
        ants.inputs.metric_weight = metric_weight
        ants.inputs.output_transform_prefix = output_transform_prefix
        ants.inputs.radius = radius
        ants.inputs.transformation_model = transformation_model
        for ef in options:
            setattr(ants.inputs, ef, options[ef])
        ants.cmdline
        self.res = ants.run()

    def affine_transform(self: 'path'):
        return self.res.outputs.affine_transform

    def inverse_warp_transform(self: 'path'):
        return self.res.outputs.inverse_warp_transform

    def metaheader(self: 'path'):
        return self.res.outputs.metaheader

    def metaheader_raw(self: 'path'):
        return self.res.outputs.metaheader_raw

    def warp_transform(self: 'path'):
        return self.res.outputs.warp_transform

###############################################################################


class ants_AffineInitializer:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, fixed_image='path', moving_image='path', **options):
        from nipype.interfaces.ants import AffineInitializer
        at = AffineInitializer()
        at.inputs.fixed_image = fixed_image
        at.inputs.moving_image = moving_image
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def out_file(self: "path"):
        return self.res.outputs.out_file

###############################################################################


class ants_AntsJointFusion():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, atlas_segmentation_image=['path', 'path'],
                 atlas_image=[['path']], target_image=['path'], **options):

        from nipype.interfaces.ants import AntsJointFusion
        at = AntsJointFusion()
        at.inputs.atlas_segmentation_image = atlas_segmentation_image
        at.inputs.atlas_image = atlas_image
        at.inputs.target_image = target_image
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def out_atlas_voting_weight_name_format(self: 'str'):
        return self.res.outputs.out_atlas_voting_weight_name_format

    def out_intensity_fusion_name_format(self: 'str'):
        return self.res.outputs.out_intensity_fusion_name_format

    def out_label_fusion(self: 'path'):
        return self.res.outputs.out_label_fusion

    def out_label_post_prob_name_format(self: 'str'):
        return self.res.outputs.out_label_post_prob_name_format

###############################################################################


class ants_ApplyTransforms():
    """
    Note:
        dependencies: nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', reference_image='path', transforms='identity', **options):
        from nipype.interfaces.ants import ApplyTransforms
        at = ApplyTransforms()
        at.inputs.input_image = input_image
        at.inputs.reference_image = reference_image
        at.inputs.transforms = transforms
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

###############################################################################


class ants_ApplyTransformsToPoints():
    """
    Note:
        dependencies: nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_file='path', transforms=['path'], **options):
        from nipype.interfaces.ants import ApplyTransformsToPoints
        at = ApplyTransformsToPoints()
        at.inputs.input_file = input_file
        at.inputs.transforms = transforms
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_file(self: 'path'):
        return self.res.outputs.output_file

###############################################################################


class ants_Atropos():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, initialization="enumerate(('Random', 'Otsu', 'KMeans', 'PriorProbabilityImages', 'PriorLabelImage'))",
                 intensity_images='path', mask_image='path'):
        from nipype.interfaces.ants import Atropos
        at = Atropos()
        at.inputs.initialization = initialization
        at.inputs.intensity_images = intensity_images
        at.inputs.mask_image = mask_image
        for ef in options:
            setattr(brainextraction.inputs, ef, options[ef])
        self.res = brainextraction.run()

    def classified_image(self: 'path'):
        return self.res.outputs.classified_image

    def posteriors(self: 'list_path'):
        return self.res.outputs.posteriors

##############################################################################


class ants_AverageAffineTransform:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, dimension='', output_affine_transform='path', transforms=['path'], **options):
        from nipype.interfaces.ants import AverageAffineTransform
        at = AverageAffineTransform()
        at.inputs.dimension = dimension
        at.inputs.output_affine_transform = output_affine_transform
        at.inputs.transforms = transforms
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def affine_transform(self: "path"):
        return self.res.outputs.affine_transform

###############################################################################


class ants_AverageImages:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, dimension=3, normalize=True, images=['path'], **options):
        from nipype.interfaces.ants import AverageImages
        at = AverageImages()
        at.inputs.dimension = dimension
        at.inputs.normalize = normalize
        at.inputs.images = images
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_average_image(self: "path"):
        return self.res.outputs.output_average_image

###############################################################################


class ants_MeasureImageSimilarity():
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self,
                 moving_image='path',
                 fixed_image='path',
                 metric="enumerate(('CC', 'MeanSquares', 'Demons'))",
                 sampling_percentage=0.0,
                 radius_or_number_of_bins=0,
                 **options):

        from nipype.interfaces.ants import MeasureImageSimilarity
        sim = MeasureImageSimilarity()
        sim.inputs.moving_image = moving_image
        sim.inputs.fixed_image = fixed_image
        sim.inputs.metric = metric
        sim.inputs.sampling_percentage = sampling_percentage
        sim.inputs.radius_or_number_of_bins = radius_or_number_of_bins
        for ef in options:
            setattr(sim.inputs, ef, options[ef])
        self.res = sim.run()

    def similarity(self: 'float'):
        return self.res.outputs.similarity

###############################################################################


class ants_MultiplyImages:
    """
    Note:
        dependencies: Nipype,ants
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, dimension=3, first_input='path', second_input='path', output_product_image='path', **options):
        from nipype.interfaces.ants import MultiplyImages
        at = MultiplyImages()
        at.inputs.dimension = dimension
        at.inputs.first_input = first_input
        at.inputs.second_input = second_input
        at.inputs.output_product_image = output_product_image
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_product_image(self: "path"):
        return self.res.outputs.output_product_image

###############################################################################


class ants_Registration():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self,
                 moving_image=['path'],
                 fixed_image=['path'],
                 metric=['CC', 'MeanSquares', 'Demons'],
                 metric_weight=[1.0],
                 transforms=['Affine', 'BSplineSyN'],
                 shrink_factors=[[2, 1], [3, 2, 1]],
                 smoothing_sigmas=[[1, 0], [2, 1, 0]], **options):

        from nipype.interfaces.ants import Registration
        reg = Registration()
        reg.inputs.moving_image = moving_image
        reg.inputs.fixed_image = fixed_image
        reg.inputs.transforms = transforms
        reg.inputs.metric = metric
        reg.inputs.metric_weight = metric_weight
        reg.inputs.shrink_factors = shrink_factors
        reg.inputs.smoothing_sigmas = smoothing_sigmas
        for ef in options:
            setattr(reg.inputs, ef, options[ef])
        reg.cmdline
        self.res = reg.run()

    def warped_image(self: 'path'):
        return self.res.outputs.warped_image

    def inverse_warped_image(self: 'path'):
        return self.res.outputs.inverse_warped_image

    def composite_transform(self: 'path'):
        return self.res.outputs.composite_transform

    def inverse_composite_transform(self: 'path'):
        return self.res.outputs.inverse_composite_transform

    def save_state(self: 'path'):
        return self.res.outputs.save_state

    def forward_transforms(self: 'list_path'):
        return self.res.outputs.forward_transforms

    def reverse_transforms(self: 'list_path'):
        return self.res.outputs.reverse_transforms

    def elapsed_time(self: 'float'):
        return self.res.outputs.elapsed_time

    def metric_value(self: 'float'):
        return self.res.outputs.metric_value

    def forward_invert_flags(self: 'list_bool'):
        return self.res.outputs.forward_invert_flags

    def reverse_invert_flags(self: 'list_bool'):
        return self.res.outputs.reverse_invert_flags

###############################################################################


class ants_RegistrationSynQuick():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self,
                 moving_image=['path'],
                 fixed_image=['path'],
                 **options):

        from nipype.interfaces.ants import RegistrationSynQuick
        reg = RegistrationSynQuick()
        reg.inputs.moving_image = moving_image
        reg.inputs.fixed_image = fixed_image
        for ef in options:
            setattr(reg.inputs, ef, options[ef])
        self.res = reg.run()

    def warped_image(self: 'path'):
        return self.res.outputs.warped_image

    def inverse_warped_image(self: 'path'):
        return self.res.outputs.inverse_warped_image

    def inverse_warp_field(self: 'path'):
        return self.res.outputs.inverse_warp_field

    def out_matrix(self: 'path'):
        return self.res.outputs.out_matrix

    def forward_warp_field(self: 'path'):
        return self.res.outputs.forward_warp_field

###############################################################################


class ants_WarpImageMultiTransform():
    """
    Note:
        dependencies: nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', transformation_series=['path'], **options):
        from nipype.interfaces.ants import WarpImageMultiTransform
        at = WarpImageMultiTransform()
        at.inputs.input_image = input_image
        at.inputs.transformation_series = transformation_series
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

###############################################################################


class ants_WarpTimeSeriesImageMultiTransform():
    """
    Note:
        dependencies: nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', transformation_series=['path'], **options):
        from nipype.interfaces.ants import WarpTimeSeriesImageMultiTransform
        at = WarpTimeSeriesImageMultiTransform()
        at.inputs.input_image = input_image
        at.inputs.transformation_series = transformation_series
        for ef in options:
            setattr(at.inputs, ef, options[ef])
        self.res = at.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

##############################################################################


class ants_BrainExtraction():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, anatomical_image='path', brain_template='path',
                 brain_probability_mask='path', **options):
        from nipype.interfaces.ants.segmentation import BrainExtraction
        brainextraction = BrainExtraction()
        brainextraction.inputs.anatomical_image = anatomical_image
        brainextraction.inputs.brain_template = brain_template
        brainextraction.inputs.brain_probability_mask = brain_probability_mask
        for ef in options:
            setattr(brainextraction.inputs, ef, options[ef])
        self.res = brainextraction.run()

    def BrainExtractionMask(self: "path"):
        return self.res.outputs.BrainExtractionMask

    def BrainExtractionBrain(self: "path"):
        return self.res.outputs.BrainExtractionBrain

    def BrainExtractionCSF(self: "path"):
        return self.res.outputs.BrainExtractionCSF

    def BrainExtractionGM(self: "path"):
        return self.res.outputs.BrainExtractionGM

    def BrainExtractionInitialAffine(self: "path"):
        return self.res.outputs.BrainExtractionInitialAffine

    def BrainExtractionInitialAffineFixed(self: "path"):
        return self.res.outputs.BrainExtractionInitialAffineFixed

    def BrainExtractionInitialAffineMoving(self: "path"):
        return self.res.outputs.BrainExtractionInitialAffineMoving

    def BrainExtractionLaplacian(self: "path"):
        return self.res.outputs.BrainExtractionLaplacian

    def BrainExtractionPrior0GenericAffine(self: "path"):
        return self.res.outputs.BrainExtractionPrior0GenericAffine

    def BrainExtractionPrior1InverseWarp(self: "path"):
        return self.res.outputs.BrainExtractionPrior1InverseWarp

    def BrainExtractionPrior1Warp(self: "path"):
        return self.res.outputs.BrainExtractionPrior1Warp

    def BrainExtractionPriorWarped(self: "path"):
        return self.res.outputs.BrainExtractionPriorWarped

    def BrainExtractionSegmentation(self: "path"):
        return self.res.outputs.BrainExtractionSegmentation

    def BrainExtractionTemplateLaplacian(self: "path"):
        return self.res.outputs.BrainExtractionTemplateLaplacian

    def BrainExtractionTmp(self: "path"):
        return self.res.outputs.BrainExtractionTmp

    def BrainExtractionWM(self: "path"):
        return self.res.outputs.BrainExtractionWM

    def N4Corrected0(self: "path"):
        return self.res.outputs.N4Corrected0

    def N4Truncated0(self: "path"):
        return self.res.outputs.N4Truncated0

##############################################################################


class ants_CorticalThickness():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, anatomical_image='path', brain_probability_mask='path',
                 brain_template='path', segmentation_priors=['path'],
                 t1_registration_template='path', **options):
        from nipype.interfaces.ants.segmentation import CorticalThickness
        ct = CorticalThickness()
        ct.inputs.anatomical_image = anatomical_image
        ct.inputs.brain_probability_mask = brain_probability_mask
        ct.inputs.brain_template = brain_template
        ct.inputs.segmentation_priors = segmentation_priors
        ct.inputs.t1_registration_template = t1_registration_template
        for ef in options:
            setattr(ct.inputs, ef, options[ef])
        self.res = ct.run()

    def BrainExtractionMask(self: 'path'):
        return self.res.outputs.BrainExtractionMask

    def BrainSegmentation(self: 'path'):
        return self.res.outputs.BrainSegmentation

    def BrainSegmentationN4(self: 'path'):
        return self.res.outputs.BrainSegmentationN4

    def BrainSegmentationPosteriors(self: 'list_path'):
        return self.res.outputs.BrainSegmentationPosteriors

    def BrainVolumes(self: 'path'):
        return self.res.outputs.BrainVolumes

    def CorticalThickness(self: 'path'):
        return self.res.outputs.CorticalThickness

    def CorticalThicknessNormedToTemplate(self: 'path'):
        return self.res.outputs.CorticalThicknessNormedToTemplate

    def ExtractedBrainN4(self: 'path'):
        return self.res.outputs.ExtractedBrainN4

    def SubjectToTemplate0GenericAffine(self: 'path'):
        return self.res.outputs.SubjectToTemplate0GenericAffine

    def SubjectToTemplate1Warp(self: 'path'):
        return self.res.outputs.SubjectToTemplate1Warp

    def SubjectToTemplateLogJacobian(self: 'path'):
        return self.res.outputs.SubjectToTemplateLogJacobian

    def TemplateToSubject0Warp(self: 'path'):
        return self.res.outputs.TemplateToSubject0Warp

    def TemplateToSubject1GenericAffine(self: 'path'):
        return self.res.outputs.TemplateToSubject1GenericAffine

##############################################################################


class ants_DenoiseImage():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', save_noise=True, **options):
        from nipype.interfaces.ants import DenoiseImage
        dn = DenoiseImage()
        dn.inputs.input_image = input_image
        dn.inputs.save_noise = save_noise
        for ef in options:
            setattr(dn.inputs, ef, options[ef])
        self.res = dn.run()

    def noise_image(self: 'path'):
        return self.res.outputs.noise_image

    def output_image(self: 'path'):
        return self.res.outputs.output_image

##############################################################################


class ants_KellyKapowski():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, segmentation_image='path', **options):
        from nipype.interfaces.ants import KellyKapowski
        kk = KellyKapowski()
        kk.inputs.segmentation_image = segmentation_image
        for ef in options:
            setattr(kk.inputs, ef, options[ef])
        self.res = kk.run()

    def cortical_thickness(self: 'path'):
        return self.res.outputs.cortical_thickness

    def warped_white_matter(self: 'path'):
        return self.res.outputs.warped_white_matter

##############################################################################


class ants_LaplacianThickness():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_gm='path', input_wm='path', **options):
        from nipype.interfaces.ants import LaplacianThickness
        ct = LaplacianThickness()
        ct.inputs.input_gm = input_gm
        ct.inputs.input_wm = input_wm
        for ef in options:
            setattr(ct.inputs, ef, options[ef])
        self.res = ct.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

##############################################################################


class ants_JointFusion():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, atlas_image=[['path']], atlas_segmentation_image=['path'],
                 target_image=['path'], **options):
        from nipype.interfaces.ants import JointFusion
        jf = JointFusion()
        jf.inputs.atlas_image = atlas_image
        jf.inputs.atlas_segmentation_image = atlas_segmentation_image
        jf.inputs.target_image = target_image
        for ef in options:
            setattr(jf.inputs, ef, options[ef])
        self.res = jf.run()

    def out_atlas_voting_weight(self: 'list_path'):
        return self.res.outputs.out_atlas_voting_weight

    def out_intensity_fusion(self: 'list_path'):
        return self.res.outputs.out_intensity_fusion

    def out_label_fusion(self: 'path'):
        return self.res.outputs.out_label_fusion

    def out_label_post_prob(self: 'list_path'):
        return self.res.outputs.out_label_post_prob

##############################################################################


class ants_N4BiasFieldCorrection():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', save_bias=False,
                 copy_header=False, **options):
        from nipype.interfaces.ants import N4BiasFieldCorrection
        print(input_image)
        n4 = N4BiasFieldCorrection()
        print(n4.version)
        n4.inputs.input_image = input_image
        n4.inputs.save_bias = save_bias
        n4.inputs.copy_header = copy_header
        for ef in options:
            setattr(n4.inputs, ef, options[ef])
        n4.cmdline
        self.res = n4.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

    def bias_image(self: 'path'):
        return self.res.outputs.bias_image

##############################################################################


class ants_ThresholdImage():
    """
    Note:
        dependencies: Nipype, ANTs
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, input_image='path', copy_header=True, **options):
        from nipype.interfaces.ants import ThresholdImage
        thres = ThresholdImage()
        thres.inputs.input_image = input_image
        thres.inputs.copy_header = copy_header
        for ef in options:
            setattr(thres.inputs, ef, options[ef])
        thres.cmdline
        self.res = thres.run()

    def output_image(self: 'path'):
        return self.res.outputs.output_image

##############################################################################
