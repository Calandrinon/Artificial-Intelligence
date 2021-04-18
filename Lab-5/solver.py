ruleTable = {
    ("PVB", "PB"): "PVVB",
    ("PVB", "P"): "PVVB",
    ("PVB", "ZO"): "PVB",
    ("PVB", "N"): "PB",
    ("PVB", "NB"): "P",

    ("PB", "PB"): "PVVB",
    ("PB", "P"): "PVB",
    ("PB", "ZO"): "PB",
    ("PB", "N"): "P",
    ("PB", "NB"): "Z",

    ("P", "PB"): "PVB",
    ("P", "P"): "PB",
    ("P", "ZO"): "P",
    ("P", "N"): "Z",
    ("P", "NB"): "N",

    ("ZO", "PB"): "PB",
    ("ZO", "P"): "P",
    ("ZO", "ZO"): "Z",
    ("ZO", "N"): "N",
    ("ZO", "NB"): "NB",

    ("N", "PB"): "P",
    ("N", "P"): "Z",
    ("N", "ZO"): "N",
    ("N", "N"): "NB",
    ("N", "NB"): "NVB",

    ("NB", "PB"): "Z",
    ("NB", "P"): "N",
    ("NB", "ZO"): "NB",
    ("NB", "N"): "NVB",
    ("NB", "NB"): "NVVB",

    ("NVB", "PB"): "N",
    ("NVB", "P"): "NB",
    ("NVB", "ZO"): "NVB",
    ("NVB", "N"): "NVVB",
    ("NVB", "NB"): "NVVB"
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

def triangularMembershipFormula(x, lowerLimit, middleValue, upperLimit):
    if lowerLimit != "-" and lowerLimit <= x < middleValue:
        return (x - lowerLimit) / (middleValue - lowerLimit)

    if upperLimit != "-" and middleValue <= x < upperLimit:
        return (upperLimit - x) / (upperLimit - middleValue)

    if lowerLimit == "-" and x <= middleValue:
        return 1

    if upperLimit == "-" and x >= middleValue:
        return 1

    return 0


def computeMembershipDegreesForTheInputParameter(inputParameter, fuzzyIntervals):
    membershipDegrees = {}
    for linguisticVariable in fuzzyIntervals:
        membershipDegrees[linguisticVariable] = triangularMembershipFormula(inputParameter, fuzzyIntervals[linguisticVariable][0], fuzzyIntervals[linguisticVariable][1], fuzzyIntervals[linguisticVariable][2]) 

    return membershipDegrees 


def evaluateRules(thetaMembershipValues, omegaMembershipValues):
    values = {}
    for rule in ruleTable:
        values[rule] = min(thetaMembershipValues[rule[0]], omegaMembershipValues[rule[1]])

    return values 


def computeForceMembershipDegree(evaluatedRules):
    values = {}
    for rule in ruleTable:
        if ruleTable[rule] not in values:
            values[ruleTable[rule]] = evaluatedRules[rule]
        else:
            values[ruleTable[rule]] = max(evaluatedRules[rule], values[ruleTable[rule]])

    return values


def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """    
    thetaMembershipValues = computeMembershipDegreesForTheInputParameter(t, thetaAngleIntervals)
    omegaMembershipValues = computeMembershipDegreesForTheInputParameter(w, omegaSpeedIntervals)    
    tractionForceValues = evaluateRules(thetaMembershipValues, omegaMembershipValues)
    evaluatedRules = evaluateRules(thetaMembershipValues, omegaMembershipValues)
    forceMembershipDegree = computeForceMembershipDegree(evaluatedRules)

    denominator = sum(forceMembershipDegree.values())
    if denominator == 0:
        return None 

    middleValues = [interval[1] for interval in tractionForceIntervals.values()] 
    print("middleValues: ", middleValues)
    print("forceMembershipDegree: ", forceMembershipDegree)

    numerator = 0
    forceMembershipValues = [x[1] for x in forceMembershipDegree.items()]
    print("forceMembershipValues: ", forceMembershipValues)
    for i in range(0, len(middleValues)):
        numerator += forceMembershipValues[i] * middleValues[i]

    return numerator / denominator