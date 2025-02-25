# Name(s): Jacob Fernandez, Grant Zhao
# Netid(s): jaf388, gz233
################################################################################
# NOTE: Do NOT change any of the function headers and/or specs!
# The input(s) and output must perfectly match the specs, or else your 
# implementation for any function with changed specs will most likely fail!
################################################################################

################### IMPORTS - DO NOT ADD, REMOVE, OR MODIFY ####################
import numpy as np


def viterbi(model, observation, tags):
  """
  Returns the model's predicted tag sequence for a particular observation.
  Uses `get_tag_likelihood` method to obtain model scores at each iteration.

  Input: 
    model: HMM model
    observation: List[String]
    tags: List[String]
  Output:
    predictions: List[String]
  """
  V = [{}]
  path = {}

  # Initialize base cases (t == 0)
  for tag in tags:
    if tag != "qf":
      V[0][tag] = model.get_start_state_probs().get(tag, -np.inf) + \
        model.get_tag_likelihood(tag, None, observation, 0)
      path[tag] = [tag]

<<<<<<< HEAD
    Input: 
        model: HMM model
        observation: List[String]
        tags: List[String]
    Output:
        predictions: List[String]
    """
    V = [{}]  
    path = {}  
    
    for tag in tags:
        if tag != "qf":  
            V[0][tag] = model.get_start_state_probs().get(tag, -np.inf) + \
                        model.get_tag_likelihood(tag, None, observation, 0)
            path[tag] = [tag]  

    for t in range(1, len(observation)):
        V.append({})
        new_path = {}

        for curr_tag in tags:
            if curr_tag == "qf":  
                continue

            (prob, best_prev_tag) = max(
                (V[t-1][prev_tag] + model.get_tag_likelihood(curr_tag, prev_tag, observation, t), prev_tag)
                for prev_tag in tags if prev_tag in V[t-1]
            )

            V[t][curr_tag] = prob
            new_path[curr_tag] = path[best_prev_tag] + [curr_tag]

        path = new_path  
    
    (prob, best_last_tag) = max((V[-1][tag], tag) for tag in V[-1])

    return path[best_last_tag] 
=======
  # Run Viterbi for t > 0
  for t in range(1, len(observation)):
    V.append({})
    new_path = {}

    for curr_tag in tags:
      if curr_tag == "qf":
        continue

      (prob, best_prev_tag) = max(
        (V[t-1][prev_tag] + model.get_tag_likelihood(curr_tag, prev_tag, observation, t), prev_tag)
        for prev_tag in tags if prev_tag in V[t-1]
      )

      V[t][curr_tag] = prob
      new_path[curr_tag] = path[best_prev_tag] + [curr_tag]

    path = new_path 

  # Find the best final state
  (prob, best_last_tag) = max((V[-1][tag], tag) for tag in V[-1])

  return path[best_last_tag]
>>>>>>> 35a9c1594498c1112515ed20c9c59f3926eeaa17
