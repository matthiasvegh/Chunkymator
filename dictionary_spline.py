import scipy.interpolate


class DummySpline(object):

    def __init__(self, values, times=None):
        self.value = values[0]

    def __call__(self, time):
        return self.value


class DictionarySpline(object):

    def __init__(self, matrix, times, interpolatingFunction=scipy.interpolate.UnivariateSpline):
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
                valueses = [[
                    parameterValues[value][breadth]
                    for value in range(len(parameterValues))
                ]
                    for breadth in range(len(parameterValues[0]))
                ]
                spline = DictionarySpline(valueses, self.times)
            elif isinstance(parameterValues[0],
                            (dict)):
                spline = {}
                for key in parameterValues[0].keys():
                    values = []
                    for i in range(len(parameterValues)):
                        values.append(parameterValues[i][key])
                    spline[key] = DictionarySpline([values], self.times)

            else:
                spline = DummySpline(parameterValues)
            self.splines.append(spline)

    def __call__(self, time):

        returnValue = []
        for spline in self.splines:
            if isinstance(spline, (dict)):
                dictionary = {}
                for key in spline.keys():
                    dictionary[key] = spline[key](time)[0]
                returnValue.append(dictionary)
            else:
                returnValue.append(spline(time))
        return returnValue
