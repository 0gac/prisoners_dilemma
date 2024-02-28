import numpy as np
import matplotlib.pyplot as plt 

class Strategy:
    '''
    object to represent a strategy in the iterated prisoner's dilemma game
    '''
    def __init__(self, name: str, action_function, action_func_parameters: dict = {}):
        '''
        name: string
        action_function: function, takes in a np.array of shape (n, 2) where n is the number of moves played so far by the opponent
        '''
        self.name: str = name
        self.action_func = action_function
        self.action_func_parameters = action_func_parameters
    def __repr__(self):
        return self.name

    def action(self, prevActions: np.array):
        '''
        Carries out the decision making process for the strategy for the singular move
        '''
        return self.action_func(prevActions, **self.action_func_parameters)
    
    def edit_af_params(self, new_params: dict):
        '''
        edits the parameters of the action function
        '''
        for (k, v) in new_params.items():
            if k in self.action_func_parameters.keys():
                self.action_func_parameters[k] = v
            else:
                print("Strategy.edit_af_params: parameter not found")
                return -1
class Match: 
    '''
    object to represent a match between two strategies
    '''
    def __init__(self, strat1: Strategy, 
                 strat2: Strategy,
                 numRounds: int=200,
                 sigma_randomRounds=False,
                 repetitions: int=5,
                 verbose: bool=False,
                 score_singleCoop_cooperant: int = 0,
                 score_singleCoop_defectant: int = 3,
                 score_bothCoop: int = 2,
                 score_bothDef: int = 1):
        # parameters
        self.strat1 = strat1
        self.strat2 = strat2
        self.score_singleCoop_cooperant = score_singleCoop_cooperant
        self.score_singleCoop_defectant = score_singleCoop_defectant
        self.score_bothCoop = score_bothCoop
        self.score_bothDef = score_bothDef
        self.verbose = verbose
        self.repetitions = repetitions
        self.score = np.zeros((repetitions, 2))
        # setup to allow for random number of rounds
        self.is_numRound_random = False
        if sigma_randomRounds is not False:
            self.is_numRound_random = True
            self.sigma_randomRound = sigma_randomRounds
        if self.is_numRound_random is False:
            self.strat1_actions = np.zeros((repetitions, numRounds))
            self.strat2_actions = np.zeros((repetitions, numRounds))
            self.numRounds = np.repeat(numRounds, repetitions)
        if self.is_numRound_random is True:
            self.avg_numRounds = numRounds
            self.numRounds = np.zeros(repetitions, dtype=int)

    def play(self):
        '''
        main function to play the match
        '''
        for i in range(self.repetitions):
            if(self.is_numRound_random):
                self.numRounds[i] = np.random.normal(self.avg_numRounds, self.sigma_randomRound)
                self.strat1_actions = np.zeros((self.repetitions, self.numRounds[i]))
                self.strat2_actions = np.zeros((self.repetitions, self.numRounds[i]))
            for j in range(self.numRounds[i]):
                # formatting of the previous moves to feed into the action function
                strat1_prevMoves = np.vstack((self.strat1_actions[i, :j], self.strat2_actions[i, :j]))
                strat2_prevMoves = np.vstack((self.strat2_actions[i, :j], self.strat1_actions[i, :j]))
                # action
                strat1_action = self.strat1.action(strat1_prevMoves)
                strat2_action = self.strat2.action(strat2_prevMoves)
                self.strat1_actions[i, j] = strat1_action
                self.strat2_actions[i, j] = strat2_action
                # score evaluation
                if(strat1_action == 0 and strat2_action == 0):
                    self.score[i, 0] += self.score_bothDef
                    self.score[i, 1] += self.score_bothDef
                elif(strat1_action == 1 and strat2_action == 0):
                    self.score[i, 1] += self.score_singleCoop_defectant
                    self.score[i, 0] += self.score_singleCoop_cooperant
                elif(strat2_action == 1 and strat1_action == 0):
                    self.score[i, 0] += self.score_singleCoop_defectant
                    self.score[i, 1] += self.score_singleCoop_cooperant
                else:
                    self.score[i, 0] += self.score_bothCoop
                    self.score[i, 1] += self.score_bothCoop
                
    def printscore(self):
        '''
        prints the score of the match
        '''
        print("Score of ", self.strat1.name, " vs ", self.strat2.name)
        for i in range(self.repetitions):
            print("number of rounds: ", self.numRounds[i])
            print("Strat1 (", self.strat1.name, ") : ", self.score[i, 0])
            print("Strat2 (", self.strat2.name, ") : ", self.score[i, 1])
            if self.verbose:
                print("moves:")
                s1 = ""
                for j in range(self.numRounds[i]):
                    s1 += str(self.strat1_actions[i, j]) + "\t"
                s2 = ""
                for j in range(self.numRounds[i]):
                    s2 += str(self.strat2_actions[i, j]) + "\t"
                print(s1)
                print(s2)
    
    def avgscore(self):
        return np.mean(self.score, axis = 0)



