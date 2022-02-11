""" Find the lowest cost way to transform a three or four letter word
into another by changing one letter at a time so that all of the
intervening strings are legal English words.  The cost of a
replacement letter can be 1 (steps), based on scrabble values
(scrabble), or based on the resulting words frequency in normal text
(frequency)
"""

import argparse
import time

from dc import DC, dictionary
from search import astar_search

usage = """
usage: python dcsolve.py word1 word2 [steps|scrabble|frequency]
  e.g. python dcsolve.py hat pin steps
"""

def dcsolver(initial="dog", goal="cat", cost='steps'):
    """ solve a dog-cat problem, print the solution, it's cost the the time taken """
    problem = DC(initial, goal, cost)
    start = time.time()
    solution = astar_search(problem)
    elapsed = time.time() - start
    if solution:
        path = ' '.join([node.state for node in solution.path()])
        path_cost = int(round(solution.path_cost))
    else:
        path = "NO SOLUTION"
        path_cost = -1
    print(f"{problem} cost:{path_cost}; time:{elapsed: .3f}; solution:{path}")

# if called from the command line, call dcsolver
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='solve dogcat prolems with several cost functions')
    p.add_argument('word1', type=str, help='initial word')
    p.add_argument('word2', type=str, help='goal word')
    p.add_argument('cost', type=str, nargs="?", default="steps", choices=["steps","scrabble","frequency"], help="cost metric")
    args = p.parse_args()
    dcsolver(args.word1, args.word2, args.cost)
        

