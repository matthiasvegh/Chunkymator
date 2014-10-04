import scipy.interpolate


def jsonSchemaCheck(jsons):
    keyses = [set(json.keys()) for json in jsons]
    if keyses.count(keyses[0]) != len(keyses):
        return False

    for key in jsons[0].keys():
        valueTypes = [type(json[key]) for json in jsons]
        if valueTypes.count(valueTypes[0]) != len(valueTypes):
            return False
        if isinstance(jsons[0][key], (dict)):
            subdictionaries = [json[key] for json in jsons]
            if not jsonSchemaCheck(subdictionaries):
                return False
    return True


class DummySpline(object):

    def __init__(self, times, values):
        self.value = values[0]

    def __call__(self, time):
        return self.value

class ConstraintSpline(object):

    def __init__(self, splineFunction, times, values, constraint=None):
        self.spline = splineFunction(times, values)
        self.constraint = constraint

    def __call__(self, time):
        value = self.spline(time)
        if self.constraint is not None:
            return self.constraint(value)
        return value


class DictionarySpline(object):

    def __init__(self, times, matrix, interpolatingFunction=scipy.interpolate.UnivariateSpline):
        self.matrix = matrix
        self.times = times
        self.interpolator = interpolatingFunction

        self.splines = []
        for parameterValues in self.matrix:
            if isinstance(parameterValues[0],
                          (int, long, float, complex)):
                if(parameterValues.count(parameterValues[0]) ==
                        len(parameterValues)):
                    spline = DummySpline(self.times, parameterValues)
                else:
                    if isinstance(parameterValues[0], (int, long)):
                        constraint = round
                    else:
                        constraint = None
                    spline = ConstraintSpline(self.interpolator,
                        self.times, parameterValues,
                        constraint=constraint)
            elif isinstance(parameterValues[0],
                            (tuple, list)):
                valueses = [[
                    parameterValues[value][breadth]
                    for value in range(len(parameterValues))
                ]
                    for breadth in range(len(parameterValues[0]))
                ]
                spline = ConstraintSpline(DictionarySpline, self.times, valueses,
                        constraint=type(parameterValues[0]))
            elif isinstance(parameterValues[0],
                            (dict)):
                spline = {}
                for key in parameterValues[0].keys():
                    values = []
                    for i in range(len(parameterValues)):
                        values.append(parameterValues[i][key])
                    spline[key] = DictionarySpline(self.times, [values])

            else:
                spline = DummySpline(self.times, parameterValues)
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
