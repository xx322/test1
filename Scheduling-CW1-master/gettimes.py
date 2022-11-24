import os
import json
import shutil
import time

import numpy as np

import schedulers
from src.parser import opts
from src.utils import form_all_workflows, HEADER, ENDC


def execute(workflows, schedules, dictionary, ip, ptimes):
    for i, workflow in enumerate(workflows):
        for job in schedules[workflow.name]:
            assert job in workflow.get_possible_nodes()
            st = time.time()
            workflow.execute(job, ip)
            ptimes[job.split('_')[0]].append(workflow.executed[job] - st)
        assert workflow.check_complete()


if __name__ == "__main__":
    shutil.rmtree('temp', ignore_errors=True)
    ip = 'localhost'
    apps = [fn for fn in os.listdir('./functions/') if '.' not in fn]
    p_times = dict(zip(apps, [[] for _ in range(len(apps))]))
    with open(f"{opts.scheduler}.json", "r") as outfile:
        schedules = json.load(outfile)
    for i in range(int(opts.runs)):
        print(HEADER + f'Run {i + 1}' + ENDC)
        workflows, dictionary = form_all_workflows(True)
        execute(workflows, schedules, dictionary, ip, p_times)
    for i in p_times:
        avg, std = "{:.4f}".format(np.mean(p_times[i])), "{:.4f}".format(np.std(p_times[i]))
        print(f'Processing Time of {i} :\t{avg} ' + u"\u00B1" + f' {std} s')
