from MCTS import MCTS
from Node import Node
from Data_Preprocessing import data_preprocessing

from Logs_process import logs_analysis
import time

expansion_policies = ["top_k", "ratio_k"]
simulation_policies = ["tolerance_policy"]
selection_policies = ["UCB", "UCB1T"]


instance = range(2, 3)
c_p = [0, 1.41, 2 * 1.41]
N_simulation = [5]
N_children = [5, 10, 15]
ratios = [0, 0.3, 0.5, 0.8, 1]

# Calculate the total number of iterations
total_iterations = (
    len(instance)
    * len(N_children)
    * len(expansion_policies)
    * len(ratios)
    * len(simulation_policies)
    * (1 if "greedy_policy" in simulation_policies else len(N_simulation))
    * len(selection_policies)
    * len(c_p)
)


iteration = 0
percentages = []
times = []

# Start time tracking
start_time = time.time()


for i in instance:
    for expansion_p in expansion_policies:
        for simulation_p in simulation_policies:
            for selection_p in selection_policies:
                for children in N_children:
                    for c_p_coeff in c_p:
                        for ratio in ratios:

                            instance_number = i
                            root_dir = "Flight connections dataset"
                            instances = f"/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/{root_dir}"
                            instance_path = f"{instances}/{instance_number}.in"

                            if simulation_p == "greedy_policy":
                                simulation = 2
                            else:
                                simulation = 10

                            iteration += 1
                            percentage_completed = (iteration / total_iterations) * 100

                            print(f"Iteration {iteration} started.")

                            mcts = MCTS(
                                instance=instance_path,
                                instance_number=instance_number,
                                number_childrens=children,
                                desired_expansion_policy=expansion_p,
                                ratio_expansion=ratio,
                                desired_simulation_policy=simulation_p,
                                number_simulation=10,
                                desired_selection_policy=selection_p,
                                cp=c_p_coeff,
                            )

                            logs_analysis(
                                root_dir=instances,
                                create_or_not=True,
                                do_we_delete=True,
                            )

                            print(f"Progress: {percentage_completed}% completed.")

for i in instance:
    for expansion_p in expansion_policies:

        for selection_p in selection_policies:
            for children in N_children:
                for c_p_coeff in c_p:
                    for ratio in ratios:

                        instance_number = i
                        root_dir = "Flight connections dataset"
                        instances = f"/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/{root_dir}"
                        instance_path = f"{instances}/{instance_number}.in"

                        iteration += 1
                        percentage_completed = (iteration / total_iterations) * 100

                        print(f"Iteration {iteration} started.")

                        mcts = MCTS(
                            instance=instance_path,
                            instance_number=instance_number,
                            number_childrens=children,
                            desired_expansion_policy=expansion_p,
                            ratio_expansion=ratio,
                            desired_simulation_policy=simulation_p,
                            number_simulation=1,
                            desired_selection_policy=selection_p,
                            cp=c_p_coeff,
                        )

                        logs_analysis(
                            root_dir=instances,
                            create_or_not=True,
                            do_we_delete=True,
                        )

                        print(f"Progress: {percentage_completed}% completed.")
