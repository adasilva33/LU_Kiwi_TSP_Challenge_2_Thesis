from MCTS import MCTS
from Logs_process import logs_analysis
import time


def run_mcts(
    instance_number,
    expansion_p,
    simulation_p,
    selection_p,
    children,
    c_p_coeff,
    ratio,
    instances,
    root_dir,
):
    instance_path = f"{instances}/{instance_number}.in"

    mcts = MCTS(
        instance=instance_path,
        instance_number=instance_number,
        number_childrens=children,
        desired_expansion_policy=expansion_p,
        ratio_expansion=ratio,
        desired_simulation_policy=simulation_p,
        number_simulation=10 if simulation_p != "greedy_policy" else 1,
        desired_selection_policy=selection_p,
        cp=c_p_coeff,
    )

    logs_analysis(
        root_dir=instances,
        create_or_not=True,
        do_we_delete=True,
    )


def grid_search(
    expansion_policies,
    simulation_policies,
    selection_policies,
    instance_range,
    c_p,
    N_simulation,
    N_children,
    ratios,
    root_dir,
):
    instances = f"/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/{root_dir}"
    iteration = 0

    total_iterations = (
        len(instance_range)
        * len(N_children)
        * len(expansion_policies)
        * len(ratios)
        * len(simulation_policies)
        * (1 if "greedy_policy" in simulation_policies else len(N_simulation))
        * len(selection_policies)
        * len(c_p)
    )

    start_time = time.time()

    for i in instance_range:
        for expansion_p in expansion_policies:
            for simulation_p in simulation_policies:
                for selection_p in selection_policies:
                    for children in N_children:
                        for c_p_coeff in c_p:
                            for ratio in ratios:
                                iteration += 1
                                percentage_completed = (
                                    iteration / total_iterations
                                ) * 100

                                print(
                                    f"Iteration {iteration} started with {expansion_p}, {simulation_p}, {selection_p}, {children}, {c_p_coeff}, {ratio}."
                                )
                                run_mcts(
                                    i,
                                    expansion_p,
                                    simulation_p,
                                    selection_p,
                                    children,
                                    c_p_coeff,
                                    ratio,
                                    instances,
                                    root_dir,
                                )
                                print(
                                    f"Progress: {percentage_completed:.2f}% completed."
                                )

    # Run with greedy_policy separately to avoid duplication
    if "greedy_policy" in simulation_policies:
        for i in instance_range:
            for expansion_p in expansion_policies:
                for selection_p in selection_policies:
                    for children in N_children:
                        for c_p_coeff in c_p:
                            for ratio in ratios:
                                iteration += 1
                                percentage_completed = (
                                    iteration / total_iterations
                                ) * 100

                                print(
                                    f"Greedy iteration {iteration} started with {expansion_p}, greedy_policy, {selection_p}, {children}, {c_p_coeff}, {ratio}."
                                )
                                run_mcts(
                                    i,
                                    expansion_p,
                                    "greedy_policy",
                                    selection_p,
                                    children,
                                    c_p_coeff,
                                    ratio,
                                    instances,
                                    root_dir,
                                )
                                print(
                                    f"Progress: {percentage_completed:.2f}% completed."
                                )

    elapsed_time = time.time() - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")


# Define the parameters
expansion_policies = ["top_k", "ratio_k"]
simulation_policies = ["random_policy", "greedy_policy"]
selection_policies = ["UCB", "UCB1T"]

instance_range = range(1, 2)
c_p = [0, 1.41, 2 * 1.41]
N_simulation = [10]
N_children = [5, 10, 15]
ratios = [0, 0.3, 0.5, 0.8, 1]

# Run the grid search
grid_search(
    expansion_policies,
    simulation_policies,
    selection_policies,
    instance_range,
    c_p,
    N_simulation,
    N_children,
    ratios,
    "Flight connections dataset",
)
