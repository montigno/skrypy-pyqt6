class BrukerInformationParser():

    def __init__(self, methodFileName='path', acqpFileName='path', visuParsFileName='path',
                 applyVisuCoreTransformation=True):

        import os
        import sys
        import shutil
        import math

        global math

        f = open(methodFileName, 'r')
        methodLines = f.readlines()
        f.close()

        f = open(visuParsFileName, 'r')
        visuParsLines = f.readlines()
        f.close()

        self._sliceOrientation = self.__getString(methodLines,
                                                  'PVM_SPackArrSliceOrient')
        self._readOrientation = self.__getString(methodLines,
                                                 'PVM_SPackArrReadOrient')

        # initializing the rotation matrix to identity
        self._rotation = [[float(1), float(0), float(0)],
                          [float(0), float(1), float(0)],
                          [float(0), float(0), float(1)]]
        # and customizing it according to slice and read orientations
        if (self._sliceOrientation == 'sagittal' and
                self._readOrientation == 'H_F'):
            self._rotation = [[float(0), float(0), float(1)],
                              [float(0), float(-1), float(0)],
                              [float(1), float(0), float(0)]]

        elif (self._sliceOrientation == 'coronal' and
                self._readOrientation == 'H_F'):
            self._rotation = [[float(0), float(1), float(0)],
                              [float(0), float(0), float(1)],
                              [float(1), float(0), float(0)]]

        elif (self._sliceOrientation == 'axial' and
                self._readOrientation == 'L_R'):
            self._rotation = [[float(0), float(1), float(0)],
                              [float(0), float(0), float(1)],
                              [float(1), float(0), float(0)]]

        self._visuCoreOrientationMatrix = self.__getMatrix(visuParsLines,
                                                           'VisuCoreOrientation')
        self.dwEffBValues = self.__getFloatVector(methodLines, 'PVM_DwEffBval')
        self._dwDir = self.__getMatrix(methodLines, 'PVM_DwDir')

        self._rdhToLdhTransformation3d = [[-1.0, 0.0, 0.0],
                                          [0.0, +1.0, 0.0],
                                          [0.0, 0.0, +1.0]]

        self._ldhToRvhTransformation3d = [[-1.0, 0.0, 0.0],
                                          [0.0, -1.0, 0.0],
                                          [0.0, 0.0, +1.0]]

        self.diffusionGradientOrientations = []

        for o in self._dwDir:
            orientation = o
            if (applyVisuCoreTransformation is True):
                # convert from physical frame to the subject coordinate system
                orientation = self.__computeMatrixDotVector(self._visuCoreOrientationMatrix,
                                                            orientation)
                # convert from RDH frame to LDH frame
                orientation = self.__computeMatrixDotVector(self._rdhToLdhTransformation3d,
                                                            orientation)
                # convert from LDH frame to RVH frame
                orientation = self.__computeMatrixDotVector(self._ldhToRvhTransformation3d,
                                                            orientation)
            else:
                orientation = self.__computeMatrixDotVector(self._rotation,
                                                            orientation)
            self.diffusionGradientOrientations.append(orientation)

    def __getLines(self, fileNameLines, fieldName):
        startIndex = 0
        index = 0
        for line in fileNameLines:
            if ('##$' + fieldName + '=' in line):
                startIndex = index
                break
            index += 1
        lines = []
        lines.append(fileNameLines[startIndex]
                                  [len('##$' + fieldName + '='): -1])
        endIndex = startIndex + 1
        while ('##$' not in fileNameLines[endIndex] and
               '$$' not in fileNameLines[endIndex]):
            lines.append(fileNameLines[endIndex][: -1])
            endIndex += 1
        return lines

    def __getMatrix(self, fileNameLines, fieldName):
        lines = self.__getLines(fileNameLines, fieldName)
        sizeItems = lines[0][1: -1].split(',')
        items = []
        for line in lines[1:]:
            items += line.split()
        values = []
        for item in items:
            values.append(float(item))
        sizes = []
        if (len(sizeItems) == 3):
            sizes = [int(sizeItems[0]),
                     int(sizeItems[1]),
                     int(sizeItems[2])]
        elif (len(sizeItems) == 2):
            if (int(sizeItems[0]) == 1):
                sizes = [int(sizeItems[0]),
                         int(math.sqrt(float(sizeItems[1]))),
                         int(math.sqrt(float(sizeItems[1])))]
            else:
                sizes = [1,
                         int(sizeItems[0]),
                         int(sizeItems[1])]
        result = []
        if (sizes[0] == 1):
            index = 0
            for i in range(0, sizes[1]):
                result.append([])
                for j in range(0, sizes[2]):
                    result[i].append(values[index])
                    index += 1
        else:
            print('getMatrix(): sizes[ 0 ] > 1 not managed')
        return result

    def __getFloatVector(self, fileNameLines, fieldName):
        lines = self.__getLines(fileNameLines, fieldName)
        size = int(lines[0][1: -1])
        items = []
        for line in lines[1:]:
            items += line.split()
        values = []
        for item in items:
            values.append(float(item))
        result = []
        for i in range(0, size):
            result.append(values[i])
        return result

    def __getString(self, fileNameLines, fieldName):
        lines = self.__getLines(fileNameLines, fieldName)
        if (lines[0][0] == '('):
            return lines[1]
        return lines[0]

    def __computeMatrixDotVector(self, A, b):
        r = [0.0, 0.0, 0.0]
        for i in range(0, 3):
            for j in range(0, 3):
                r[i] += A[i][j] * b[j]
        return r

    def getDiffusionGradientOrientations(self: 'array_float'):
        return self.diffusionGradientOrientations

    def getBValues(self: 'list_float'):
        return self.dwEffBValues
