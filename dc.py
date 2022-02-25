""" starter file for hw2: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file


# file name for the dictionary, with one word per line.  Each line
# will have a word followed by a tab followed by a number, e.g.
#   and     0.07358445
#   for     0.18200336

dict_file = "words34.txt.gz"

# dictionary is a dict to hold legal 3 and 4 letter words with their
# frequencies based on a sample of a large text corpus.  The dict's
# keys are the words and its values are their frequencies

# load words into the dictionary dict
dictionary = {}
for line in gzip.open(dict_file, 'rt'):
    word, n = line.strip().split('\t')
    n = float(n)
    dictionary[word] = n

class DC(search.Problem):

    """DC is a subclass of the AIMA search files's Problem class
       It's init method takes three arguments: the initial word, goal word and cost method.

       A state is represented as a lowercase string of three or four
       ascii characters.  Both the initial and goal states must be
       words of the same length and they must be in the dict
       dictionary. The cost argument specifies how to measure the
       cost of an action and can be 'steps', 'scrabble' or 'frequency'
       """
    alphabet = {
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 
        'h': 4, 'i': 1, 'j': 6, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 
        'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
        'v': 4, 'w': 4, 'x': 6, 'y': 4, 'z':10
    }

    def __init__(self, initial='dog', goal='cat', cost='steps'):

        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost_method = cost
        self.current_cost = 0
        self.dictionary = dictionary
        
        # make sure the arguments are legal, raising an error if any are bad.
        for var in  [initial, goal, cost]:
            if type(var) != str:
                raise TypeError("All arguments must be a string")

        for string in [initial, goal]:
            if len(string) != 3 and len(string) != 4:
                raise ValueError("%s must be a string of length 3 or 4." % string)

            elif string not in self.dictionary:
                raise ValueError("%s must be a string of length 3 or 4." % string)

        if len(initial) != len(goal):
            raise ValueError("%s and %s must be strings of equal length." % (initial, goal))
            

        if cost not in ["steps", "scrabble", "frequency"]:
            raise ValueError("%s is an invalid cost method" % cost)

        # if the cost method is frequency calls a helper function to calculate heuristic
        if self.cost_method == "frequency":
            self.frequency_h()


    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        valid_actions = []
        
        # iterates through the word and tries replacing each character
        # with every letter from the alphabet to check for valid words
        for i in range(len(state)):
            for letter in self.alphabet:

                temp = self.result(state, (i, letter))
                if temp in self.dictionary and temp != state:
                    valid_actions.append((i, temp[i]))
        
        return valid_actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        idx = action[0]
        return state[:idx] + action[1] + state[idx+1:]            

    def goal_test(self, state):
        return state == self.goal

    
    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get from the state state to
        state1. For the the dc problem, you will have to check what
        the cost metric is being used for this problem instance, i.e.,
        is it steps, scrabble or frequency """
        if self.cost_method == "steps":
            return c + 1
                
        elif self.cost_method == "scrabble":
            return c + self.alphabet[action[1]]

        elif self.cost_method == "frequency":
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return ("dc(%s, %s, %s)" % (self.initial, self.goal, self.cost_method))

    def frequency_h(self):
        """" helper function for calculating heuristcs if the cost method 
        is frequency calculates the minimum possible cost of a word 
        that has the same letter as the goal word at a given position """

        # an array of length = len(word) populated with 9999
        self.frequency_costs = [9999 for i in range(len(self.goal))] 

        # iterates through dictionary, calculating min possible cost 
        # of words sharing the same letter in the same poisition as the goal word
        for word in dictionary:
            if len(word) == len(self.goal):
                for i in range(len(self.goal)):
                    if self.goal[i] == word[i] and dictionary[word] < self.frequency_costs[i]:
                        self.frequency_costs[i] = dictionary[word]


    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of this node to the goal state.  The heuristic's value
        should depend on the Problem's cost parameter (steps, scrabble
        or frequency) as this will effect the estimate cost to get to
        the nearest goal. """

        estimate = 0

        # every difference in chracter adds 1 to the estimate
        if self.cost_method == "steps":
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    estimate += 1

        # every difference in character adds an amount based 
        # on the desired character's scrabble cost
        elif self.cost_method == "scrabble":
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    estimate += self.alphabet[self.goal[i]]
        
        # every difference in chracter adds the lowest possible
        # cost of a word that has the desired character at
        # the given position
        elif self.cost_method == "frequency":

            arr = []
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    arr.append(1 + self.frequency_costs[i])
            
            if len(arr) == 1:
                estimate = 1 + dictionary[self.goal]
            else:
                estimate = sum(arr) 

        return estimate



        

