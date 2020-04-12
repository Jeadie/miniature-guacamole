# Overview
Code was only written for Q4. 

## Usage
To run the MDP for a given set of probabilities p_s, p_r, one can call the function directly: 
```
  run_value_iteration(p_s=x, p_r=y)
```
Whereby 0 <=x,y <= 1. Currently (for assignment appendix reasons) the value function is printed for each iteration of the value iteration algorithm. It is recommended that this is removed for future use. This can be done by removing print statements at MDP.py:84

Alternatively, to run the file (which will run all 6 p_r, p_s cases): 
```
  python3 MDP.py
```
