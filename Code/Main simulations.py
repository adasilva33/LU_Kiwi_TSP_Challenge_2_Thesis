from MCTS import MCTS
from Node import Node

import time


root_dir = "/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Flight connections dataset"

instances = range(1, 2)
number_childrens_options = [10]
desired_expansion_policy_options = ["ratio_k", "top_k"]
ratio_expansion_options = [0, 0.5, 1]
desired_simulation_policy_options = [
    "heuristic_policy",
    "random_policy",
    "tolerance_policy",
]
number_simulation_options = [10]
desired_selection_policy_options = ["UCB", "UCB1T", "SP", "Bayesian"]
cp_options = [0, 1.41, 2]

# Calculate the total number of simulations
total_iterations = (
    len(instances)
    * len(number_childrens_options)
    * len(desired_expansion_policy_options)
    * len(ratio_expansion_options)
    * len(desired_simulation_policy_options)
    * (
        1
        if "heuristic_policy" in desired_simulation_policy_options
        else len(number_simulation_options)
    )
    * len(desired_selection_policy_options)
    * len(cp_options)
)


# Initialize counters and lists for plotting
iteration = 0
percentages = []
times = []
start_time = time.time()


for instance_number in instances:
    for number_childrens in number_childrens_options:
        for desired_expansion_policy in desired_expansion_policy_options:
            for ratio_expansion in ratio_expansion_options:
                for desired_simulation_policy in desired_simulation_policy_options:
                    if desired_simulation_policy == "heuristic_policy":
                        number_simulation_options_current = [1]
                    else:
                        number_simulation_options_current = number_simulation_options

                    for number_simulation in number_simulation_options_current:
                        for (
                            desired_selection_policy
                        ) in desired_selection_policy_options:
                            for cp in cp_options:

                                iteration += 1
                                percentage_completed = (
                                    iteration / total_iterations
                                ) * 100
                                current_time = time.time() - start_time
                                percentages.append(percentage_completed)
                                times.append(current_time)

                                print(f"Iteration {iteration} started.")

                                instance_path = f"{root_dir}/{instance_number}.in"

                                mcts = MCTS(
                                    instance=instance_path,
                                    number_childrens=number_childrens,
                                    desired_expansion_policy=desired_expansion_policy,
                                    ratio_expansion=ratio_expansion,
                                    desired_simulation_policy=desired_simulation_policy,
                                    number_simulation=number_simulation,
                                    desired_selection_policy=desired_selection_policy,
                                    cp=cp,
                                )

                                print(
                                    f"Iteration {iteration}/{total_iterations} ({percentage_completed:.2f}%) completed."
                                )

import Clean
