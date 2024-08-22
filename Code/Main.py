from MCTS import MCTS
from Node import Node
from Data_Preprocessing import data_preprocessing

instance_number = 1
instance_path = f"/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Flight connections dataset/{instance_number}.in"

expansion_policies = ["top_k", "ratio_k"]
simulation_policies = [
    "greedy_policy",
    "random_policy",
    "tolerance_policy",
]

selection_policy = ["UCB", "UCB1T", "SP", "Bayesian"]

mcts = MCTS(
    instance=instance_path,
    number_childrens=10,
    desired_expansion_policy="ratio_k",
    ratio_expansion=0.5,
    desired_simulation_policy="greedy_policy",
    number_simulation=10,
    desired_selection_policy="UCB",
    cp=1.41,
)

import Clean
