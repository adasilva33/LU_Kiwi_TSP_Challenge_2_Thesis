from MCTS import MCTS
from Node import Node
from Data_Preprocessing import data_preprocessing

instance_number = 2
instance_path = f"/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Flight connections dataset/{instance_number}.in"

expansion_policies = ["top_k", "ratio_k"]
simulation_policies = [
    "heuristic_policy",
    "random_policy",
    "tolerance_heuristic_policy",
]

mcts = MCTS(
    instance=instance_path,
    number_childrens=10,
    desired_expansion_policy="ratio_k",
    ratio_expansion=0.4,
    desired_simulation_policy="heuristic_policy",
    number_simulation=3,
    desired_selection_policy="UCB",
    cp=1,
)
