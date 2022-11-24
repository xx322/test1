import numpy as np

links = [[0, 30],
             [1, 0],
             [2, 7],
             [3, 2],
             [4, 1],
             [5, 15],
             [10, 4],
             [6, 5],
             [7, 6],
             [8, 7],
             [9, 8],
             [11, 4],
             [12, 11],
             [13, 12],
             [14, 10],
             [15, 14],
             [16, 15],
             [17, 16],
             [18, 17],
             [19, 18],
             [20, 17],
             [21, 20],
             [22, 21],
             [23, 4],
             [24, 23],
             [25, 24],
             [26, 25],
             [28, 27],
             [29, 3],
             [27, 25],
             [29, 9],
             [29, 13],
             [29, 19],
             [29, 22],
             [29, 26],
             [29, 28]]

nodes = ['onnx_1', 'muse_1', 'emboss_1', 'emboss_2', 'blur_1', 'emboss_3', 'vii_1', 'blur_2', 'wave_1', 'blur_3',
         'blur_4', 'emboss_4', 'onnx_2', 'onnx_3', 'blur_5', 'wave_2', 'wave_3', 'wave_4', 'emboss_5', 'onnx_4',
         'emboss_6', 'onnx_5', 'vii_2', 'blur_6', 'night_1', 'muse_2', 'emboss_7', 'onnx_6', 'wave_5', 'emboss_8',
         'muse_3']

due_dates = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34, 233, 77, 88, 122, 71, 181,
             340, 141, 209, 217, 256, 144, 307, 329, 269]

p_times = [4,17,2,2,6,2,21,6,13,6,6,2,4,4,6,13,13,13,2,4,2,4,21,6,25,17,2,4,13,2,17]

# p_time = {
#     'onnx_1': 4, 'muse_1': 17, 'emboss_1': 2, 'emboss_2': 2, 'blur_1': 6, 'emboss_3': 2,
#     'vii_1': 21, 'blur_2': 6, 'wave_1': 13, 'blur_3': 6, 'blur_4': 6, 'emboss_4': 2,
#     'onnx_2': 4, 'onnx_3': 4, 'blur_5': 6, 'wave_2': 13, 'wave_3': 13, 'wave_4': 13,
#     'emboss_5': 2, 'onnx_4': 4, 'emboss_6': 2, 'onnx_5': 4, 'vii_2': 21, 'blur_6': 6,
#     'night_1': 25, 'muse_2': 17, 'emboss_7': 2, 'onnx_6': 4, 'wave_5': 13, 'emboss_8': 2, 'muse_3': 17
# }

Cmax = 259

# reverse
for i in range(len(links)): links[i].reverse()
links.reverse()

start = list()
tardiness = 0.0
Tardiness = dict()
Time = dict()
queue = list()
all_node = list()

# find start node and end node according to links
F = list()
C = list()
for ids in links:
    i, j = ids
    F.append(i)
    C.append(j)

# find start_node and end_node according to difference
start_node = set(F)-set(C)
end_node = set(C) - set(F)
start_node = start_node.pop()
end_node = end_node.pop()


time = Cmax
tardiness += max(0, time - due_dates[start_node])
Tardiness[start_node] = tardiness
Time[start_node] = time

# sum node number
node_num = 1

# queue is used to remove and all_node is used to store all the nodes and connection
for ids in links:
    i, j = ids
    queue.append([i,j])
    all_node.append([i,j])

#traverse all child nodes
def check_multi_clild(child_num,connection):
    node = list()
    for i in range(0, child_num):
        node.append(connection[i])
        schedules(node[i])

#find edges and calculate tardiness
def schedule(start_node):
    global tardiness, time, queue, node_num,schedule, Tardiness
    child_num = 0
    connection = list()
    for i,j in queue:
        if i == start_node:        # match start
            # print('进入匹配')
            # print('j',j)
            # schedule.append([start_node])
            queue.remove([i, j])
            # print('startnode',start_node)
            # print(queue)
            time = time - p_times[start_node]
            tardiness += max(0, time - due_dates[j])
            Tardiness[j] = tardiness
            Time[j] = time
            connection.append([j, tardiness, time, i])   #the tardiness and time of j
            node_num = node_num + 1
            child_num += 1

    if child_num == 1:
        start_node = connection[0][0]
        check_child(child_num,start_node,connection)
    elif child_num != 1:
        check_multi_clild(child_num,connection)

#traverse all child nodes
def schedules(node):
    global Tardiness, Time, node_num
    start_node = node[0]
    tardiness = Tardiness[start_node]
    time = Time[start_node]
    child_num = 0
    connection = list()
    for i, j in queue:
        # print('start', start_node)
        # print('i', i)
        if i == start_node:
            # schedule.append([start_node])
            # print('j',j)
            # print(queue)
            queue.remove([i, j])
            #if exist then remove
            # print(queue)
            # print('startnode',start_node)
            # print(queue)
            time = time - p_times[start_node]
            tardiness += max(0, time - due_dates[j])
            Tardiness[j] = tardiness
            Time[j] = time
            connection.append([j, tardiness, time, i])  # j点的tardiness and time
            node_num = node_num + 1
            child_num += 1

    if child_num == 1:
        start_node = connection[0][0]
        check_child(child_num, start_node, connection)
    elif child_num != 1:
        check_multi_clild(child_num,connection)


def check_child(child_num,start_node,connection):
    if child_num == 1:
        schedule(start_node)

if __name__ == "__main__":
    schedule(start_node)


