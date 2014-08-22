import json
import scipy.interpolate


class VectorSpline:
    def __init__(self, matrix, times):
        self.matrix = matrix
        self.times = times

        self.splines = []
        for parameterValues in self.matrix:
            spline = scipy.interpolate.UnivariateSpline(
                    self.times, parameterValues)
            self.splines.append(spline)

    def __call__(self, time):

        #TODO: Make this pretty with a list comprehension
        returnValue = []
        for spline in self.splines:
            returnValue.append(spline(time))
        return returnValue

