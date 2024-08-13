import numpy as np
import random
from copy import deepcopy
import logging
import time
import os
import shutil
import glob

from Data_Preprocessing import data_preprocessing
from Node import Node


class MCTS(data_preprocessing):
    def __init__(
        self,
        instance,
        number_childrens,
        desired_expansion_policy,
        ratio_expansion,
        desired_simulation_policy,
        desired_selection_policy,
        cp,
        number_simulation,
    ):
        self.number_childrens = number_childrens
        self.desired_simulation_policy = desired_simulation_policy
        self.desired_expansion_policy = desired_expansion_policy
        self.ratio_expansion = ratio_expansion
        self.number_simulation = number_simulation
        self.desired_selection_policy = desired_selection_policy
        self.cp = cp

        self.start_time = time.time()
        super().__init__(instance_path=instance)
        self.end_time_data_preprocessing = time.time() - self.start_time
        self.logger = self.configure_logging()
        self.root = Node(
            self.initialise_root_node(),
            desired_selection_policy=self.desired_selection_policy,
            cp=self.cp,
        )
        self.best_leaf = None
        self.best_leaf_cost = float("inf")
        self.search()
        self.end_search_time = time.time() - self.start_time
        self.print_execution_times()
        # self.simulation()

    def configure_logging(self):
        log_file = f"{self.instance_path}_{self.number_childrens}_{self.desired_simulation_policy}.log"
        log_file = self.get_unique_log_file(log_file)

        # Configure the logger
        logging.basicConfig(
            level=logging.DEBUG,  # Set the log level to DEBUG to capture all types of logs
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(
                    log_file, mode="w"
                ),  # 'w' to overwrite the log file each run, 'a' to append
                logging.StreamHandler(),  # Optional: to also print logs to the console
            ],
        )
        logger = logging.getLogger(__name__)
        return logger

    def get_unique_log_file(self, base_log_file):
        """
        Check if the log file exists and if so, create a new file with a unique suffix.
        """
        if not os.path.exists(base_log_file):
            return base_log_file

        base_name, extension = os.path.splitext(base_log_file)
        counter = 1
        while True:
            new_log_file = f"{base_name}_{counter}{extension}"
            if not os.path.exists(new_log_file):
                return new_log_file
            counter += 1

    def initialise_root_node(self):
        return {
            "current_day": 1,
            "current_airport": self.starting_airport,
            "remaining_zones": [
                x for x in self.list_areas if x != self.starting_area
            ],  # Exclude the starting area
            "visited_zones": [self.starting_area],  # Exclude the starting area
            "total_cost": 0,
            "path": [self.starting_airport],
        }

    def expand_node(self, node):
        actions = (
            self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
                node.state["current_day"],
                node.state["current_airport"],
                node.state["visited_zones"],
            )
        )

        expansion_policy = self.get_expansion_policy()
        actions = expansion_policy(actions=actions)

        self.logger.debug(actions)
        self.logger.debug("\nExpansion")
        # for action in actions:
        for action in actions:
            new_state = self.transition_function(node.state, action)
            child_node = node.add_child(new_state)
            self.logger.info(
                f"Children: {child_node.state}, Visit count: {child_node.visit_count}, Total cost: {child_node.total_cost}"
            )
        self.logger.debug("\nEnd expansion")

    def transition_function(self, state, action):
        new_state = deepcopy(state)
        new_state["current_day"] += 1
        new_state["current_airport"] = action[0]
        new_state["total_cost"] += action[1]
        new_state["path"].append(action[0])
        new_state["remaining_zones"].remove(
            self.associated_area_to_airport(airport=new_state["current_airport"])
        )
        new_state["visited_zones"].append(
            self.associated_area_to_airport(airport=action[0])
        )
        return new_state

    def random_policy(self, state):
        actions = (
            self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
                day=state["current_day"],
                from_airport=state["current_airport"],
                visited_areas=state["visited_zones"],
            )
        )
        if not actions:
            return None
        return random.choice(actions)

    def heuristic_policy(self, state):
        actions = (
            self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
                day=state["current_day"],
                from_airport=state["current_airport"],
                visited_areas=state["visited_zones"],
            )
        )
        self.logger.info(f"Actions: {actions}")
        if not actions:
            return None
        # Select the action with the lowest cost
        best_action = min(actions, key=lambda x: x[1])
        self.logger.info(f"Chosen action based on heuristic policy: {best_action}")
        return best_action

    def tolerance_heuristic_policy(self, state):
        actions = (
            self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
                day=state["current_day"],
                from_airport=state["current_airport"],
                visited_areas=state["visited_zones"],
            )
        )
        self.logger.info(f"Actions: {actions}")

        if not actions:
            return None

        # Find the minimum cost
        min_cost = min(actions, key=lambda x: x[1])[1]

        # Define the tolerance level (30%)
        tolerance = 0.3 * min_cost

        # Filter actions within the tolerance level
        best_actions = [
            action for action in actions if action[1] <= min_cost + tolerance
        ]

        # Select a random action from the best actions
        best_action = random.choice(best_actions)

        self.logger.info(f"Chosen action based on heuristic policy: {best_action}")

        return best_action

    def select(self, node):
        while True:
            if not node.children:
                self.expand_node(node)

                if not node.children:  # No more children can be expanded
                    return node
                return random.choice(node.children)

            unvisited_children = self.get_unvisited_children(node)
            if unvisited_children:
                self.logger.info(f"Unvisited children picked randomly")
                return random.choice(unvisited_children)

            node = node.best_child()
            self.logger.info(
                f"Best node has been chosen on {self.desired_selection_policy}: {node.state}"
            )

    def get_unvisited_children(self, node):
        queue = [node]
        unvisited_children = []
        while queue:
            current_node = queue.pop(0)
            for child in current_node.children:
                if child.visit_count == 0:
                    unvisited_children.append(child)
                else:
                    queue.append(child)

        return unvisited_children

    def simulate(self, node):
        simulation_policy = self.get_simulation_policy()
        current_simulation_state = deepcopy(node.state)
        self.logger.info(f"Selected node for simulation {current_simulation_state}")
        while current_simulation_state["current_day"] != self.number_of_areas:
            action = simulation_policy(state=current_simulation_state)

            if action is None:  # No valid actions available
                break

            current_simulation_state = self.transition_function(
                current_simulation_state, action
            )
            self.logger.info(f"Current simulation state {current_simulation_state}")

        if current_simulation_state["current_day"] < self.number_of_areas:
            self.logger.info("Final state not reached")
            return 100000

        flights_to_go_back_initial_zone = (
            self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
                day=current_simulation_state["current_day"],
                from_airport=current_simulation_state["current_airport"],
                visited_areas=current_simulation_state["visited_zones"][1:],
            )
        )

        min_price = 1000000
        final_airport = None

        for flight in flights_to_go_back_initial_zone:
            if flight[1] < min_price:
                min_price = flight[1]
                final_airport = flight[0]

        if not final_airport:
            return min_price

        self.logger.info(f"Last flight to {final_airport} at the cost: {min_price}")
        current_simulation_state["total_cost"] += min_price

        if current_simulation_state["total_cost"] < self.best_leaf_cost:
            self.best_leaf = current_simulation_state
            self.best_leaf_cost = current_simulation_state["total_cost"]

        return current_simulation_state["total_cost"]

    def backpropagate(self, node, cost):
        while node is not None:

            node.update(cost)

            self.logger.info(
                f"Backpropagating Node: {node.state}, Visit Count: {node.visit_count}, Total Cost: {node.total_cost}"
            )

            node = node.parent

    def expand_and_select(self, node):
        if not node.is_fully_expanded():
            self.expand_node(node)
        unvisited_children = self.get_unvisited_children(node)
        if unvisited_children:
            return random.choice(unvisited_children)
        return node.best_child()

    def search(self):
        while True:
            node_to_explore = self.select(self.root)
            if len(node_to_explore.state["remaining_zones"]) == 0:
                cost = self.simulate(node_to_explore)
                self.backpropagate(node_to_explore, cost)
                if len(self.get_unvisited_children(node_to_explore.parent)) == 0:

                    self.logger.info("Children reached")
                    break

            if node_to_explore.is_fully_expanded():
                node_to_explore = self.expand_and_select(node_to_explore)
            cost = self.simulate(node_to_explore)
            self.backpropagate(node_to_explore, cost)

        self.logger.info(f"Best node: {self.best_leaf}")
        self.logger.info(f"Associated cost: {self.best_leaf_cost}")

    def collect_all_nodes(self):
        nodes = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            nodes.append(node)
            queue.extend(node.children)
        return nodes

    def display_all_nodes(self, nodes):
        for node in nodes:
            print(
                f"State: {node.state}, Visit Count: {node.visit_count}, Total Cost: {node.total_cost}"
            )
            self.logger.info(
                f"State: {node.state}, Visit Count: {node.visit_count}, Total Cost: {node.total_cost}"
            )

    def print_execution_times(self):
        self.logger.info(
            f"\n\n\n Time to preprocess the data: {self.end_time_data_preprocessing:.4f} seconds"
        )
        self.logger.info(
            f"\n\n\n Time to find the solution: {self.end_search_time:.4f} seconds"
        )
        self.logger.info(
            f"\n\n\n Total time: {self.end_time_data_preprocessing+self.end_search_time:.4f} seconds \n\n"
        )

    def get_simulation_policy(self):
        if self.desired_simulation_policy == "heuristic_policy":
            return self.heuristic_policy
        elif self.desired_simulation_policy == "random_policy":
            return self.random_policy
        elif self.desired_simulation_policy == "tolerance_heuristic_policy":
            return self.tolerance_heuristic_policy
        else:
            raise ValueError(
                f"Unknown simulation policy: {self.desired_simulation_policy}"
            )

    def get_expansion_policy(self):
        if self.desired_expansion_policy == "top_k":
            return self.top_k_actions

        if self.desired_expansion_policy == "ratio_k":
            return self.ration_best_random

        else:
            raise ValueError(
                f"Unknown expansion policy: {self.desired_expansion_policy}"
            )

    def top_k_actions(self, actions):
        sorted_actions = sorted(actions, key=lambda x: x[1])
        return sorted_actions[: self.number_childrens]

    def ration_best_random(self, actions):
        # Determine the number of best actions to take based on the ratio
        ratio = self.ratio_expansion
        num_best = int(self.number_childrens * ratio)
        num_random = self.number_childrens - num_best

        # Sort actions to get the best ones
        sorted_actions = sorted(actions, key=lambda x: x[1])
        best_actions = sorted_actions[:num_best]

        # Select the remaining random actions from the remaining pool
        remaining_actions = sorted_actions[num_best:]

        # Ensure we don't try to sample more than available actions
        num_random = min(num_random, len(remaining_actions))

        # If num_random is zero or there are no remaining actions, we skip the sampling
        if num_random > 0 and remaining_actions:
            random_actions = random.sample(remaining_actions, num_random)
        else:
            random_actions = []

        # Combine the best actions and the random actions
        final_actions = best_actions + random_actions
        random.shuffle(final_actions)

        return final_actions

    def simulation(self):
        for _ in range(self.number_simulation):
            self.logger = self.configure_logging()
            self.root = Node(
                self.initialise_root_node(),
                desired_selection_policy=self.desired_selection_policy,
                cp=self.cp,
            )
            self.best_leaf = None
            self.best_leaf_cost = float("inf")
            self.search()
            self.end_search_time = time.time() - self.start_time
            self.print_execution_times()
