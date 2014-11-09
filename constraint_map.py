

class ConstraintMap(object):

    def __init__(self, strings, functions):
        self.constraintMap = []
        for t in zip(strings, functions):
            self.constraintMap.append(t)

    def __getitem__(self, string):

        matchingStrings = []
        matchinFunctions = []

        for t in self.constraintMap:
            prefix = string + '.'
            if t[0].startswith(prefix):
                matchingStrings.append(t[0][len(prefix):])
                matchingFunctions.append(t[1])

        return ConstraintMap(matchingStrings, matchingFunctions)

