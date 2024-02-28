import numpy as np
import matplotlib.pyplot as plt 

class Strategy:
    '''
    object to represent a strategy in the iterated prisoner's dilemma game
    '''
    def __init__(self, name: str, action_function, action_func_trans, prevConsidered: int=1):
        '''
        name: string
        prevConsidered: int, number of previous moves to consider
        action_function: function, takes in a np.array of shape (n, 2) where n is the number of moves played so far by the opponent
        action_func_trans: behaviur of the action function when the number of moves played by the opponent is less than prevConsidered: 
            - function to specify the behaviour
            - 'Nice' (default): always cooperate
            - 'Nasty': always defect
        '''
        self.name: str = name
        self.prevConsidered = prevConsidered
        self.action_func = action_function
        self.action_func_trans = action_func_trans
        self.nice_trans = False
        self.nasty_trans = False
    def __repr__(self):
        return self.name

    def action(self, prevActions: np.array, action_func_parameters: dict):
        '''
        Carries out the decision making process for the strategy for the singular move
        prevActions: np.array of shape (n,2) where n is the number of moves played so far
        '''
        moveNum = np.shape(prevActions)[1]
        # normal behaviour
        if(moveNum >= self.prevConsidered):
            return self.action_func(prevActions, **action_func_parameters)
        # transition behaviour
        else: 
            return self.action_func_trans(prevActions, **action_func_parameters)

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
                 score_bothDef: int = 1,
                 action_func_parameters: dict = {}):
        
        self.strat1 = strat1
        self.strat2 = strat2
        self.is_numRound_random = False
        self.score_singleCoop_cooperant = score_singleCoop_cooperant
        self.score_singleCoop_defectant = score_singleCoop_defectant
        self.score_bothCoop = score_bothCoop
        self.score_bothDef = score_bothDef
        self.action_func_parameters = action_func_parameters
        if sigma_randomRounds is not False:
            self.is_numRound_random = True
            self.sigma_randomRound = sigma_randomRounds
        self.repetitions = repetitions
        self.verbose = verbose
        self.score = np.zeros((repetitions, 2))
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
                strat1_prevMoves = np.vstack((self.strat1_actions[i, :j], self.strat2_actions[i, :j]))
                strat2_prevMoves = np.vstack((self.strat2_actions[i, :j], self.strat1_actions[i, :j]))
                strat1_action = self.strat1.action(strat1_prevMoves, self.action_func_parameters)
                strat2_action = self.strat2.action(strat2_prevMoves, self.action_func_parameters)
                self.strat1_actions[i, j] = strat1_action
                self.strat2_actions[i, j] = strat2_action
                # if(self.verbose):
                #     print("Round: ", j)
                #     print("Strat1 (", self.strat1.name, ") : ", strat1_action)
                #     print("Strat2 (", self.strat2.name, ") : ", strat2_action)
                # scoring
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



