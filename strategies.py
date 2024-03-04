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

def probing_af(prevActions: np.array, memory = 10, opp_aggr_ratio = 0.5, defect_prob = 0.5, behaviour: str = 'e4e', **kwargs):
    if np.shape(prevActions)[1] < memory:
        if behaviour == 'bad':
            return np.array([0])
        else:
            return np.array([1])
    else: 
        self_first_defect = False
        opp_first_defect = False
        default_behaviour = False
        for i in np.arange(-memory, 0):
            if prevActions[0, i] == 0:
                self_first_defect = True
                break
            elif prevActions[1, i] == 0:
                opp_first_defect = True
                break
            else: 
                pass 

        if(self_first_defect or not (self_first_defect or opp_first_defect)):
            opp_tot_defect = memory - np.sum(prevActions[1, -memory:])
            if opp_tot_defect/memory < opp_aggr_ratio:
                if np.random.rand(1)[0] < defect_prob:
                    return np.array([0])
                else: 
                    default_behaviour = True
            else: 
                default_behaviour = True
        else: 
            default_behaviour = True
        
        if default_behaviour == True: 
            if behaviour == 'e4e' or behaviour == 'bad':
                return prevActions[1, -1]
            else: 
                return np.array([1])
        else: 
            print("probing_af: fatal error ahaahaaaaaaaaa")
            return -1

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

def diffident_e4e_af(prevActions: np.array, **kwargs):
    if np.size(prevActions) == 0:
        return np.array([0])
    else: 
        return prevActions[1, -1] 

def very_diffident_e4e_af(prevActions: np.array, **kwargs):
    if np.shape(prevActions)[1] < 2:
        return np.array([0])
    else: 
        if prevActions[1, -1] == 1 and prevActions[1, -2] == 1:
            return np.array([1])
        else:
            return np.array([0])

e4e = prd.Strategy("e4e", e4e_af) 
random = prd.Strategy("Random", random_af)
nice = prd.Strategy("Nice", nice_af)
nasty = prd.Strategy("Nasty", nasty_af)
nice_e4e = prd.Strategy("nice_e4e", nice_e4e_af)
diffident_e4e = prd.Strategy("diffident_e4e", diffident_e4e_af)
very_diffident_e4e = prd.Strategy("very_diffident_e4e", very_diffident_e4e_af)
grudge_5 = prd.Strategy("grudge_5", grudge_af, action_func_parameters={"memory": 5})
grudge_10 = prd.Strategy("grudge_10", grudge_af, action_func_parameters={"memory": 10})
probing_5 = prd.Strategy("probing_5", probing_af, action_func_parameters={"memory": 5, "confident_ratio": 0.5, "defect_prob": 0.5})
probing_10 = prd.Strategy("probing_10", probing_af, action_func_parameters={"memory": 10, "confident_ratio": 0.5, "defect_prob": 0.5})
probing_shy = prd.Strategy("probing_shy", probing_af, action_func_parameters={"memory": 20, "confident_ratio": 0.2, "defect_prob": 0.5})
probing_trembling = prd.Strategy("probing_tembling", probing_af, action_func_parameters={"memory": 20, "confident_ratio": 0.5, "defect_prob": 0.8})
probing_good = prd.Strategy("probing_good", probing_af, action_func_parameters={"memory": 20, "confident_ratio": 0.5, "defect_prob": 0.5, "behaviour": "good"})
probing_bad = prd.Strategy("probing_bad", probing_af, action_func_parameters={"memory": 20, "confident_ratio": 0.5, "defect_prob": 0.5, "behaviour": "bad"})
