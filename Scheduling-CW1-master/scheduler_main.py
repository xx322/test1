import os
import shutil
import json
import networkx as nx

from datetime import datetime

import schedulers
from src.parser import opts
from src.workflow import Workflow

from dags_reversed import due_dates, edge_sets



function_types = [fn for fn in os.listdir('./functions/') if '.' not in fn]

def get_only_node_names(graph):
    return [n.split('_')[0] for n in graph.nodes()]

def form_dag(edge_set):
    graph = nx.DiGraph()
    graph.add_edges_from(edge_set)
    assert nx.is_directed_acyclic_graph(graph)  # Check DAG
    assert not set(get_only_node_names(graph)) - set(function_types)  # Check no exta nodes
    return graph

def form_all_workflows():
    shutil.rmtree('dags', ignore_errors=True)
    shutil.rmtree('temp', ignore_errors=True)
    workflows = []
    dictionary = {}
    for i, edge_set in enumerate(edge_sets):
        graph = form_dag(edge_set)
        workflows.append(Workflow(f'workflow_{i}', graph))
        d = {'edge_set': edge_set, 'due_dates': due_dates[i]}
        dictionary[f'workflow_{i}'] = d
    with open("input.json", "w") as outfile:
        json.dump(dictionary, outfile, indent=4)
    return workflows, dictionary


if __name__ == "__main__":
    start_time = datetime.now()
    shutil.rmtree('temp', ignore_errors=True)
    if opts.scheduler in ['bnb_scheduler', 'hu_scheduler']:
        workflows, dictionary = form_all_workflows()
        scheduler = getattr(schedulers, opts.scheduler)
        schedules = {workflow.name: scheduler(workflow, dictionary) for workflow in workflows}
        with open(f"{opts.scheduler}.json", "w") as outfile:
            json.dump(schedules, outfile, indent=4)
    print("Scheduler runtime: ", datetime.now() - start_time)
