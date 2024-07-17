import numpy as np
import random
from copy import deepcopy
#random.seed(12)

class data_preprocessing:
    def __init__(self,instance_path):
        self.instance_path=instance_path
        
        self.info, self.flights = self.read_file(f_name=self.instance_path)
        self.number_of_areas,self.starting_airport=int(self.info[0][0]),self.info[0][1]
        
        
        self.flights_by_day_dict = self.flights_by_day(flight_list=self.flights)
        
        self.flights_by_day_dict=self.remove_duplicate(flights_by_day=self.flights_by_day_dict)
        
        self.list_days= [k for k in range(1,self.number_of_areas)]
        
        self.airports_by_area = self.get_airports_by_areas()
        self.area_to_explore=self.which_area_to_explore(airports_by_area=self.airports_by_area)
        self.area_by_airport=self.invert_dict(original_dict=self.airports_by_area)
        
        self.starting_area=self.associated_area_to_airport(airport=self.starting_airport)
        self.list_airports=self.get_list_of_airports()
        self.list_areas=list(self.airports_by_area.keys())
        self.areas_connections_by_day=self.possible_flights_from_zone_to_zone_specific_day()
        
    def read_file(self,f_name):
        dist = []
        line_nu = -1
        with open(f_name) as infile:
            for line in infile:
                line_nu += 1
                if line_nu == 0:
                    index = int(line.split()[0]) * 2 + 1
                if line_nu >= index:
                    temp = line.split()
                    temp[2] = int(temp[2])
                    temp[3] = int(temp[3])
                    dist.append(temp)
                else:
                    dist.append(line.split())
            info = dist[:int(dist[0][0])*2+1]
            flights = dist[int(dist[0][0])*2+1:]
        return info, flights
    
    def flights_by_day(self,flight_list):
        # Create an empty dictionary to hold flights organized by day
        flights_by_day = {}

        # Iterate over each flight in the input list
        for flight in flight_list:
            # Extract the day from the flight entry
            day = flight[2]

            # Create a flight entry without the day
            flight_without_day = flight[:2] + flight[3:]

            # Add the flight to the corresponding day in the dictionary
            if day not in flights_by_day:
                flights_by_day[day] = []
            flights_by_day[day].append(flight_without_day)
            
        return flights_by_day
    
    def flights_from_airport(self,flights_by_day, from_airport, considered_day):
        flights_from_airport = []
        for day, flights in flights_by_day.items():
            if day==considered_day:
                for flight in flights:
                    if flight[0] == from_airport:
                        flights_from_airport.append(flight)
                return flights_from_airport
            else:
                return None

    def invert_dict(self,original_dict):
        inverted_dict = {}
        for key, value_list in original_dict.items():
            for value in value_list:
                if value in inverted_dict:
                    inverted_dict[value].append(key)
                else:
                    inverted_dict[value] = key
        return inverted_dict

    def get_cost(self, day, from_airport, to_airport):
        # Retrieve flights for the specified day and day 0
        flights_day = self.flights_by_day_dict.get(day, [])
        flights_day_0 = self.flights_by_day_dict.get(0, [])
        
        # Find the cost for the specified day
        cost_day = next(
            (flight[2]
            for flight in flights_day
            if flight[0] == from_airport and flight[1] == to_airport),
            float('inf')
        )
        
        # Find the cost for day 0
        cost_day_0 = next(
            (flight[2]
            for flight in flights_day_0
            if flight[0] == from_airport and flight[1] == to_airport),
            float('inf')
        )
        
        # Return the minimum cost if either exists, otherwise inf
        if cost_day == float('inf') and cost_day_0 == float('inf'):
            return float('inf')
        
        return min(cost_day, cost_day_0)

    def possible_flights_from_zone_to_zone_specific_day(self):
        areas_connections_by_day = {}

        for day, flights in self.flights_by_day_dict.items():
            areas_connections_list = []

            for flight in flights:
                connection = f"{self.area_by_airport.get(flight[0])} to {self.area_by_airport.get(flight[1])}"
                if connection not in areas_connections_list:
                    areas_connections_list.append(connection)

            areas_connections_by_day[day] = areas_connections_list

        return areas_connections_by_day

    def get_airports_by_areas(self):
        area_num = int(self.info[0][0])
        return {f"{i}": self.info[2+i * 2] for i in range(0, area_num)}
    
    def get_list_of_airports(self):
        unique_airports = set()

        # Iterate through each sublist and add elements to the set
        for sublist in self.airports_by_area.values():
            for airport in sublist:
                unique_airports.add(airport)
        
        return list(unique_airports)
                    
    def associated_area_to_airport(self,airport):
        return next(
            (
                area
                for area, airports in self.airports_by_area.items()
                if airport in airports
            ),
            "Airport not found",
        ) 
    
    def remove_duplicate(self,flights_by_day):
        for day, flights in flights_by_day.items():
            unique_flights = {}
            for flight in flights:
                flight_key = (flight[0], flight[1])
                if flight_key not in unique_flights:
                    unique_flights[flight_key] = flight
                else:
                    if flight[2] < unique_flights[flight_key][2]:
                        #print(flight[2],unique_flights[flight_key][2])
                        unique_flights[flight_key] = flight
                flights_by_day[day] = list(unique_flights.values())
        return flights_by_day
    
    def possible_flights_from_an_airport_at_a_specific_day(self,day,from_airport):
        daily_flights = self.flights_by_day_dict.get(day, [])
        
        flights_from_airport = []
        for flight in daily_flights:
            if flight[0] == from_airport:
                
                flights_from_airport.append([flight[1], flight[2]])

        return flights_from_airport
    
    def possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(self,day,from_airport, visited_areas):
        daily_flights = self.flights_by_day_dict.get(day, [])
        
        flights_from_airport = []
        for flight in daily_flights:
            #print(self.associated_area_to_airport(airport=flight[0]))
            if (flight[0] == from_airport) and (self.associated_area_to_airport(airport=flight[1]) not in visited_areas):
                
                flights_from_airport.append([flight[1], flight[2]])

        return flights_from_airport
    
    def which_area_to_explore(self,airports_by_area):
        return list({key: len(value) for key, value in airports_by_area.items() if len(value) > 1})
    
class Node:
    def __init__(self, state, parent=None):
        self.state = state  # State is a dictionary representing the current situation
        self.parent = parent  # Parent node
        self.children = []  # List of child nodes
        self.visit_count = 0  # Number of times this node has been visited
        self.total_cost = 0  # Total cost accumulated in simulations from this node

    def add_child(self, child_state):
        child_node = Node(child_state, self)
        self.children.append(child_node)
        return child_node

    def is_fully_expanded(self):
        if self.parent is None:
            return False
        return len(self.children) > 0 and all(child.visit_count > 0 for child in self.children)
    
    def best_child(self, c_param=1.41):
        epsilon = 1e-6

        visited_children = [child for child in self.children if (child.visit_count > 0)]
        unvisited_children = [child for child in self.children if child.visit_count == 0]

        sorted_children = sorted(visited_children, key=lambda child: child.total_cost / (child.visit_count + epsilon))
        scores = {child: rank + 1 for rank, child in enumerate(sorted_children)}
        total_scores = sum(scores.values())

        def normalized_score(child):
            return scores[child] / total_scores

        choices_weights = [
            normalized_score(child) + c_param * ( np.log(self.visit_count + 1) / (child.visit_count + epsilon)) ** 0.5
            for child in visited_children
        ]

        print(f"UCT score {choices_weights}")
        best_child_node = self.children[np.argmin(choices_weights)]
        print(f"Selected Node: {best_child_node.state}, , Visit Count: {best_child_node.visit_count}, Total Cost: {best_child_node.total_cost}")  # Log the selected node
        print("Children picked on UCT critera")
        return best_child_node
    
    def update(self, result):
        self.visit_count += 1
        self.total_cost += result
        
class MCTS(data_preprocessing):
    def __init__(self, instance, iterations):
        super().__init__(instance_path=instance)
        self.root=Node(self.initialise_root_node())
        self.iterations = iterations
        self.best_leaf = None
        self.best_leaf_cost = float('inf')
        self.search()
        

    def initialise_root_node(self):
        return {
        'current_day': 1,
        'current_airport': self.starting_airport,
        'remaining_zones': [x for x in self.list_areas if x != self.starting_area],  # Exclude the starting area
        'visited_zones': [self.starting_area],  # Exclude the starting area
        'total_cost': 0,
        'path': [self.starting_airport]
        }
                
    def expand_node(self, node):
        actions = self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
            node.state['current_day'], node.state['current_airport'], node.state['visited_zones'])

        print('\nExpansion \n')
        for action in actions:
            new_state = self.transition_function(node.state, action)
            child_node = node.add_child(new_state)
            print(f"Children: {child_node.state}, Visit count: {child_node.visit_count}, Total cost: {child_node.total_cost}")
        print('\nEnd Expansion \n')
        
    def transition_function(self, state, action):
        new_state = deepcopy(state)
        new_state['current_day'] += 1
        new_state['current_airport'] = action[0]
        new_state['total_cost'] += action[1]
        new_state['path'].append(action[0])
        new_state['remaining_zones'].remove(self.associated_area_to_airport(airport=new_state['current_airport']))
        new_state['visited_zones'].append(self.associated_area_to_airport(airport=action[0]))
        return new_state

    def random_policy(self, state):
        actions = self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
            day=state['current_day'], from_airport=state['current_airport'], visited_areas=state['visited_zones']
        )
        if not actions:
            return None
        return random.choice(actions)
    
    def heuristic_policy(self, state):
        actions = self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
            day=state['current_day'], from_airport=state['current_airport'], visited_areas=state['visited_zones']
        )
        if not actions:
            return None
        # Select the action with the lowest cost
        best_action = min(actions, key=lambda x: x[1])
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
                return random.choice(unvisited_children)
            print('\nNo more unvisited children')
            node = node.best_child()
        return node

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
        current_simulation_state = deepcopy(node.state)
        print(f"Selected node for simulation {current_simulation_state}")
        while current_simulation_state['current_day'] != self.number_of_areas:
        #while current_simulation_state['current_day'] <= self.number_of_areas and current_simulation_state['remaining_zones']:
            #action = self.random_policy(current_simulation_state)
            action = self.heuristic_policy(state=current_simulation_state)
            if action is None:  # No valid actions available
                break
            current_simulation_state = self.transition_function(current_simulation_state, action)
        
        flights_to_go_back_initial_zone = self.possible_flights_from_an_airport_at_a_specific_day_with_previous_areas(
            day=current_simulation_state['current_day'], from_airport=current_simulation_state['current_airport'], 
            visited_areas=current_simulation_state['visited_zones'][1:])
        
        min_price = 1000000
        final_airport = None
        
        for flight in flights_to_go_back_initial_zone:
            if flight[1] < min_price:
                min_price = flight[1]
                final_airport = flight[0]

        #print(f"{min_price}, {final_airport}")
        current_simulation_state['total_cost'] += min_price

        if current_simulation_state['total_cost'] < self.best_leaf_cost:
            self.best_leaf = current_simulation_state
            self.best_leaf_cost = current_simulation_state['total_cost']
        
        #print(f"Simulation result: {current_simulation_state}")
        return current_simulation_state['total_cost']

    def backpropagate(self, node, cost):
        while node is not None:
            node.update(cost)
            print(f"Backpropagating Node: {node.state}, Visit Count: {node.visit_count}, Total Cost: {node.total_cost}")

            node = node.parent

    def expand_and_select(self, node):
        if not node.is_fully_expanded():
            self.expand_node(node)
        unvisited_children = self.get_unvisited_children(node)
        if unvisited_children:
            return random.choice(unvisited_children)
        return node.best_child()
        
    def search(self):
        for _ in range(self.iterations):
            node_to_explore = self.select(self.root)
            if node_to_explore.is_fully_expanded():
                node_to_explore = self.expand_and_select(node_to_explore)
            cost = self.simulate(node_to_explore)
            self.backpropagate(node_to_explore, cost)
        
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
            print(f"State: {node.state}, Visit Count: {node.visit_count}, Total Cost: {node.total_cost}")

instance_path = 'Code/Flight connections dataset/1.in'
data_processor = data_preprocessing(instance_path=instance_path)

mcts = MCTS(instance=instance_path, iterations=100)

print('\n')
mcts.display_all_nodes(nodes=mcts.collect_all_nodes())

