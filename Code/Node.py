import numpy as np


class Node:
    def __init__(self, state, desired_selection_policy, cp, parent=None):
        self.cp = cp
        self.desired_selection_policy = desired_selection_policy
        self.state = state  # State is a dictionary representing the current situation
        self.parent = parent  # Parent node
        self.children = []  # List of child nodes
        self.visit_count = 0  # Number of times this node has been visited
        self.total_cost = 0  # Total cost accumulated in simulations from this node

    def add_child(self, child_state):
        child_node = Node(
            state=child_state,
            desired_selection_policy=self.desired_selection_policy,
            cp=self.cp,
            parent=self,
        )
        self.children.append(child_node)
        return child_node

    def is_fully_expanded(self):
        if self.parent is None:
            return False
        return len(self.children) > 0 and all(
            child.visit_count > 0 for child in self.children
        )

    def UCB(self):
        epsilon = 0

        visited_children = [child for child in self.children if (child.visit_count > 0)]
        unvisited_children = [
            child for child in self.children if child.visit_count == 0
        ]

        sorted_children = sorted(
            visited_children,
            key=lambda child: child.total_cost / (child.visit_count + epsilon),
        )
        scores = {child: rank + 1 for rank, child in enumerate(sorted_children)}
        total_scores = sum(scores.values())

        def normalized_score(child):
            return scores[child] / total_scores

        choices_weights = [
            normalized_score(child)
            + self.cp
            * (2 * np.log(self.visit_count) / (child.visit_count + epsilon)) ** 0.5
            for child in visited_children
        ]

        print(f"UCB_{self.cp} score {choices_weights}")
        best_child_node = self.children[np.argmin(choices_weights)]
        print(
            f"Selected Node: {best_child_node.state}, , Visit Count: {best_child_node.visit_count}, Total Cost: {best_child_node.total_cost}"
        )
        print("Children picked on UCT critera")
        return best_child_node

    def update(self, result):
        self.visit_count += 1
        self.total_cost += result

    def best_child(self):
        if self.desired_selection_policy == "UCB":
            return self.UCB()
        else:
            raise ValueError(
                f"Unknown Selection policy: {self.desired_selection_policy}"
            )
