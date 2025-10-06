class T1Map_LevenbergM():
    def __init__(self,
                 image=[[0.0]],
                 model="enumerate(('a*(1-exp(-bx))','a*(1-exp(-bx))+c'))",
                 offset_time=0,
                 min_amp=20000.0,
                 iteration=5,
                 listEcho=[0.0]):

        from lmfit import Minimizer, Parameters, report_fit
        import numpy as np
        from itertools import product
        import ray

        @ray.remote(num_returns=3)
        def _goFit(img):
            row = img.shape[0]
            column = img.shape[1]
            a = np.zeros((row, column))
            b = np.zeros((row, column))
            c = np.zeros((row, column))
            for j, k in product(range(row), range(column)):
                a[j, k], b[j, k], c[j, k] = _process(img[j, k])
            return a, b, c

        def _fcn2min(params, lstEch, data):
            amp = params['amp']
            shift = params['shift']
            decay = params['decay']
            if model == 'a*(1-exp(-bx))+c':
                mod = amp * (1 - np.exp(-lstEch / decay)) + shift
            else:
                mod = amp * (1 - np.exp(-lstEch / decay))
            return mod - data

        def _process(dataproc):
            y = dataproc[offset_time:]
            lstEch = self.listEcho[offset_time:]
            ymax = y[-1]
            if ymax < min_amp:
                t1 = -1.0
                magn = 0.0
                shift = 0.0
                return t1, magn, shift
            yT1 = ymax * (1 - np.exp(-1))
            idx = (np.abs(y - yT1)).argmin()
            t1_init = lstEch[idx]
            try:
                params.add('amp', value=ymax)
                params.add('decay', value=t1_init)
                params.add('shift', value=0.0)
                minner = Minimizer(_fcn2min,
                                   params,
                                   fcn_args=(lstEch, y),
                                   max_nfev=iteration)
                result = minner.minimize()
                t1 = result.params['decay'].value
                magn = result.params['amp'].value
                shift = result.params['shift'].value
                if t1 > 5000.0:
                    t1 = -1.0
                    magn = 0.0
                    shift = 0.0
            except Exception as e:
                t1 = -1.0
                magn = 0.0
                shift = 0.0
            return t1, magn, shift

        ray.init(local_mode=True)

        self.listEcho = np.asarray(listEcho)
        self.image = np.asarray(image)
        params = Parameters()
        self.t1, self.magn, self.shift = [], [], []
        if len(self.image.shape) == 4:
            slice = self.image.shape[2]
            for j in range(slice):
                id1, id2, id3 = _goFit.remote(self.image[:, :, j, :])
                self.t1.append(id1)
                self.magn.append(id2)
                self.shift.append(id3)
            self.t1 = np.asarray(ray.get(self.t1))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))
            self.t1 = np.moveaxis(self.t1, 0, -1)
            self.magn = np.moveaxis(self.magn, 0, -1)
            self.shift = np.moveaxis(self.shift, 0, -1)
        else:
            self.t1, self.magn, self.shift = _goFit.remote(self.image)
            self.t1 = np.asarray(ray.get(self.t1))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))

        ray.shutdown()

    def T1map(self: 'array_float'):
        return self.t1

    def magnitude(self: 'array_float'):
        return self.magn

    def shift(self: 'array_float'):
        return self.shift

##############################################################################


class T2Map_LevenbergM():
    def __init__(self,
                 image=[[0.0]],
                 model="enumerate(('a*(exp(-bx))','a*(exp(-bx))+c'))",
                 offset_time=0,
                 min_amp=20000.0,
                 iteration=5,
                 listEcho=[0.0]):

        from lmfit import Minimizer, Parameters, report_fit
        import numpy as np
        from itertools import product
        import ray

        @ray.remote(num_returns=3)
        def _goFit(img):
            row = img.shape[0]
            column = img.shape[1]
            a = np.zeros((row, column))
            b = np.zeros((row, column))
            c = np.zeros((row, column))
            for j, k in product(range(row), range(column)):
                a[j, k], b[j, k], c[j, k] = _process(img[j, k])
            return a, b, c

        def _fcn2min(params, lstEch, data):
            amp = params['amp']
            decay = params['decay']
            shift = params['shift']
            if model == 'a*(exp(-bx))+c':
                mod = amp * (np.exp(-lstEch / decay)) + shift
            else:
                mod = amp * (np.exp(-lstEch / decay))
            return mod - data

        def _process(dataproc):
            y = dataproc[offset_time:]
            lstEch = self.listEcho[offset_time:]
            ymax = y[0]
            if ymax < min_amp:
                t2 = -1.0
                magn = 0.0
                shift = 0.0
                return t2, magn, shift

            yT1 = ymax * (1 - np.exp(-1))
            idx = (np.abs(y - yT1)).argmin()
            t2_init = lstEch[idx]
            try:
                params.add('amp', value=ymax)
                params.add('decay', value=t2_init)
                params.add('shift', value=0.0)
                minner = Minimizer(_fcn2min,
                                   params,
                                   fcn_args=(lstEch, y),
                                   max_nfev=iteration)
                result = minner.minimize()
                t2 = result.params['decay'].value
                magn = result.params['amp'].value
                shift = result.params['shift'].value
                if t2 > 3500.0:
                    t2 = -1
                    magn = 0.0
                    shift = 0.0

            except Exception as e:
                t2 = -1.0
                magn = 0.0
                shift = 0.0

            return t2, magn, shift

        # ray.init(ignore_reinit_error=True)
        ray.init(local_mode=True)

        self.listEcho = np.asarray(listEcho)
        self.image = np.asarray(image)
        params = Parameters()
        self.t2, self.magn, self.shift = [], [], []
        if len(self.image.shape) == 4:
            slice = self.image.shape[2]
            for j in range(slice):
                id1, id2, id3 = _goFit.remote(self.image[:, :, j, :])
                self.t2.append(id1)
                self.magn.append(id2)
                self.shift.append(id3)
            self.t2 = np.asarray(ray.get(self.t2))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))
            self.t2 = np.moveaxis(self.t2, 0, -1)
            self.magn = np.moveaxis(self.magn, 0, -1)
            self.shift = np.moveaxis(self.shift, 0, -1)
        else:
            self.t2, self.magn, self.shift = _goFit.remote(self.image)
            self.t2 = np.asarray(ray.get(self.t2))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))

        ray.shutdown()

    def T2map(self: 'array_float'):
        return self.t2

    def magnitude(self: 'array_float'):
        return self.magn

    def shift(self: 'array_float'):
        return self.shift

##############################################################################


class T2Map_LevenbergM_stderr():
    def __init__(self,
                 image=[[0.0]],
                 model="enumerate(('a*(exp(-bx))','a*(exp(-bx))+c'))",
                 offset_time=0,
                 min_amp=20000.0,
                 iteration=5,
                 listEcho=[0.0]):

        from lmfit import Minimizer, Parameters, report_fit
        import numpy as np
        from itertools import product
        import ray

        @ray.remote(num_returns=5)
        def _goFit(img):
            row = img.shape[0]
            column = img.shape[1]
            a = np.zeros((row, column))
            b = np.zeros((row, column))
            c = np.zeros((row, column))
            d = np.zeros((row, column))
            e = np.zeros((row, column))
            for j, k in product(range(row), range(column)):
                a[j, k], b[j, k], c[j, k], d[j, k], e[j, k] = _process(img[j, k])
            return a, b, c, d, e

        def _fcn2min(params, lstEch, data):
            amp = params['amp']
            decay = params['decay']
            shift = params['shift']
            if model == 'a*(exp(-bx))+c':
                mod = amp * (np.exp(-lstEch / decay)) + shift
            else:
                mod = amp * (np.exp(-lstEch / decay))
            return mod - data

        def _process(dataproc):
            y = dataproc[offset_time:]
            lstEch = self.listEcho[offset_time:]
            ymax = y[0]
            if ymax < min_amp:
                t2 = -1.0
                magn = 0.0
                shift = 0.0
                t2_stderr, magn_stderr = 0.0, 0.0
                return t2, magn, shift, t2_stderr, magn_stderr

            yT1 = ymax * (1 - np.exp(-1))
            idx = (np.abs(y - yT1)).argmin()
            t2_init = lstEch[idx]
            try:
                params.add('amp', value=ymax)
                params.add('decay', value=t2_init)
                params.add('shift', value=0.0)
                minner = Minimizer(_fcn2min,
                                   params,
                                   fcn_args=(lstEch, y),
                                   max_nfev=iteration)
                result = minner.minimize()
                t2 = result.params['decay'].value
                magn = result.params['amp'].value
                shift = result.params['shift'].value
                t2_stderr = result.params['decay'].stderr
                magn_stderr = result.params['amp'].stderr

                if not t2_stderr:
                    t2_stderr = 0.0
                if not magn_stderr:
                    magn_stderr = 0.0
                if t2 > 3500.0 or t2 < 0:
                    t2 = -1
                    magn = 0.0
                    shift = 0.0
                    t2_stderr, magn_stderr = 0.0, 0.0

            except Exception as e:
                t2 = -1.0
                magn = 0.0
                shift = 0.0
                t2_stderr, magn_stderr = 0.0, 0.0
            return t2, magn, shift, t2_stderr, magn_stderr

        # ray.init(ignore_reinit_error=True)
        ray.init(local_mode=True)

        self.listEcho = np.asarray(listEcho)
        self.image = np.asarray(image)
        params = Parameters()
        self.t2, self.magn, self.shift = [], [], []
        self.t2_stderr, self.magn_stderr = [], []
        if len(self.image.shape) == 4:
            slice = self.image.shape[2]
            for j in range(slice):
                id1, id2, id3, id4, id5 = _goFit.remote(self.image[:, :, j, :])
                self.t2.append(id1)
                self.magn.append(id2)
                self.shift.append(id3)
                self.t2_stderr.append(id4)
                self.magn_stderr.append(id5)
            self.t2 = np.asarray(ray.get(self.t2))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))
            self.t2_stderr = np.asarray(ray.get(self.t2_stderr))
            self.magn_stderr = np.asarray(ray.get(self.magn_stderr))
            self.t2 = np.moveaxis(self.t2, 0, -1)
            self.magn = np.moveaxis(self.magn, 0, -1)
            self.shift = np.moveaxis(self.shift, 0, -1)
            self.t2_stderr = np.moveaxis(self.t2_stderr, 0, -1)
            self.magn_stderr = np.moveaxis(self.magn_stderr, 0, -1)
        else:
            self.t2, self.magn, self.shift = _goFit.remote(self.image)
            self.t2 = np.asarray(ray.get(self.t2))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))
            self.t2_stderr = np.asarray(ray.get(self.t2_stderr))
            self.magn_stderr = np.asarray(ray.get(self.magn_stderr))

        ray.shutdown()

    def T2map(self: 'array_float'):
        return self.t2

    def T2map_stderr(self: 'array_float'):
        return self.t2_stderr

    def magnitude(self: 'array_float'):
        return self.magn

    def magnitude_stderr(self: 'array_float'):
        return self.magn_stderr

    def shift(self: 'array_float'):
        return self.shift

##############################################################################


class TIMap_LevenbergM():
    def __init__(self,
                 image=[[0.0]],
                 model="enumerate(('a*(1-2*exp(-bx))','a*(1-2*c*exp(-bx))'))",
                 offset_time=0,
                 min_amp=20000.0,
                 iteration=5,
                 listEcho=[0.0]):

        from lmfit import Minimizer, Parameters, report_fit
        import numpy as np
        from itertools import product
        import ray

        @ray.remote(num_returns=3)
        def _goFit(img):
            row = img.shape[0]
            column = img.shape[1]
            a = np.zeros((row, column))
            b = np.zeros((row, column))
            c = np.zeros((row, column))
            for j, k in product(range(row), range(column)):
                a[j, k], b[j, k], c[j, k] = _process(img[j, k])
            return a, b, c

        def _fcn2min(params, lstEch, data):
            amp = params['amp']
            decay = params['decay']
            shift = params['shift']
            if model == 'a*(1-2*c*exp(-bx))':
                mod = abs(amp * (1 - 2 * shift * np.exp(-lstEch / decay)))
            else:
                mod = abs(amp * (1 - 2 * np.exp(-lstEch / decay)))
            return mod - data

        def _process(dataproc):
            y = dataproc[offset_time:]
            lstEch = self.listEcho[offset_time:]
            ymax = y[-1]
            if ymax < min_amp:
                ti = -1.0
                magn = 0.0
                shift = 1.0
                return ti, magn, shift

            idx = (np.abs(y)).argmin()
            ti_init = lstEch[idx] / np.log(2)
            try:
                params.add('amp', value=ymax)
                params.add('decay', value=ti_init)
                params.add('shift', value=1.0)
                minner = Minimizer(_fcn2min,
                                   params,
                                   fcn_args=(lstEch, y),
                                   max_nfev=iteration)
                result = minner.minimize()
                ti = result.params['decay'].value
                magn = result.params['amp'].value
                shift = result.params['shift'].value
            except Exception as e:
                ti = -1.0
                magn = 0.0
                shift = 1.0
            return ti, magn, shift

        ray.init(local_mode=True)

        self.listEcho = np.asarray(listEcho)
        self.image = np.asarray(image)
        params = Parameters()
        self.ti, self.magn, self.shift = [], [], []
        if len(self.image.shape) == 4:
            slice = self.image.shape[2]
            for j in range(slice):
                id1, id2, id3 = _goFit.remote(self.image[:, :, j, :])
                self.ti.append(id1)
                self.magn.append(id2)
                self.shift.append(id3)
            self.ti = np.asarray(ray.get(self.ti))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))
            self.ti = np.moveaxis(self.ti, 0, -1)
            self.magn = np.moveaxis(self.magn, 0, -1)
            self.shift = np.moveaxis(self.shift, 0, -1)

        else:
            self.ti, self.magn, self.shift = _goFit.remote(self.image)
            self.ti = np.asarray(ray.get(self.ti))
            self.magn = np.asarray(ray.get(self.magn))
            self.shift = np.asarray(ray.get(self.shift))

        ray.shutdown()

    def TImap(self: 'array_float'):
        return self.ti

    def magnitude(self: 'array_float'):
        return self.magn

    def shift(self: 'array_float'):
        return self.shift

##############################################################################


class CEST():
    def __init__(self, y=[0.0], x=[0.0], center_freq=0.0,
                 mapping_ppm=1.0, delta_mapping=0.1, cest_center=False, **options):
        import numpy as np
        from scipy.interpolate import interp1d

        S0 = y[0]
        y = 100 * y[1:] / S0

        n_interp = options.get('n_interp', 100)
        kind_interp = options.get('kind_interp', 'cubic')

        f2 = interp1d(x, y, kind=kind_interp, bounds_error=False, fill_value=(y[0], y[-1]))
        xnew = np.linspace(x[0], x[-1], n_interp * (len(x) - 1) + len(x))
        y_fit = f2(xnew)

        xnew_corrected = []

        if cest_center:
            ind = xnew[np.where(y_fit == min(y_fit))[0][0]]
        else:
            if center_freq < 0:
                ind = abs(center_freq)
            else:
                ind = center_freq

        for i, el in enumerate(xnew):
            xnew_corrected.append(el + ind)
        y_corrected = f2(xnew_corrected)

        # indice_mini_y_corr = np.argmin(y_corrected)
        indice_mini_y_corr = int(len(xnew) / 2)

        asym = []
        # x_asym = list(xnew)[indice_mini_y_corr:]
        x_asym = list(xnew)[indice_mini_y_corr:]

        for i in range(indice_mini_y_corr, len(xnew_corrected)):
            j = indice_mini_y_corr - i
            delta_w_neg = y_corrected[indice_mini_y_corr + j]
            delta_w_pos = y_corrected[i]
            asym.append(abs(100 * (delta_w_neg - delta_w_pos) / S0))

        # ind_ppm = list(x_asym).index(mapping_ppm)
        # self.out_map = asym[ind_ppm]

        area_map = [0, 0]
        area_map[0] = mapping_ppm - delta_mapping
        area_map[1] = mapping_ppm + delta_mapping
        indx = []
        for lsm in area_map:
            absolute_difference_function = lambda list_value: abs(list_value - lsm)
            closest_value = min(x_asym, key=absolute_difference_function)
            indx.append(x_asym.index(closest_value))
        sublist_asym = asym[indx[0]:indx[1]]
        self.xspectr = xnew
        self.zpectr = y_corrected
        self.xasym = x_asym
        self.asym = asym
        self.out_map = np.mean(sublist_asym)

    def out_xspectra(self: 'list_float'):
        return self.xspectr

    def out_zspectra(self: 'list_float'):
        return self.zpectr

    def out_xasym(self: 'list_float'):
        return self.xasym

    def out_asym(self: 'list_float'):
        return self.asym

    def out_mapping(self: 'float'):
        return self.out_map

##############################################################################


class CEST_2():
    def __init__(self, y=[0.0], x=[0.0], center_freq=0.0,
                 mapping_ppm=1.0, delta_mapping=0.1, cest_center=False, **options):
        import numpy as np
        from scipy.interpolate import interp1d

        S0 = y[0]
        y = 100 * y[1:] / S0

        n_interp = options.get('n_interp', 100)
        kind_interp = options.get('kind_interp', 'cubic')

        f2 = interp1d(x, y, kind=kind_interp, bounds_error=False, fill_value=(y[0], y[-1]))
        xnew = np.linspace(x[0], x[-1], n_interp * (len(x) - 1) + len(x))
        y_fit = f2(xnew)

        xnew_corrected = []

        if cest_center:
            ind = xnew[np.where(y_fit == min(y_fit))[0][0]]
        else:
            if center_freq < 0:
                ind = abs(center_freq)
            else:
                ind = center_freq

        for i, el in enumerate(xnew):
            xnew_corrected.append(el + ind)
        y_corrected = f2(xnew_corrected)

        # indice_mini_y_corr = np.argmin(y_corrected)
        indice_mini_y_corr = int(len(xnew) / 2)

        asym = []
        # x_asym = list(xnew)[indice_mini_y_corr:]
        x_asym = list(xnew)[indice_mini_y_corr:]

        for i in range(indice_mini_y_corr, len(xnew_corrected)):
            j = indice_mini_y_corr - i
            # S0_new = y_corrected[0]
            delta_w_neg = y_corrected[indice_mini_y_corr + j]
            delta_w_pos = y_corrected[i]
            asym.append(abs(100 * (delta_w_neg - delta_w_pos) / 100))

        # ind_ppm = list(x_asym).index(mapping_ppm)
        # self.out_map = asym[ind_ppm]

        area_map = [0, 0]
        area_map[0] = mapping_ppm - delta_mapping
        area_map[1] = mapping_ppm + delta_mapping
        indx = []
        for lsm in area_map:
            absolute_difference_function = lambda list_value: abs(list_value - lsm)
            closest_value = min(x_asym, key=absolute_difference_function)
            indx.append(x_asym.index(closest_value))
        sublist_asym = asym[indx[0]:indx[1]]
        self.xspectr = xnew
        self.zpectr = y_corrected
        self.xasym = x_asym
        self.asym = asym
        self.out_map = np.mean(sublist_asym)

    def out_xspectra(self: 'list_float'):
        return self.xspectr

    def out_zspectra(self: 'list_float'):
        return self.zpectr

    def out_xasym(self: 'list_float'):
        return self.xasym

    def out_asym(self: 'list_float'):
        return self.asym

    def out_mapping(self: 'float'):
        return self.out_map

##############################################################################


class WASSR():
    def __init__(self, y=[0.0], x=[0.0]):
        import numpy as np
        import scipy.optimize as opt
        from scipy.interpolate import interp1d

        global f_interp

        S0 = y[0]
        y = 100 * y[1:] / S0

        c = x[np.where(y == min(y))[0][0]]

        f_interp = interp1d(x, y, kind='cubic', bounds_error=False, fill_value=(y[0], y[-1]))
        # (c_), q_ = opt.curve_fit(f, x, y, bounds=(0., 1.))
        (c_), q_ = opt.curve_fit(self._f,  x,  y,  c)
        n_interpol = 100
        xnew = np.linspace(x[0], x[-1], n_interpol * (len(x) - 1) + len(x), endpoint=True)
        y_fit = self._f(xnew, c_)
        self.center = float(c_[0])

        self.center_wass = c

    def _f(self, xd, c):
        x_arr = 2 * c - xd
        return f_interp(x_arr)

    def estimated_center_freq(self: 'float'):
        return self.center

    def center_wassr(self: 'float'):
        return self.center_wass

##############################################################################


class Linear_registration_multiple_images:
    def __init__(self,
                 image_fixed='path',
                 image_moved='path',
                 output_moved_name='path',
                 matrix_moved_name='path',
                 images_apply_transformation=['path'],
                 images_transformed_name=['path'],
                 cost_func="enumerate(('mutualinfo',\
                                       'corratio',\
                                       'normcorr',\
                                       'normmi',\
                                       'leastsq',\
                                       'labeldiff',\
                                       'bbr'))",
                 interp="enumerate(('trilinear',\
                                    'nearestneighbour',\
                                    'sinc',\
                                    'spline'))"):

        from nipype.interfaces import fsl
        import os

        flt = fsl.FLIRT()
        flt.inputs.in_file = image_moved
        flt.inputs.reference = image_fixed
        flt.inputs.cost_func = cost_func
        flt.inputs.out_matrix_file = matrix_moved_name
        flt.inputs.interp = interp
        flt.inputs.output_type = 'NIFTI'
        flt.inputs.out_file = output_moved_name
        res = flt.run()
        self.outfile = res.outputs.out_file
        self.outmtrx = res.outputs.out_matrix_file
        cur_dir = os.path.dirname(output_moved_name)
        flts = fsl.FLIRT()
        self.list_out_files = []
        images_apply_transformation = [x for x in images_apply_transformation if x != 'path' and x]
        i = 0
        for cur_path in images_apply_transformation:
            flts.inputs.in_file = cur_path
            flts.inputs.reference = self.outfile
            flts.inputs.interp = interp
            flts.inputs.out_file = images_transformed_name[i]
            flts.inputs.apply_xfm = True
            flts.inputs.in_matrix_file = self.outmtrx
            flts.inputs.output_type = 'NIFTI'
            resa = flts.run()
            self.list_out_files.append(resa.outputs.out_file)
            i += 1

    def out_file(self: 'path'):
        return self.outfile

    def out_matrix_file(self: 'path'):
        return self.outmtrx

    def out_other_files(self: 'list_path'):
        return self.list_out_files

##############################################################################


class Non_linear_registration_for_Atlases:
    def __init__(self,
                 image_fixed='path',
                 atlas_template_moved='path',
                 atlas_label_moved='path',
                 output_template_name='path',
                 output_label_name='path',
                 interpolator="enumerate(('linear',\
                                          'nearestNeighbor',\
                                          'multiLabel',\
                                          'genericlabel',\
                                          'gaussian',\
                                          'bSpline',\
                                          'cosineWindowedSinc',\
                                          'welchWindowedSinc',\
                                          'hammingWindowedSinc',\
                                          'lanczosWindowedSinc'))",
                 transform="enumerate(('Translation',\
                                       'Rigid',\
                                       'Similarity',\
                                       'QuickRigid',\
                                       'DenseRigid',\
                                       'BOLDRigid',\
                                       'Affine',\
                                       'AffineFast',\
                                       'BOLDAffine',\
                                       'TRSAA',\
                                       'ElasticSyN',\
                                       'SyN',\
                                       'SyNRA',\
                                       'SyNOnly',\
                                       'SyNCC',\
                                       'SyNabp',\
                                       'SyNBold',\
                                       'SyNBoldAff',\
                                       'SyNAggro',\
                                       'TVMSQ',\
                                       'TVMSQC'))",
                 **options):
        import ants
        img_fi = ants.image_read(image_fixed)
        atlas_temp_mo = ants.image_read(atlas_template_moved)
        atlas_lab_mo = ants.image_read(atlas_label_moved)
        warpedmoveout = ants.registration(fixed=img_fi,
                                          moving=atlas_temp_mo,
                                          type_of_transform=transform, **options)
        imagetransformed = ants.apply_transforms(fixed=warpedmoveout['warpedmovout'], moving=atlas_lab_mo,
                                                 transformlist=warpedmoveout['fwdtransforms'],
                                                 interpolator=interpolator)
        ants.image_write(warpedmoveout['warpedmovout'], output_template_name)
        ants.image_write(imagetransformed, output_label_name)
        self.temp_reg = output_template_name
        self.lab_reg = output_label_name

    def out_template_registred(self: 'path'):
        return self.temp_reg

    def out_label_registred(self: 'path'):
        return self.lab_reg

##############################################################################


class Non_linear_registration:
    def __init__(self,
                 image_ref='path',
                 image_in='path',
                 out_file='path',
                 interpolator="enumerate(('linear',\
                                          'nearestNeighbor',\
                                          'multiLabel',\
                                          'genericlabel',\
                                          'gaussian',\
                                          'bSpline',\
                                          'cosineWindowedSinc',\
                                          'welchWindowedSinc',\
                                          'hammingWindowedSinc',\
                                          'lanczosWindowedSinc'))",
                 transform="enumerate(('Translation',\
                                       'Rigid',\
                                       'Similarity',\
                                       'QuickRigid',\
                                       'DenseRigid',\
                                       'BOLDRigid',\
                                       'Affine',\
                                       'AffineFast',\
                                       'BOLDAffine',\
                                       'TRSAA',\
                                       'ElasticSyN',\
                                       'SyN',\
                                       'SyNRA',\
                                       'SyNOnly',\
                                       'SyNCC',\
                                       'SyNabp',\
                                       'SyNBold',\
                                       'SyNBoldAff',\
                                       'SyNAggro',\
                                       'TVMSQ',\
                                       'TVMSQC'))"):
        import ants
        img_fi = ants.image_read(image_ref)
        img_mo = ants.image_read(image_in)
        warpedmoveout = ants.registration(fixed=img_fi,
                                          moving=img_mo,
                                          type_of_transform=transform)
        ants.image_write(warpedmoveout['warpedmovout'], out_file)
        self.img_reg = out_file

    def out_image_registred(self: 'path'):
        return self.img_reg

##############################################################################


class Non_linear_registration_multiple_images:
    def __init__(self,
                 image_fixed='path',
                 image_moved='path',
                 output_moved_name='path',
                 matrix_moved_name='path',
                 images_apply_transform=['path'],
                 images_transformed_name=['path'],
                 interpolator="enumerate(('linear',\
                                          'nearestNeighbor',\
                                          'multiLabel',\
                                          'genericlabel',\
                                          'gaussian',\
                                          'bSpline',\
                                          'cosineWindowedSinc',\
                                          'welchWindowedSinc',\
                                          'hammingWindowedSinc',\
                                          'lanczosWindowedSinc'))",
                 transform="enumerate(('Translation',\
                                       'Rigid',\
                                       'Similarity',\
                                       'QuickRigid',\
                                       'DenseRigid',\
                                       'BOLDRigid',\
                                       'Affine',\
                                       'AffineFast',\
                                       'BOLDAffine',\
                                       'TRSAA',\
                                       'ElasticSyN',\
                                       'SyN',\
                                       'SyNRA',\
                                       'SyNOnly',\
                                       'SyNCC',\
                                       'SyNabp',\
                                       'SyNBold',\
                                       'SyNBoldAff',\
                                       'SyNAggro',\
                                       'TVMSQ',\
                                       'TVMSQC'))"):
        import ants
        import os
        img_fi = ants.image_read(image_fixed)
        img_mo = ants.image_read(image_moved)
        warpedmoveout = ants.registration(fixed=img_fi,
                                          moving=img_mo,
                                          type_of_transform=transform)
        warp_mov_out = warpedmoveout['warpedmovout']
        warp_mov_transf = warpedmoveout['fwdtransforms']
        self.img_tra = []
        images_apply_transform = [x for x in images_apply_transform if x != 'path' and x]
        i = 0
        for lst_img in images_apply_transform:
            out_img_transform = images_transformed_name[i]
            img_tra = ants.image_read(lst_img)
            imagetransformed = ants.apply_transforms(fixed=warp_mov_out, moving=img_tra,
                                                     transformlist=warp_mov_transf,
                                                     interpolator=interpolator)
            ants.image_write(imagetransformed, out_img_transform)
            self.img_tra.append(out_img_transform)
            i += 1
        ants.image_write(warp_mov_out, output_moved_name)
        self.matrix = matrix_moved_name
        file_mat = open(self.matrix, 'w')
        file_mat.write(str(warp_mov_transf))
        file_mat.close()
        self.img_reg = output_moved_name

    def out_image_registred(self: 'path'):
        return self.img_reg

    def out_image_transformed(self: 'list_path'):
        return self.img_tra

    def out_matrix_file(self: 'path'):
        return self.matrix

##############################################################################


class Seg_conv3D:
    def __init__(self, file_in='path', file_out_name='path', threshold=5.0, radius=9):
        from NodeEditor.modules.Images.Nifti import nifti_open_file
        from NodeEditor.modules.Images.Nifti import nifti_get_header
        from NodeEditor.modules.Images.Scipy import scipy_convolve3d
        from NodeEditor.modules.Numpy.Image_filters import numpy_threshold
        from NodeEditor.modules.Images.Nifti import nifti_save_file
        from skimage.morphology import erosion
        from skimage.morphology import dilation
        from skimage.morphology import ball
        from scipy import ndimage
        import numpy as np

        img = nifti_open_file(file_in).image()
        if len(img.shape) < 4:
            image = img
        else:
            image = img[:, :, :, 0]
        kern = [1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0]
        imgtmp = scipy_convolve3d(image, kern).Convol3d()
        imgtmp = -imgtmp
        imgtmp = numpy_threshold(imgtmp, threshold, 'high').img_threshold()
        selem = ball(radius)
        imgtmp = erosion(imgtmp, selem)
        imgtmp = dilation(imgtmp, selem)
        imgtmp = ndimage.binary_fill_holes(imgtmp, structure=np.ones((3, 3, 1)))
        if len(img.shape) < 4:
            imgtmp = np.multiply(image, imgtmp)
        else:
            for i in range(img.shape[3]):
                img[:, :, :, i] = np.multiply(img[:, :, :, i], imgtmp)
            imgtmp = img
        hdr = nifti_get_header(file_in).nii_hdr()
        self.out_file = nifti_save_file(imgtmp, file_out_name, header=hdr, out_type='nii').pathFile()

    def output_file(self: 'path'):
        return self.out_file
