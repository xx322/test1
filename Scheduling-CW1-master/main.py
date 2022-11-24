import shutil
import time
import json

import numpy as np
from datetime import datetime

import schedulers
from src.parser import opts
from src.utils import form_all_workflows, HEADER, ENDC


def execute(workflows, schedules, dictionary, ip):
    response_times, tardiness_times, lateness_times = [], [], []
    for i, workflow in enumerate(workflows):
        start = time.time()
        for job in schedules[workflow.name]:
            assert job in workflow.get_possible_nodes(), "Infeasible scheduling"
            st = time.time()
            workflow.execute(job, ip)
            ct = workflow.executed[job] - start
            print(job, 'P', workflow.executed[job] - st, 'T', max(0, ct - dictionary[workflow.name]['due_dates'][job]))
        assert workflow.check_complete()
        response_times.append(time.time() - start)
        tardiness_values = []
        lateness_values = []
        for node in workflow.executed.keys():
            due_date = dictionary[workflow.name]['due_dates'][node]
            completion_time = workflow.executed[node] - start
            tardiness_values.append(max(0, completion_time - due_date))
            lateness_values.append(completion_time - due_date)
        tardiness_times.append(np.sum(tardiness_values))
        lateness_times.append(np.sum(lateness_values))
    return response_times, tardiness_times, lateness_times


if __name__ == "__main__":
    start_time = datetime.now()
    shutil.rmtree('temp', ignore_errors=True)
    ip = opts.ip
    is_job_list = opts.joblist
    rts, tds, lts = [], [], []
    if opts.scheduler in ['random_scheduler', 'simple_scheduler']:
        workflows, dictionary = form_all_workflows(is_job_list)
        scheduler = getattr(schedulers, opts.scheduler)
        schedules = {workflow.name: scheduler(workflow, dictionary) for workflow in workflows}
        with open(f"{opts.scheduler}.json", "w") as outfile:
            json.dump(schedules, outfile, indent=4)
    else:
        with open(f"{opts.scheduler}.json", "r") as outfile:
            schedules = json.load(outfile)
    for i in range(int(opts.runs)):
        print(HEADER + f'Run {i + 1}' + ENDC)
        workflows, dictionary = form_all_workflows(is_job_list)
        rt, td, lt = execute(workflows, schedules, dictionary, ip)
        rts.append(rt)
        tds.append(td)
        lts.append(lt)
    rts, tds, lts = np.array(rts), np.array(tds), np.array(lts)
    means, stds = np.mean(rts, axis=0), np.std(rts, axis=0)
    t_means, t_stds = np.mean(tds, axis=0), np.std(tds, axis=0)
    l_means, l_std = np.mean(lts, axis=0), np.std(lts, axis=0)
    for i in range(len(workflows)):
        avg, std = "{:.4f}".format(means[i]), "{:.4f}".format(stds[i])
        print(f'Completion Time of Workflow {i + 1}:\t{avg} ' + u"\u00B1" + f' {std} s')
        avg, std = "{:.4f}".format(t_means[i]), "{:.4f}".format(t_stds[i])
        print(f'Tardiness of Workflow {i + 1}:\t{avg} ' + u"\u00B1" + f' {std} s')
    print("Script finish time: ", datetime.now() - start_time)
# avg, std = "{:.4f}".format(l_means[i]), "{:.4f}".format(l_std[i])
# print(f'Lateness of Workflow {i+1}:\t{avg} ' + u"\u00B1" + f' {std} s')
