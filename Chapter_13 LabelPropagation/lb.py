# coding:UTF-8
'''
Date:20160805
@author: zhaozhiyong
'''
import string

def loadData(filePath):
    '''
    input:  filePath(string)文件的存储位置
    output: vector_dict(dict)节点：社区
            edge_dict(dict)存储节点之间的边和权重
    '''
    f = open(filePath)
    vector_dict = {}  # 存储节点
    edge_dict = {}  # 存储边
    for line in f.readlines():
        lines = line.strip().split("\t")

        for i in range(2):#  0 , 1
            if lines[i] not in vector_dict:  # 节点已存储
                # 将节点放入到vector_dict中，设置所属社区为其自身
                vector_dict[lines[i]] = int(lines[i]) #字符串转换成浮点型
                # 将边放入到edge_dict
                edge_list = []
                if len(lines) == 3:
                    edge_list.append(lines[1 - i] + ":" + lines[2])
                else:
                    edge_list.append(lines[1 - i] + ":" + "1")
                edge_dict[lines[i]] = edge_list
            else:  # 节点未存储
                edge_list = edge_dict[lines[i]]
                if len(lines) == 3:
                    edge_list.append(lines[1 - i] + ":" + lines[2])
                else:
                    edge_list.append(lines[1 - i] + ":" + "1")
                edge_dict[lines[i]] = edge_list
    f.close()
    return vector_dict, edge_dict

def get_max_community_label(vector_dict, adjacency_node_list):
    '''得到相邻接的节点中标签数最多的标签
    input:  vector_dict(dict)节点：社区
            adjacency_node_list(list)节点的邻接节点
    output: 节点所属的社区
    '''
    label_dict = {}
    for node in adjacency_node_list:
        node_id_weight = node.strip().split(":")
        node_id = node_id_weight[0]#邻接节点
        node_weight = int(node_id_weight[1])#与邻接节点之间的权重
        if vector_dict[node_id] not in label_dict:
            label_dict[vector_dict[node_id]] = node_weight
        else:
            label_dict[vector_dict[node_id]] += node_weight

    # 找到最大的标签
    sort_list = sorted(label_dict.items(), key=lambda d: d[1], reverse=True)  #reverse = True进行降序排列、列表、数据项的方法 
    return sort_list[0][0]

def check(vector_dict, edge_dict):
    '''检查是否满足终止条件
    input:  vector_dict(dict)节点：社区
            edge_dict(dict)存储节点之间的边和权重
    output: 是否需要更新
    '''
    for node in vector_dict.keys():
        adjacency_node_list = edge_dict[node]  # 与节点node相连接的节点
        node_label = vector_dict[node]  # 节点node所属社区
        label = get_max_community_label(vector_dict, adjacency_node_list)
        if node_label == label: # 对每个节点，其所属的社区标签是最大的
            continue
        else:
            return 0
    return 1

def label_propagation(vector_dict, edge_dict):
    '''标签传播
    input:  vector_dict(dict)节点：社区
            edge_dict(dict)存储节点之间的边和权重
    output: vector_dict(dict)节点：社区
    '''
    # 初始化，设置每个节点属于不同的社区
    t = 0
    # 以随机的次序处理每个节点
    while True:
        if (check(vector_dict, edge_dict) == 0):
            t = t + 1
            print ("iteration: ", t)
            # 对每一个node进行更新
            for node in vector_dict.keys():
                adjacency_node_list = edge_dict[node] # 获取节点node的邻接节点
                vector_dict[node] = get_max_community_label(vector_dict, adjacency_node_list)
            print (vector_dict)
        else:
            break
    return vector_dict

def save_result(file_name, vec_new):
    f_result = open(file_name, "w")
    for key in vec_new.keys():
        f_result.write(str(key) + "\t" + str(vec_new[key]) + "\n")   
    f_result.close()


if __name__ == "__main__":
    # 1、导入数据
    print ("----------1.load data ------------")
    vector_dict, edge_dict = loadData("cd_data.txt")
    print ("original community: \n", vector_dict)
    # 2、利用label propagation算法进行社区划分
    print ("----------2.label propagation ------------")
    vec_new = label_propagation(vector_dict, edge_dict)
    # 3、保存最终的社区划分的结果
    print ("----------3.save result ------------")
    save_result("result1", vec_new)
    print ("final_result:", vec_new)
    
    
'''
    ----------1.load data ------------
original community: 
 {'0': 0, '2': 2, '3': 3, '4': 4, '5': 5, '1': 1, '7': 7, '6': 6, '10': 10, '11': 11, '8': 8, '9': 9, '14': 14, '15': 15, '12': 12, '13': 13}
----------2.label propagation ------------
iteration:  1
{'0': 2, '2': 2, '3': 2, '4': 2, '5': 2, '1': 2, '7': 2, '6': 2, '10': 2, '11': 2, '8': 2, '9': 2, '14': 2, '15': 2, '12': 2, '13': 2}
----------3.save result ------------
final_result: {'0': 2, '2': 2, '3': 2, '4': 2, '5': 2, '1': 2, '7': 2, '6': 2, '10': 2, '11': 2, '8': 2, '9': 2, '14': 2, '15': 2, '12': 2, '13': 2}

'''
    
    
    
