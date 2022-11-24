import numpy as np
import random

from copy import deepcopy

random.seed(5)


def random_scheduler(workflow, dictionary):
    schedule = []
    while not workflow.check_complete():
        possible_nodes = workflow.get_possible_nodes()
        selected = random.choice(possible_nodes)
        workflow.remaining_graph.remove_node(selected)
        schedule.append(selected)
    return schedule


def simple_scheduler(workflow, dictionary):
    schedule = []
    while not workflow.check_complete():
        possible_nodes = workflow.get_possible_nodes()
        due_dates = [dictionary[workflow.name]['due_dates'][node] for node in possible_nodes]
        selected = possible_nodes[np.argmin(due_dates)]
        workflow.remaining_graph.remove_node(selected)
        schedule.append(selected)
    return schedule


i_max = 9000

p = {
    'vii': 18.8516,
    'blur': 5.5883,
    'night': 22.7332,
    'onnx': 3.3044,
    'emboss': 1.7246,
    'muse': 15.2032,
    'wave': 10.8110
}

Cmax = 227.25400000000005

due_dates = {
    'onnx_1': 172, 'muse_1': 82, 'emboss_1': 18, 'emboss_2': 61, 'blur_1': 93, 'emboss_3': 71,
    'vii_1': 217, 'blur_2': 295, 'wave_1': 290, 'blur_3': 287, 'blur_4': 253, 'emboss_4': 307,
    'onnx_2': 279, 'onnx_3': 73, 'blur_5': 355, 'wave_2': 34, 'wave_3': 233, 'wave_4': 77,
    'emboss_5': 88, 'onnx_4': 122, 'emboss_6': 71, 'onnx_5': 181, 'vii_2': 340, 'blur_6': 141,
    'night_1': 209, 'muse_2': 217, 'emboss_7': 256, 'onnx_6': 144, 'wave_5': 307, 'emboss_8': 329, 'muse_3': 269
}

jobs_idx = list(due_dates.keys())


class Node:
    node_count = 0  # Used to keep track of number of nodes created.

    def __init__(self, schedule, remainder):  # Each node has an associated partial schedule and remaining workflow.
        Node.node_count += 1
        self.schedule = schedule
        self.remainder = remainder
        self.children = []
        self.explored = False

        self.lower_bound = 0.0  # Calculate tardiness of partial schedule.
        time = Cmax
        for job in self.schedule:
            self.lower_bound += max(0, time - due_dates[job])
            time -= p[job.split('_')[0]]

    def calc_lower_bound(self):  # Get best estimate of lower bound of this schedule.
        if (self.children == []): return self.lower_bound  # Use own partial schedule if child nodes are unexplored.

        return min([node.calc_lower_bound() for node in self.children])  # Get lower bound of child nodes if explored.

    def calc_depth(self):  # Get length of longest schedule from self or child nodes.
        if (self.children == []): return len(self.schedule)

        return max([node.calc_depth() for node in self.children])

    def calc_cost(self):  # Get the lower bound of tardiness/length.
        if (self.children == []): return (self.lower_bound / len(self.schedule))

        return min([node.calc_cost() for node in self.children])

    def explore_children(self):  # Create child nodes.
        self.explored = True
        possible_nodes = self.remainder.get_possible_nodes()

        for node in possible_nodes:
            new_remainder = deepcopy(self.remainder)
            new_remainder.remaining_graph.remove_node(node)
            self.children.append(Node(self.schedule + [node], new_remainder))

        self.remainder = None


###############################################################
# These schedulers need to be run by scheduler_main.py.       #
# Use: python scheduler_main.py --scheduler <scheduler_name>  #
###############################################################


def bnb_scheduler(workflow, dictionary):
    root = Node([], deepcopy(workflow))  # Create root node with empty schedule and full workflow.
    current = root

    for i in range(i_max):
        if (current.remainder.check_complete()): break  # Finish if best node has a complete schedule.

        current.explore_children()  # Generate child nodes of best node.

        # if((i < 3) or (i > 8997)): print([jobs_idx.index(j)+1 for j in current.schedule], current.lower_bound, i)
        print(current.schedule, current.lower_bound, i)
        # if(i == 28): print(current.schedule, current.calc_lower_bound(), current.lower_bound, i)

        current = root  # Find node with smallest lower bound, starting from root.
        best = root

        while (current.children != []):
            best_bound = float("inf")
            for node in current.children:
                node_bound = node.calc_lower_bound()
                if (node_bound <= best_bound):
                    best = node
                    best_bound = node_bound
            current = best

    current = root  # Find best partial schedule.
    best = root

    while (current.children != []):
        best_bound = float("inf")
        best_length = 0
        best_cost = float("inf")
        for node in current.children:
            node_bound = node.calc_lower_bound()
            node_length = node.calc_depth()
            node_score = node.calc_cost()

            if (node_bound < best_bound):  # Compare quality of partial schedules.
                best = node
                best_bound = node_bound
                best_length = node_length
                best_score = node_score

            elif (node_bound == best_bound):
                if (node_length > best_length):  # Break ties.
                    best = node
                    best_bound = node_bound
                    best_length = node_length
                    best_score = node_score

        current = best

    schedule = best.schedule
    workflow = best.remainder
    print()
    print("L. Bound: ", best.calc_lower_bound())
    print("Partial schedule: ", schedule)

    while not workflow.check_complete():  # Perform EDD on remaining jobs.
        possible_nodes = workflow.get_possible_nodes()
        possible_due_dates = [due_dates[node] for node in possible_nodes]
        selected = possible_nodes[np.argmin(possible_due_dates)]
        workflow.remaining_graph.remove_node(selected)
        schedule.append(selected)

    schedule.reverse()
    print("EDD completed schedule: ", schedule)
    print("Node count: ", Node.node_count)
    return schedule


def hu_scheduler(workflow, dictionary):  # Schedule jobs based on distance from exit node.
    schedule = []
    while not workflow.check_complete():
        possible_nodes = workflow.get_possible_nodes()
        print(possible_nodes)

        while possible_nodes != []:

            lowest_idx = float("inf")
            for node in possible_nodes:
                lowest_idx = min(lowest_idx, jobs_idx.index(node))

            selected = jobs_idx[lowest_idx]
            workflow.remaining_graph.remove_node(selected)
            possible_nodes.remove(selected)
            schedule.append(selected)

    schedule.reverse()
    print(schedule)
    return schedule