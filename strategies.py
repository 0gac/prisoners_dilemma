import numpy as np
import prisoner_dilemma as prd
def e4e_af(prevActions: np.array, **kwargs):
    return prevActions[1, -1]  

def nice_af(prevActions: np.array, **kwargs):
    return np.array([1])

def nasty_af(prevActions: np.array, **kwargs):
    return np.array([0])

def random_af(prevActions: np.array, **kwargs):
    return np.array([np.random.randint(0, 2)])

def probing_af(prevActions: np.array, **kwargs):
    self_first_defect = False
    opp_first_defect = False
    for i in range(np.shape(prevActions)[1]):
        if prevActions[0, i] == 0:
            self_first_defect = True
            break
        if prevActions[1, i] == 0:
            opp_first_defect = True
            break 
    if(self_first_defect or not (self_first_defect or opp_first_defect)):
        opp_tot_defect = np.shape(prevActions)[1] - np.sum(prevActions[1])
        if opp_tot_defect/np.shape(prevActions)[1] < 0.5:
            if np.random.rand(1)[0] < 0.5:
                return np.array([0])
    return prevActions[1, -1]

def grudge_af(prevActions: np.array, **kwargs):
    if np.sum(prevActions[1]) != np.shape(prevActions)[1]:
        return np.array([0])
    else:
        return np.array([1])

def nice_e4e_af(prevActions: np.array, **kwargs):
    if prevActions[1, -1] == 0 and prevActions[1, -2]:
        return np.array([0])
    else: 
        return np.array([1])

e4e = prd.Strategy("e4e", e4e_af, nice_af) 
random = prd.Strategy("Random", random_af, random_af)
nice = prd.Strategy("Nice", nice_af, nice_af)
nasty = prd.Strategy("Nasty", nasty_af, nasty_af)
probing_5 = prd.Strategy("probing_5", probing_af, nice_af, prevConsidered=5)
probing_10 = prd.Strategy("probing_10", probing_af, nice_af, prevConsidered=10)
grudge_5 = prd.Strategy("grudge_5", grudge_af, nice_af, prevConsidered=5)
grudge_10 = prd.Strategy("grudge_10", grudge_af, nice_af, prevConsidered=10)
nice_e2e = prd.Strategy("nice_e4e", nice_e4e_af, nice_af, prevConsidered=2)