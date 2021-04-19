ruleTable = {
    "NB": {
        "NB": "NVVB",
        "N": "NVB",
        "ZO": "NB",
        "P": "N",
        "PB": "Z"
    },

    "N": {
        "NB": "NVB",
        "N": "NB",
        "ZO": "N",
        "P": "Z",
        "PB": "P"
    },

    "ZO": {
        "NB": "NB",
        "N": "N",
        "ZO": "Z",
        "P": "P",
        "PB": "PB"
    },

    "P": {
        "NB": "N",
        "N": "Z",
        "ZO": "P",
        "P": "PB",
        "PB": "PVB"
    },

    "PB": {
        "NB": "Z",
        "N": "P",
        "ZO": "PB",
        "P": "PVB",
        "PB": "PVVB"
    },

    "PVB": {
        "NB": "P",
        "N": "PB",
        "ZO": "PVB",
        "P": "PVVB",
        "PB": "PVVB"
    },

    "NVB": {
        "NB": "NVVB",
        "N": "NVVB",
        "ZO": "NVB",
        "P": "NB",
        "PB": "N"
    }
}

thetaAngleIntervals = {
    "NVB": ("-", -40, -25),
    "NB": (-40, -25, -10),
    "N": (-20, -10, 0),
    "ZO": (-5, 0, 5),
    "P": (0, 10, 20),
    "PB": (10, 25, 40),
    "PVB": (25, 40, "-")
}

omegaSpeedIntervals = {
    "NB": ("-", -8, -3),
    "N": (-6, -3, 0),
    "ZO": (-1, 0, 1),
    "P": (0, 3, 6),
    "PB": (3, 8, "-")
}

tractionForceIntervals = {
    "NVVB": ("-", -32, -24),
    "NVB": (-32, -24, -16),
    "NB": (-24, -16, -8),
    "N": (-16, -8, 0),
    "Z": (-4, 0, 4),
    "P": (0, 8, 16),
    "PB": (8, 16, 24),
    "PVB": (16, 24, 32),
    "PVVB": (24, 32, "-")
}


def triangularMembershipFunction(x, lowerLimit, middlePoint, upperLimit):
    if (lowerLimit == "-" and x <= middlePoint) or (upperLimit == "-" and x >= middlePoint):
        return 1

    if lowerLimit != "-" and lowerLimit <= x < middlePoint:
        return (x - lowerLimit) / (middlePoint - lowerLimit)

    if upperLimit != "-" and middlePoint <= x < upperLimit:
        return (upperLimit - x) / (upperLimit - middlePoint)

    return 0


def computeTheMembershipValuesOfTheInput(inputParameter, intervals):
    membershipValues = {}
    for key in intervals:
        membershipValues[key] = triangularMembershipFunction(inputParameter, intervals[key][0], intervals[key][1], intervals[key][2])
    return membershipValues


def computeForceMembership(thetaMembership, omegaMembership):
    forceMembership = {}
    for thetaLinguisticVariable in ruleTable:
        for omegaLinguisticVariable, force in ruleTable[thetaLinguisticVariable].items():
            value = min(thetaMembership[thetaLinguisticVariable], omegaMembership[omegaLinguisticVariable])
            forceMembership[force] = value if force not in forceMembership else max(value, forceMembership[force]) 

    return forceMembership


def solver(t, w):
    thetaMembership = computeTheMembershipValuesOfTheInput(t, thetaAngleIntervals)
    omegaMembership = computeTheMembershipValuesOfTheInput(w, omegaSpeedIntervals)
    forceMembership = computeForceMembership(thetaMembership, omegaMembership)

    sumOfValues = sum(forceMembership.values())
    if sumOfValues == 0:
        return None

    middleValues = {key: value[1] for key, value in tractionForceIntervals.items()}
    return sum(forceMembership[fuzzySet] * middleValues[fuzzySet] for fuzzySet in forceMembership.keys()) / sumOfValues