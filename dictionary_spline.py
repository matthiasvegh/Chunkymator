import json
import scipy.interpolate


class DummySpline:
    def __init__(self, values):
        self.value = values[0]
    def __call__(self, time):
        return self.value

class VectorSpline:
    def __init__(self, matrix, times, interpolatingFunction=
            scipy.interpolate.UnivariateSpline):
        self.matrix = matrix
        self.times = times
        self.interpolator = interpolatingFunction

        self.splines = []
        for parameterValues in self.matrix:
            if isinstance(parameterValues[0],
                    (int, long, float, complex)):
                if(parameterValues.count(parameterValues[0]) ==
                        len(parameterValues)):
                    spline = DummySpline(parameterValues)
                else:
                    spline = self.interpolator(
                        self.times, parameterValues)
            elif isinstance(parameterValues[0],
                    (tuple, list)):
                valueses = []
                for breadth in range(len(parameterValues[0])):
                    values = []
                    for value in range(len(parameterValues)):
                        values.append(parameterValues[value][breadth])
                    valueses.append(values)

                spline = VectorSpline(valueses, self.times)
            elif isinstance(parameterValues[0],
                    (dict)):
                spline = {}
                for key in parameterValues[0].keys():
                    values = []
                    for i in range(len(parameterValues)):
                        values.append(parameterValues[i][key])
                    spline[key] = VectorSpline([values], self.times)

            else:
                spline = DummySpline(parameterValues)
            self.splines.append(spline)

    def __call__(self, time):

        returnValue = []
        for spline in self.splines:
            if isinstance(spline,
                    (tuple, list)):
                subSplineValues = []
                for subSpline in spline:
                    subSplineValues.append(subSpline(time))
                returnValue.append(subSplineValues)
            elif spline.__class__.__name__ == self.__class__.__name__:
                returnValue.append(spline(time))
            elif isinstance(spline, (dict)):
                dictionary = {}
                for key in spline.keys():
                    dictionary[key] = spline[key](time)[0]
                returnValue.append(dictionary)
            else:
                returnValue.append(spline(time))
        return returnValue

