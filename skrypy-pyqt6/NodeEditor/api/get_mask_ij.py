import numpy as np
from matplotlib.path import Path
from matplotlib import patches, lines


class get_mask():

    def __init__(self, w, h, roi, color):
        self.shift_coord = 0.5
        self.msk, self.plt = None, None
        self.ptch, self.fll = None, None
        self.color = color
        if roi['type'] in ['polygon', 'freehand', 'traced']:
            roi_x, roi_y = roi['x'], roi['y']
            roi_x, roi_y = np.subtract(roi_x, self.shift_coord), np.subtract(roi_y, self.shift_coord)
            roi_coord = np.array([roi_x, roi_y])
            roi_coord = np.transpose(roi_coord)
            self.msk = self.create_poly_mask(w, h, roi_coord)
            self.fll = (roi_x, roi_y)
        elif roi['type'] == 'rectangle':
            roi_coord = np.array([roi['left'],
                   roi['top'],
                   roi['width'],
                   roi['height']])
            self.msk = self.create_rectangle_mask(h, w,
                                             (roi_coord[0], roi_coord[1]),
                                             (roi_coord[2], roi_coord[3]))
            self.ptch = self.patch_rect(roi_coord[0], roi_coord[1],
                                        roi_coord[2], roi_coord[3])
        elif roi['type'] == 'oval':
            oval_left, oval_top, oval_width, oval_height = (roi['left'] - self.shift_coord,
                                                            roi['top'] - self.shift_coord,
                                                            roi['width'],
                                                            roi['height'])
            oval_xcenter, oval_ycenter = oval_left + oval_width / 2, oval_top + oval_height / 2
            self.msk = self.create_ellipse_mask(h, w,
                                                (oval_xcenter, oval_ycenter),
                                                (oval_width / 2, oval_height / 2))
            self.ptch = self.patch_ellipse(oval_xcenter, oval_ycenter, oval_width, oval_height)
        elif roi['type'] == 'line':
            roi_coord = np.array([roi['x1'], roi['x2'], roi['y1'], roi['y2']])
            
            roi_array = np.array([[roi['x1'], roi['x1'], roi['x2'], roi['x2']],
                                  [roi['y1'] + 0.5, roi['y1'] - 0.5, roi['y2'] - 0.5, roi['y2'] + 0.5]])
            roi_array = np.transpose(roi_array)
            self.msk = self.create_line_mask(w, h, roi_array)
            self.ptch = self.patch_line(roi_coord[0], roi_coord[1],
                                        roi_coord[2], roi_coord[3])
        elif roi['type'] == 'point':
            self.plt = ([roi['x'], roi['y']])

    def create_line_mask(self, nx, ny, coord):
        x, y = np.mgrid[:ny,:nx]
        coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
        line_path = Path(coord)
        mask = line_path.contains_points(coors)
        mask = mask.reshape((ny, nx))
        mask = np.transpose(mask)
        return mask

    def create_poly_mask(self, nx, ny, coord):
        x, y = np.mgrid[:ny,:nx]
        coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
        poly_path = Path(coord)
        mask = poly_path.contains_points(coors)
        mask = mask.reshape((ny, nx))
        mask = np.transpose(mask)
        return mask

    def create_ellipse_mask(self, w, h, center=None, radius=None):
        if center is None:  # use the middle of the image
            center = (int(w / 2), int(h / 2))
        if radius is None:  # use the smallest distance between the center and image walls
            radius = (int(w / 2), int(h / 2))
        Y, X = np.ogrid[:h,:w]
        dist_from_center = ((X - center[0]) / radius[0]) ** 2 + ((Y - center[1]) / radius[1]) ** 2
        return dist_from_center <= 1

    def create_rectangle_mask(self, w, h, orig=None, dim=None):
        if orig is None:
            orig = (0, 0)
        if dim is None:
            dim = (h / 2, w / 2)
        x_start, y_start = orig[0], orig[1]
        x_end, y_end = orig[0] + dim[0], orig[1] + dim[1]
        x_array = [x for x in range(x_start, x_end)]
        y_array = [y for y in range(y_start, y_end)]
        mask_rect = np.full((h, w), False)
        for i in x_array:
            for j in y_array:
                mask_rect[j][i] = True
        return mask_rect

    def patch_line(self, x1, y1, x2, y2):
        p = lines.Line2D([x1, y1], [x2, y2], lw=1, color=self.color)
        return p

    def patch_ellipse(self, oval_xcenter, oval_ycenter, oval_width, oval_height):
        p = patches.Ellipse((oval_xcenter, oval_ycenter), oval_width, oval_height,
                         angle=0.0, linewidth=1, fill=False, edgecolor=self.color, zorder=1)
        return p

    def patch_rect(self, rect_left, rect_top, rect_width, rect_height):
        p = patches.Rectangle((rect_left - self.shift_coord, rect_top - self.shift_coord), rect_width, rect_height,
                           angle=0.0, linewidth=1, fill=False, edgecolor=self.color, zorder=1)
        return p

    def mask(self):
        return self.msk
    
    def mask_coord(self):
        return np.argwhere(self.msk)

    def fill(self):
        return self.fll

    def patch(self):
        return self.ptch
    
    def plot(self):
        return self.plt
