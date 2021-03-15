# function to identify router with maximum connections
def identify_router(node_list):
    """
    This function return node name which has max connections
    Agrs:
       node_list(list): it has list of nodes
    Return:
        It will return node name which has max connection
    """
    node_count_dict = {}
    max_conn_node = node_list[0]
    max_conns = 0
    for node in node_list:
        if node in node_count_dict:
            node_count_dict[node] = node_count_dict[node] + 2
        else:
            node_count_dict[node] = 2 if node_count_dict else 1
        if node_count_dict[node] > max_conns:
            max_conns = node_count_dict[node]
            max_conn_node = node
    else:
        if node_count_dict[node] > 1:
            node_count_dict[node] = node_count_dict[node] - 1
            if node_count_dict[node] > max_conns:
                max_conn_node = node
    max_conn = node_count_dict[max_conn_node]
    node = [key for key, value in node_count_dict.items() if value == max_conn]
    return node


node_list = "1->2->3->5->2->1".split("->")
print(identify_router(node_list))