import numpy as np
import prisoner_dilemma as prd
def e4e_af(prevActions: np.array, **kwargs):
    if np.size(prevActions) == 0:
        return np.array([1])
    else: 
        return prevActions[1, -1]  

def nice_af(prevActions: np.array, **kwargs):
    return np.array([1])

def nasty_af(prevActions: np.array, **kwargs):
    return np.array([0])

def random_af(prevActions: np.array, **kwargs):
    return np.array([np.random.randint(0, 2)])

def probing_af(prevActions: np.array, memory = 10, **kwargs):
    if np.shape(prevActions)[1] < memory:
        return np.array([1])
    else: 
        self_first_defect = False
        opp_first_defect = False
        for i in np.arange(-memory, 0):
            if prevActions[0, i] == 0:
                self_first_defect = True
                break
            if prevActions[1, i] == 0:
                opp_first_defect = True
                break 
        if(self_first_defect or not (self_first_defect or opp_first_defect)):
            opp_tot_defect = memory - np.sum(prevActions[1, -memory:])
            if opp_tot_defect/memory < 0.5:
                if np.random.rand(1)[0] < 0.5:
                    return np.array([0])
        return prevActions[1, -1]

def grudge_af(prevActions: np.array, memory = 10, **kwargs):
    if np.shape(prevActions)[1] == 0: # first move 
        return np.array([1])
    elif np.shape(prevActions)[1] < memory: # moves < memory the logic breaks lol and np.shape(prevActions)[1] must be used instead of memory
        if np.sum(prevActions[1, -np.shape(prevActions)[1]:]) != np.shape(prevActions)[1]:
            return np.array([0])
        else:
            return np.array([1])
    else: # works nicely 
        if np.sum(prevActions[1, -memory:]) != memory:
            return np.array([0])
        else:
            return np.array([1])

def nice_e4e_af(prevActions: np.array, **kwargs):
    if np.shape(prevActions)[1] < 2:
        return np.array([1])
    else:
        if prevActions[1, -1] == 0 and prevActions[1, -2]:
            return np.array([0])
        else: 
            return np.array([1])

e4e = prd.Strategy("e4e", e4e_af) 
random = prd.Strategy("Random", random_af)
nice = prd.Strategy("Nice", nice_af)
nasty = prd.Strategy("Nasty", nasty_af)
nice_e2e = prd.Strategy("nice_e4e", nice_e4e_af)
probing_10 = prd.Strategy("probing_10", probing_af, action_func_parameters={"memory": 10})
grudge_10 = prd.Strategy("grudge_10", grudge_af, action_func_parameters={"memory": 10})
probing_5 = prd.Strategy("probing_5", probing_af, action_func_parameters={"memory": 5})
grudge_5 = prd.Strategy("grudge_5", grudge_af, action_func_parameters={"memory": 5})