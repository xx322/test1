import numpy as np
import sys  # 导入sys模块

sys.setrecursionlimit(10000)  # 将默认的递归深度修改为3000

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
k_beam = list()
final_schedule = list()
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


#find edges and calculate tardiness
def schedule(start_node):
    global tardiness, time, queue, node_num,schedule, Tardiness, final_schedule
    connection = list()
    child_num = 0
    for i,j in queue:
        if i == start_node:        # match start
            queue.remove([i, j])
            time = time - p_times[start_node]
            tardiness += max(0, time - due_dates[j])
            Tardiness[j] = tardiness
            Time[j] = time
            connection.append([j, tardiness, time, i])   #the tardiness and time of j
            if i not in final_schedule: final_schedule.append(i)
            if i == end_node: return
            node_num = node_num + 1
            child_num += 1
    if child_num == 1:
        start_node = connection[0][0]
        check_child(child_num,start_node, connection)
    elif child_num > 1:
        check_multi_clild(connection, connection[0][3])

def check_child(child_num,start_node,connection):
    if child_num == 1:
        schedule(start_node)

#traverse all child nodes
#一次传多个
def check_multi_clild(connection, start_node):
    global all_node, time, Tardiness, Time, p_times
    node = list()
    connection_multi = list()
    connection_sort = list()
    best = list()
    for j in range(0,len(connection)):
        j = connection[j][0]
        time = Time[start_node] - p_times[start_node]
        tardiness = Tardiness[start_node] + max(0, time - due_dates[j])
        Tardiness[j] = tardiness
        connection_multi.append([tardiness, time, start_node, j])
    Min = min(connection_multi)
    connection_sort.append(Min)
    if Min[3] not in final_schedule: final_schedule.append(Min[3])
    if Min[3] == end_node: return
    connection_multi.remove(Min)
    second_min = min(connection_multi)
    connection_sort.append(second_min)
    if second_min[3] not in final_schedule: final_schedule.append(second_min[3])
    if Min[3] == end_node: print('end')
    for i in range(0, len(connection_sort)):
        node.append(connection_sort[i])
    check_branch(node)


def check_child_num(child_list):
    #把所有的孩子找到
    global all_node, time, Tardiness, Time, p_times,queue
    global tardiness, time, queue, node_num, schedule, Tardiness, final_schedule
    connection = list()
    connection_sort = list()
    child_num = 0
    for num in range(0, len(child_list)):
        start_node = child_list[num][3]
        tardiness = Tardiness[start_node]
        for i, j in queue:
            if i == start_node:  # match start
                queue.remove([i, j])
                time = Time[start_node] - p_times[start_node]
                tardiness += max(0, time - due_dates[j])
                Tardiness[j] = tardiness
                Time[j] = time
                connection.append([tardiness, time, i, j])  # the tardiness and time of j
    if len(connection) == 0:
        print(final_schedule)
    elif len(connection) == 2:
        Min = min(connection)
        connection_sort.append(Min)
        if Min[3] not in final_schedule: final_schedule.append(Min[3])
        if Min[3] == end_node: return
        connection.remove(Min)
        if len(connection) != 0:
            second_min = min(connection)
            connection_sort.append(second_min)
            if second_min[3] not in final_schedule: final_schedule.append(second_min[3])

    check_branch(connection_sort)


def check_branch(connection):
    global all_node, time, Tardiness, Time, p_times,end_node
    connection_multi = list()
    connection_sort = list()

    for a in range(0, len(connection)):
        start_node = connection[a][3]
        for i, j in queue:
            if i == start_node and i != end_node:  # match start
                queue.remove([i, j])
                time = connection[a][1] - p_times[start_node]
                tardiness = Tardiness[start_node] + max(0, time - due_dates[j])
                Tardiness[j] = tardiness
                Time[j] = time
                connection_multi.append([tardiness, time, start_node, j])
    if len(connection_multi) == 0: print(final_schedule)
    else:
        if len(connection_multi) != 0:
            Min = min(connection_multi)
            connection_sort.append(Min)
            if Min[3] not in final_schedule: final_schedule.append(Min[3])
            if Min[3] == end_node: return
            connection_multi.remove(Min)
            if len(connection_multi) != 0:
                second_min = min(connection_multi)
                connection_sort.append(second_min)
                if second_min[3] not in final_schedule: final_schedule.append(second_min[3])
    check_child_num(connection_sort)


if __name__ == "__main__":
    schedule(start_node)
    print(Tardiness)
    print(final_schedule)