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
	'vii':    18.8516,
	'blur':   5.5883,
	'night':  22.7332,
	'onnx':   3.3044,
	'emboss': 1.7246,
	'muse':   15.2032,
	'wave':   10.8110
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

	node_count = 0

	def __init__(self, schedule, remainder):
		Node.node_count += 1
		self.schedule  = schedule
		self.remainder = remainder
		self.children  = []
		self.explored  = False

		tardiness = 0.0
		time = Cmax
		for job in self.schedule:
			tardiness += max(0, time - due_dates[job])
			time -= p[job.split('_')[0]]
		self.lower_bound = tardiness

	def calc_lower_bound(self):
		if(self.children == []): return self.lower_bound

		tardiness = float("inf")
		for node in self.children:
			tardiness = min(tardiness, node.calc_lower_bound())
		return tardiness

	def explore_children(self):
		self.explored = True
		possible_nodes = self.remainder.get_possible_nodes()

		for node in possible_nodes:
			new_remainder = deepcopy(self.remainder)
			new_remainder.remaining_graph.remove_node(node)
			self.children.append(Node(self.schedule + [node], new_remainder))

		self.remainder = None



def bnb_scheduler(workflow, dictionary):

	root    = Node([], deepcopy(workflow))
	current = root
	best    = root

	for i in range(i_max):
		if(len(best.schedule) == 31): break

		current.explore_children()

		#if((i < 3) or (i > 8997)): print([jobs_idx.index(j)+1 for j in current.schedule], current.lower_bound, i)

		current = root

		best_bound = float("inf")
		while(current.children != []):
			for node in current.children:
				node_bound = node.calc_lower_bound()
				if (node_bound <= best_bound):
					best = node
					best_bound = node_bound

			current = best


	current = root
	low_bound = float("inf")
	best = current
	while(current.children != []):
		for node in current.children:
			if(node.calc_lower_bound() <= low_bound):
				best = node

			low_bound = node.calc_lower_bound()

		current = best


	schedule = best.schedule
	print()
	print("L. Bound: ", best.calc_lower_bound())
	print("Partial schedule: ", schedule[::-1])
	workflow = best.remainder
	while not workflow.check_complete():
		possible_nodes = workflow.get_possible_nodes()
		possible_due_dates = [due_dates[node] for node in possible_nodes]
		selected = possible_nodes[np.argmin(possible_due_dates)]
		workflow.remaining_graph.remove_node(selected)
		schedule.append(selected)

	schedule.reverse()
	print("EDD completed schedule: ", schedule)
	print("Node count: ", Node.node_count)
	return schedule


def hu_scheduler(workflow, dictionary):
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
