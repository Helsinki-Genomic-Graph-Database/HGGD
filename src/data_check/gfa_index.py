examplelist = ["E gres s1+ s2+ b1 e1 b2 e2", "E 5984 s3- s4- b1 e1 b2 e2", "E * s5- s6+ b1 e54 b2 e2", "E * s7+ s8- b1 e1 bfjeios e2 fjoire"]

edge_line_list = []
node_dict = {}
new_node_name = 1

def change_orientation(orientation):
    if orientation == "-":
        orientation = "+"
    elif orientation == "+":
        orientation = "-"
    return orientation

for line in examplelist:
    line = str(line)
    print(line)
    if line[0] == "E":
        # Edge line format should be "E <eid:opt_id> <sid1:ref> <sid2:ref> <beg1:pos> <end1:pos> <beg2:pos> <end2:pos> <alignment> <tag>*
        # where the nodes are "<sid1:ref>" and "<sid2:ref>"
        # e.g. "E * s1+ s2- b1 e1 b2 e2" -> nodes are "s1+" and "s2-"
        new_line = line.lstrip("E")
        new_line_parts = new_line.split()
        node1a = new_line_parts[1]
        orientation = node1a[-1]
        other_orientation = change_orientation(orientation)
        node1b = node1a[0:-1]+other_orientation
        node2a = new_line_parts[2]
        orientation = node2a[-1]
        other_orientation = change_orientation(orientation)
        node2b = node2a[0:-1]+other_orientation
        nodes = [node1a, node1b, node2a, node2b]
        for node in nodes:
            if not node in node_dict:
                node_dict[node] = str(new_node_name)
                new_node_name += 1
            print(node, node_dict[node])
        string_line = "e "+node_dict[node1a]+" "+node_dict[node2a]+"\n"
        edge_line_list.append(string_line)
        string_line = "e "+node_dict[node2b]+" "+node_dict[node1b]+"\n"
        edge_line_list.append(string_line)
for line in edge_line_list:
    print(line)