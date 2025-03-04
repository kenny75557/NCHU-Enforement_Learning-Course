# https://deeplearningcourses.com/c/artificial-intelligence-reinforcement-learning-in-python
# https://www.udemy.com/artificial-intelligence-reinforcement-learning-in-python
from __future__ import print_function, division
from builtins import range
# Note: you may need to update your version of future
# sudo pip install -U future


import numpy as np
from grid_world import standard_grid

SMALL_ENOUGH = 1e-3 # threshold for convergence

def print_values(V, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      v = V.get((i,j), 0)
      if v >= 0:
        print(" %.2f|" % v, end="")
      else:
        print("%.2f|" % v, end="") # -ve sign takes up an extra space
    print("")


def print_policy(P, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      a = P.get((i,j), ' ')
      print("  %s  |" % a, end="")
    print("")

if __name__ == '__main__':
  # iterative policy evaluation
  # given a policy, let's find it's value function V(s)
  # we will do this for both a uniform random policy and fixed policy
  # NOTE:
  # there are 2 sources of randomness
  # p(a|s) - deciding what action to take given the state
  # p(s',r|s,a) - the next state and reward given your action-state pair
  # we are only modeling p(a|s) = uniform
  # how would the code change if p(s',r|s,a) is not deterministic?
  grid = standard_grid()

  # states will be positions (i,j)
  # simpler than tic-tac-toe because we only have one "game piece"
  # that can only be at one position at a time
  states = grid.all_states()
  
  ### uniformly random actions ###
  # initialize V(s) = 0
  V = {}
  for s in states:
    V[s] = 0
  gamma = 1.0 # discount factor
  # repeat until convergence
  cnt=0
  while True:
    biggest_change = 0 #delta: backup
    for s in states:
      old_v = V[s]
      # V(s) only has value if it's not a terminal state
      if s in grid.actions:
        #random action
        new_v = 0 # we will accumulate the answer
        opt=-9999
        p_a = 1.0 / len(grid.actions[s]) # each action has equal probability
        for a in grid.actions[s]:
          grid.set_state(s)
          r = grid.move(a)
          new_v  += p_a * (r + gamma * V[grid.current_state()])
          if(opt<new_v):
              opt = new_v
        V[s] = opt
        biggest_change = max(biggest_change, np.abs(old_v - V[s])) #找最大之後收斂
    cnt+=1

    if biggest_change < SMALL_ENOUGH:
      break
  
  print("values for value iteration:")
  print_values(V, grid)
  print('迭代次數:',cnt)
 
