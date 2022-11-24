def create_dag():
    nodes = ['onnx_1', 'muse_1', 'emboss_1', 'emboss_2', 'blur_1', 'emboss_3', 'vii_1', 'blur_2', 'wave_1', 'blur_3',
             'blur_4', 'emboss_4', 'onnx_2', 'onnx_3', 'blur_5', 'wave_2', 'wave_3', 'wave_4', 'emboss_5', 'onnx_4',
             'emboss_6', 'onnx_5', 'vii_2', 'blur_6', 'night_1', 'muse_2', 'emboss_7', 'onnx_6', 'wave_5', 'emboss_8',
             'muse_3']
    links = [[0, 30],
             [1, 0],
             [2, 7],
             [3, 2],
             [4, 1],
             [5, 15],
             [6, 5],
             [7, 6],
             [8, 7],
             [9, 8],
             [10, 4],
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
             [27, 25],
             [28, 27],
             [29, 3],
             [29, 9],
             [29, 13],
             [29, 19],
             [29, 22],
             [29, 26],
             [29, 28]]

    edge_sets = list()
    for ids in links:
        i, j = ids
        edge_sets.append([nodes[i], nodes[j]])

    due_times = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34, 233, 77, 88, 122, 71, 181,
                 340, 141, 209, 217, 256, 144, 307, 329, 269]

    due_dates = dict()
    for node, due_time in zip(nodes, due_times):
        due_dates[node] = due_time
    return edge_sets, due_dates


e, d = create_dag()

edge_sets = [e]
due_dates = [d]
