# import libraries
import json
import sys
import os
import argparse
import platform

# import helper files
import nearleyReader
import utils


# defines the file struct that is used to parse a file and return a struct of that file.
class File:
    def __init__(self, filename, new_filename, root_node, node_connector, node_structure, last_node, last_edge,
                 max_depth, tree_file_boolean, tree_structure):
        self.filename = filename
        self.new_filename = new_filename
        self.root_node = root_node
        self.node_connector = node_connector
        self.node_structure = node_structure
        self.last_node = last_node
        self.last_edge = last_edge
        self.max_depth = max_depth
        self.treeFileBoolean = tree_file_boolean
        self.tree_structure = tree_structure


# ArgumentParser commands
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='types of print')

print_parser = subparsers.add_parser("print")
node_parser = subparsers.add_parser("node")
export_parser = subparsers.add_parser("export")

# print parser commands
print_parser.add_argument("--all", "-a", help="Prints the description and the tree diagram.", action="store_true")
print_parser.add_argument("--tree", "-tr", help="Prints the tree diagram.", action="store_true")
print_parser.add_argument("--level", "-lev", help="Prints the node.")
print_parser.add_argument("--node", "-n", help="Prints the node.")
print_parser.add_argument("--description", "-des", help="Prints the description.", action="store_true")
print_parser.add_argument("--notConnected", "-nc", help="Prints the not connected nodes.", action="store_true")

# node parser commands
node_parser.add_argument("--expand", "-ex", help="Expands the node.")
node_parser.add_argument("--scaleDown", "-sd", help="Scales down the node.")
node_parser.add_argument("--create", "-c", help="Creates a node.", action="store_true")
node_parser.add_argument("--label", "-l", help="Specifies label of a node.")
node_parser.add_argument("--type", "-t", help="Specifies type of a node.")
node_parser.add_argument("--connect", "-con", help="Creates an edge between two nodes.")
node_parser.add_argument("--root", "-r", help="Sets a new root node in the diagram.")
node_parser.add_argument("--modify", "-m", help="Modifies a node.")
node_parser.add_argument("--find", "-f", help="Finds a node based on label.")
node_parser.add_argument("--disconnect", "-dis", help="Deletes an edge between two nodes.")
node_parser.add_argument("--delete", "-del", help="Deletes a node.")

# export parser commands
export_parser.add_argument("--json", "-j", help="Exports the modified tree to .json format.")
export_parser.add_argument("--txt", help="Exports the modified tree to .txt format.")


# given a file loads all the information from the file necessary to run the program.
def load_file(filename=None):
    edge_dictionary.clear()
    node_dictionary.clear()
    file_node_structure = "{parentID; nodeID; childrenID; label; type; value}"
    tree_boolean = False
    file_max_depth = 0

    if filename:
        if filename.lower().endswith('.json'):
            # if file exists
            if os.path.isfile(filename):
                new_filename = utils.create_new_file(filename)
                # read the json file and copies the content to local variables, creating a dictionary for the nodes
                # and one for the edges
                with open(filename, 'r') as f:
                    input_data = json.loads(f.read())

                # check if the root node exists
                file_selected_root_node = None
                for node in (input_data['nodes']):
                    if input_data['selectedRootNode'] == node:
                        file_selected_root_node = input_data['selectedRootNode']

                file_node_connector = input_data['nodeConnector']

                for edge in (input_data['edges']):
                    edge_dictionary[edge] = {'parentNodeId': input_data['edges'][edge]['parentNodeId'],
                                             'childNodeId': input_data['edges'][edge]['childNodeId'],
                                             'parentPieceId': input_data['edges'][edge]['parentPieceId']}
                    last_edge_created = edge

                for node in (input_data['nodes']):
                    node_value = input_data['nodes'][node]['value']
                    if node_value == "Not connected":
                        node_value = "NotConnected"

                    node_dictionary[node] = {'new_id': None,
                                             'expanded': False,
                                             'pieces': input_data['nodes'][node]['pieces'],
                                             'type': input_data['nodes'][node]['type'],
                                             'value': node_value}
                    last_node_created = node
                f.close()

            # raise an error if file does not exist
            else:
                raise FileNotFoundError

        # if file is of type .txt, we parse it with nearley.js parser
        elif filename.lower().endswith('.txt'):
            # if file exists
            if os.path.isfile(filename):
                (filename, new_filename, read_node_dictionary, last_node_created, read_edge_dictionary,
                 last_edge_created,
                 file_selected_root_node, file_node_connector, file_node_structure, file_max_depth,
                 tree_boolean) = nearleyReader.read_txt_file_nearley(filename)

                # copy elements from new created dictionary in old one
                for i in read_node_dictionary:
                    node_dictionary[i] = read_node_dictionary[i]
                for l in read_edge_dictionary:
                    edge_dictionary[l] = read_edge_dictionary[l]

            # raise an error if file does not exist
            else:
                raise FileNotFoundError

        # if file is .tree parse it for recover last state (with a json parser)
        elif filename.lower().endswith('.tree'):
            new_filename = filename
            tree_boolean = True

            # if file exists
            if os.path.isfile(filename):
                # read the input of the .tree file (structured like a json file)
                with open(new_filename, 'r') as f:
                    input_data = json.loads(f.read())

                # read variables
                file_node_connector = input_data['variables']['nodeConnector']
                filename = input_data['variables']['originalFileName']
                last_node_created = input_data['variables']['LastCreatedNodeID']
                last_edge_created = input_data['variables']['LastCreatedEdgeID']
                file_node_structure = input_data['variables']['nodeStructure']
                file_max_depth = input_data['variables']['maxDepth']

                # check if the root node exists and register value
                file_selected_root_node = None
                for node in (input_data['nodes']):
                    if input_data['variables']['selectedRootNode'] == node:
                        file_selected_root_node = input_data['variables']['selectedRootNode']

                # read edges
                for edge in input_data['edges']:
                    edge_dictionary[edge] = {'parentNodeId': input_data['edges'][edge]['parentNodeId'],
                                             'childNodeId': input_data['edges'][edge]['childNodeId'],
                                             'parentPieceId': input_data['edges'][edge]['parentPieceId']}

                # read nodes
                for node in input_data['nodes']:
                    node_dictionary[node] = {'new_id': input_data['nodes'][node]['new_id'],
                                             'expanded': input_data['nodes'][node]['expanded'],
                                             'pieces': input_data['nodes'][node]['pieces'],
                                             'type': input_data['nodes'][node]['type'],
                                             'value': input_data['nodes'][node]['value']}

                # read tree structure
                node_levels.clear()
                for level in input_data['treeStructure']:
                    node_levels[level] = input_data['treeStructure'][level]

                f.close()

            # raise an error if file does not exist
            else:
                raise FileNotFoundError

        # raise an error if file is not json file
        else:
            raise TypeError

    # if load_file called without argument (initialization of a blank tree diagram)
    else:
        new_filename = utils.create_new_file()

        last_node_created = '00'  # 00 indicates no nodes
        last_edge_created = '00'  # 00 indicates no edges

        file_selected_root_node = None
        file_node_connector = "#"

    new_file = File(filename, new_filename, file_selected_root_node, file_node_connector, file_node_structure,
                    last_node_created, last_edge_created, file_max_depth, tree_boolean, node_levels)

    return new_file, edge_dictionary, node_dictionary


# gives some general info for developing purposes
def dev_print_infos():
    print("-------------------------------------------------------")
    print("DATABASE AND INFO FOR DEVELOPING PURPOSES:")
    print(f"Number of nodes: {len(node_dictionary)}")
    print(f"Number of edges: {len(edge_dictionary)}")
    print(f"Root node: {selected_root_node}")
    print(f"Node connector: {node_connector}")
    print("\n Dictionary of nodes:")
    for node in node_dictionary:
        print(f" {node} - {node_dictionary[node]}")
    print("\n Dictionary of edges:")
    for edge in edge_dictionary:
        print(f" {edge} - {edge_dictionary[edge]}")
    print("\n Tree structure:")
    for level in node_levels:
        print(f" {level} - {node_levels[level]}")
    print("-------------------------------------------------------\n")


# populate levels takes the nodes and gives the new id's and creates the new tree structure
def populate_levels(root_node):
    max_found_depth = 0
    node_levels.clear()

    if root_node:
        node_counter = 0
        new_id_counter = 1
        node_levels["not_connected"] = []
        for node in node_dictionary:
            if node_dictionary[node]['value'] == 'NotConnected':
                node_levels["not_connected"].append(node)
                node_counter += 1

        node_dictionary[root_node].update({'new_id': 'root'})
        node_levels["root"] = [root_node]
        actual_level = "root"
        node_counter += 1

        while node_counter < len(node_dictionary):
            for actual_node in node_levels[actual_level]:
                next_level = 1 if actual_level == "root" else actual_level + 1

                for edge in edge_dictionary:
                    if edge_dictionary[edge]['parentNodeId'] == actual_node:
                        if next_level not in node_levels:
                            node_levels[next_level] = []
                            max_found_depth += 1
                        node_levels[next_level].append(edge_dictionary[edge]['childNodeId'])
                        node_dictionary[edge_dictionary[edge]['childNodeId']].update({'new_id': new_id_counter})
                        node_counter += 1
                        new_id_counter += 1

            actual_level = 1 if actual_level == "root" else actual_level + 1

        # assign new id to not connected nodes and set expanded value to False.
        if "not_connected" in node_levels:
            for not_connected_node in node_levels["not_connected"]:
                node_dictionary[not_connected_node].update({'new_id': new_id_counter})
                new_id_counter += 1

    else:
        # if root node not specified but nodes exist, all the nodes are categorized as not connected and all the
        # connections are deleted
        if len(node_dictionary) > 0:
            node_levels["not_connected"] = []
            new_id_counter = 0
            for node in node_dictionary:
                node_dictionary[node].update({'new_id': new_id_counter, 'value': 'NotConnected'})
                node_levels["not_connected"].append(node)
                new_id_counter += 1
            delete_connection_all()

    return max_found_depth, node_levels


# exports the tree diagram to json format so that it can be imported to the expression tutor
# if it is called with an argument filename he keeps that argument as name, else he creates one.
# the file format is the same as the input json files that we read.
def export(export_filename):
    if not export_filename:
        export_filename = utils.get_date_time() + "_treediagram.json"

    # restructure the node dictionary, so that it contains the same fields as the expression tutor json file.
    node_export_dictionary = {}
    for node in node_dictionary:
        node_export_dictionary[node] = {'pieces': node_dictionary[node]['pieces'],
                                        'x': 0,
                                        'y': 0,
                                        'type': node_dictionary[node]['type'],
                                        'value': node_dictionary[node]['value'],
                                        'isFinal': False}

    data = {"nodes": node_export_dictionary,
            "edges": edge_dictionary,
            "selectedRootNode": selected_root_node,
            "nodeConnector": node_connector}

    with open(export_filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)

    outfile.close()
    return export_filename


# exports a txt file with the actual state of the diagram that we normally see in the terminal
def export_txt(export_txt_filename):
    with open(export_txt_filename, 'w') as txt_file:
        txt_file.write(f"{print_description()}\n")
        txt_file.write(f"{print_separator()}\n")
        txt_file.write(print_levels(None, None))
    txt_file.close()


# called always after a change in the diagram, copies the actual state of the tree diagram in the .tree file.
def update_tree_file():
    tree_variables = {'originalFileName': read_file.filename,
                      'selectedRootNode': selected_root_node,
                      'nodeConnector': node_connector,
                      'nodeStructure': node_structure,
                      'maxDepth': max_depth,
                      'LastCreatedNodeID': last_node_created,
                      'LastCreatedEdgeID': last_edge_created}

    data = {"nodes": node_dictionary,
            "edges": edge_dictionary,
            "treeStructure": node_levels,
            "variables": tree_variables}

    with open(read_file.new_filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)

    outfile.close()
    return


# when exporting a txt or json file with a name parameter, update consequently also the name of the .tree file
def rename_tree_file(exported_file_name):
    exported_file_name = exported_file_name.split('.')[0] + "_td.tree"
    os.rename(read_file.new_filename, exported_file_name)
    read_file.new_filename = exported_file_name


# returns the description of the tree diagram as a string (for printing)
def print_description():
    return (f'type: treeDiagram, nodes: {len(node_dictionary)}, maxDepth: {max_depth}, '
            f'nodeStructure: {node_structure}, connector: "{node_connector}"')


# returns the separator between the description and the tree diagram as a string (for printing)
def print_separator(number_of_separators=10, separator="-"):
    return "" + separator * number_of_separators


# changes the root node, all the other nodes are changed to not connected and all the edges are deleted.
def set_root(new_root):
    node_dictionary[new_root].update({'new_id': 'root', 'value': ''})
    new_id_counter = 0
    for node in node_dictionary:
        if node != new_root:
            node_dictionary[node].update({'new_id': new_id_counter, 'value': 'NotConnected'})
            new_id_counter += 1
    delete_connection_all()


# creates a new node, standard value not connected, label and node type can be specified
def create_node(label, node_type):
    if last_node_created == '00':
        node_key = 'n0'
    else:
        node_key = 'n' + str(int(last_node_created[1:]) + 1)

    node_dictionary[node_key] = {'new_id': None,
                                 'expanded': False,
                                 'pieces': label,
                                 'type': node_type,
                                 'value': "NotConnected"}
    return node_key


# connects a node that is already in the diagram (parent node) with a node that is not connected (child node).
def connect_nodes(parent_node, child_node):
    if last_edge_created == '00':
        edge_key = 'e0'
    else:
        edge_key = 'e' + str(int(last_edge_created[1:]) + 1)

    edge_dictionary[edge_key] = {'parentNodeId': parent_node,
                                 'childNodeId': child_node,
                                 'parentPieceId': 0}

    node_dictionary[child_node].update({"value": ""})
    return edge_key


# disconnects two nodes that are connected in the diagram (parent node - child node) and removes also the connections
# of all the sub-nodes.
def disconnect_nodes(edge_remove):
    nodes_to_check_connections = [edge_dictionary[edge_remove]['childNodeId']]
    del edge_dictionary[edge_remove]

    while nodes_to_check_connections:
        if nodes_to_check_connections[0] is None:
            break

        children_nodes = get_children_nodes(nodes_to_check_connections[0])

        if children_nodes:
            for child in children_nodes:
                nodes_to_check_connections.append(check_node_get_original_id(str(child)))
                edge = check_edge(str(nodes_to_check_connections[0]), check_node_get_original_id(str(child)))
                del edge_dictionary[edge]

        node_dictionary[nodes_to_check_connections[0]].update({'value': 'NotConnected'})
        nodes_to_check_connections.pop(0)


# returns true if connection between parent and child node exists
def check_edge(parent_node, child_node):
    for edge in edge_dictionary:
        if edge_dictionary[edge]['parentNodeId'] == parent_node and edge_dictionary[edge]['childNodeId'] == child_node:
            return edge
    return None


# deletes all the connections in the tree diagram
def delete_connection_all():
    edge_dictionary.clear()
    global last_edge_created
    last_edge_created = '00'


# deletes a node and if necessary disconnects the nodes affected from this change
def delete_node(node_id_to_delete):
    parent_node_id = get_parent_node(node_id_to_delete)

    # case the node is not connected
    if node_dictionary[node_id_to_delete]['value'] == 'NotConnected':
        del node_dictionary[node_id_to_delete]

    # case the node has a parent
    elif parent_node_id:
        disconnect_nodes(check_edge(check_node_get_original_id(str(parent_node_id)), node_id_to_delete))
        del node_dictionary[node_id_to_delete]

    # case the node is the root and has no parent
    else:
        delete_connection_all()
        global selected_root_node
        selected_root_node = None
        del node_dictionary[node_id_to_delete]


# change expanded value to true
def expand_node(node_id_to_expand):
    node_dictionary[node_id_to_expand].update({"expanded": True})


# expands all the nodes in the tree diagram
def expand_all():
    for node_id_to_expand in node_dictionary:
        node_dictionary[node_id_to_expand].update({"expanded": True})


# change expanded value to false
def scale_down_node(node_id_to_scale_down):
    node_dictionary[node_id_to_scale_down].update({"expanded": False})


# scales down all the nodes in the tree diagram
def scale_down_all():
    for node_id_to_scale_down in node_dictionary:
        node_dictionary[node_id_to_scale_down].update({"expanded": False})


# returns the parent node of a node
def get_parent_node(node_id_find_parent):
    find_parent = False
    for edge in edge_dictionary:
        if edge_dictionary[edge]['childNodeId'] == node_id_find_parent:
            return node_dictionary[edge_dictionary[edge]['parentNodeId']]['new_id']
    if not find_parent:
        return None


# returns the children nodes (if any) of a node
def get_children_nodes(node_id_find_child):
    find_children = False
    list_of_children = []
    for edge in edge_dictionary:
        if edge_dictionary[edge]['parentNodeId'] == node_id_find_child:
            find_children = True
            list_of_children.append(node_dictionary[edge_dictionary[edge]['childNodeId']]['new_id'])
    if find_children:
        return list_of_children
    else:
        return None


# Convert list to string
def list_to_string(list_of_elements):
    new_string = '"' + (''.join([str(elem) for elem in list_of_elements])) + '"'
    return new_string


# returns the label of a node
def get_label(node_id_find_label):
    if node_dictionary[node_id_find_label]['pieces'] == '':
        return 'noLabel'
    return list_to_string(node_dictionary[node_id_find_label]['pieces'])


# returns the type of a node
def get_type(node_id_find_type):
    if node_dictionary[node_id_find_type]['type'] == '':
        return 'noType'
    return node_dictionary[node_id_find_type]['type']


# returns value of a node
def get_value(node_id_find_value):
    if node_dictionary[node_id_find_value]['value'] == '':
        return 'noValue'
    return node_dictionary[node_id_find_value]['value']


# prints a node, expanded or not
def print_node(node_id_print):
    children = get_children_nodes(node_id_print)
    if not children:
        children = 'null'
    if len(children) == 1:
        children = children[0]

    parent = get_parent_node(node_id_print)
    if not parent:
        parent = 'null'

    if node_dictionary[node_id_print]['expanded']:
        # return formatted expanded node
        return ('{' + 'parentID: ' + str(parent) + '; ' +
                'nodeID: ' + str(node_dictionary[node_id_print]['new_id']) + '; ' +
                'childrenID: ' + str(children) + '; ' +
                'label: ' + str(get_label(node_id_print)) + '; ' +
                'type: ' + str(get_type(node_id_print)) + '; ' +
                'value: ' + str(get_value(node_id_print)) + '}')
    else:
        # return formatted scaled down node
        return ('{' + str(parent) + ';' +
                str(node_dictionary[node_id_print]['new_id']) + ';' +
                str(children) + ';' +
                str(get_label(node_id_print)) + ';' +
                str(get_type(node_id_print)) + ';' +
                str(get_value(node_id_print)) + '}')


# prints the node present in a level
def print_level(level):
    string = ""
    for single_node in node_levels[level]:
        string += print_node(single_node) + " "
    return string


# prints the level indicator and the nodes present in a level
def print_levels(selected_level, to_level):
    string_to_return = ''
    if selected_level:
        # if we want to print a single line
        if not to_level:
            if selected_level in ["root", "not_connected"]:
                string_to_return = f"@{selected_level} {print_level(selected_level)}"
            else:
                string_to_return = f"@{int(selected_level)} {print_level(int(selected_level))}"
        # if we want to print a rang of lines
        else:
            if selected_level == "root":
                string_to_return += f"@root {print_level('root')}\n"
                selected_level = 0

            for level in node_levels:
                if level in ["not_connected", "root"]:
                    continue

                if (int(selected_level) <= level) and (level <= int(to_level)):
                    string_to_return += f"@{level} {print_level(level)}\n"
    # if we want to print all lines
    else:
        for level in node_levels:
            if level != "not_connected":
                string_to_return += f"@{level} {print_level(level)}\n"

        if "not_connected" in node_levels:
            level = "not_connected"
            string_to_return += f"@{level} {print_level(level)}\n"
    return string_to_return


# clears the terminal
def clear():
    _ = os.system('clear')


# checks the input given by the user
def get_string(message):
    while True:
        string = input(message)
        if string != '':
            return string
        else:
            utils.print_message(False, f"Warning: Your input was empty!\n")


# if the node exists returns the original ID of the node
def check_node_get_original_id(node_id_to_test):
    if node_id_to_test == "root":
        for node in node_dictionary:
            if node_dictionary[node]['new_id'] == "root":
                return node

    if node_id_to_test.isnumeric():
        if 0 <= int(node_id_to_test) < len(node_dictionary):
            for node in node_dictionary:
                if node_dictionary[node]['new_id'] == int(node_id_to_test):
                    return node

    else:
        return False


# returns a list of node ID's that contain the letter, number, symbol or word that is passed to the function in
# the label of the node.
def find_node(argument):
    found_nodes_list = []
    for node_id in node_dictionary:
        if str(get_label(node_id)).find(argument) != -1:
            found_nodes_list.append(node_id)
    return found_nodes_list


# ---------------------------------------------------------------------------------------------------------------------
# main function
if __name__ == "__main__":

    max_depth = 0
    node_levels = {}
    node_dictionary = {}
    edge_dictionary = {}
    last_node_created = '00'  # 00 indicates no nodes
    last_edge_created = '00'  # 00 indicates no edges

    if 0 < len(sys.argv) < 3:
        file_to_read = None
        if len(sys.argv) == 2:
            file_to_read = sys.argv[1]

        try:
            read_file, edge_dictionary, node_dictionary = load_file(file_to_read)
            selected_root_node = read_file.root_node
            node_connector = read_file.node_connector
            node_structure = read_file.node_structure
            last_node_created = read_file.last_node
            last_edge_created = read_file.last_edge
            if read_file.treeFileBoolean:
                max_depth = read_file.max_depth
                node_levels = read_file.tree_structure
            else:
                max_depth, node_levels = populate_levels(selected_root_node)
                update_tree_file()

            print(f"loaded file: {read_file.filename} - created file: {read_file.new_filename}\n")

            print(print_description())
            print(print_separator())
            print(print_levels(None, None))

        except FileNotFoundError:
            utils.print_message(False, f"Warning: File does not exist!\n")
        except TypeError:
            utils.print_message(False, f"Warning: Accepts only .json, .txt and .tree files!\n")
        except FileExistsError:
            utils.print_message(False, f"Warning: The nearley.js parser was not able to parse the file!\n")

    else:
        utils.print_message(False, f"Warning: Expects input of type python3 ConverterExpressionTreeEditor.py or "
                                   f"python3 ConverterExpressionTreeEditor.py filename.tree/json/txt!\n")

    while True:
        command = get_string("Insert command: ")
        commandList = command.strip().split(" ")

        # HELPER commands
        if commandList[0] in ['clear', 'c']:
            clear()

        elif commandList[0] in ['quit', 'q']:
            break

        # returns the list of existing commands
        elif commandList[0] in ['help', 'h']:
            print(f'List of existing commands: \nclear or c \nquit or q \nhelp or h \nprint \nprint --all or -a '
                  f'\nprint --tree or -tr \nprint --level or -lev [levelNumber] or [fromLevelNumber]-[toLevelNumber] '
                  f'\nprint --node or -n [nodeID] \nprint --description or -des \nprint --notConnected or -nc '
                  f'\nnode --expand or -ex [nodeID or "all"] \nnode --scaleDown or -sd [nodeID or "all"] '
                  f'\nnode --create or -c --label or -l [label] --type or -t [type] '
                  f'\nnode --connect or -con [parentNodeID]-[childNodeID] '
                  f'\nnode --disconnect or -dis [parentNodeID]-[childNodeID] \nnode --delete or -del [nodeID]'
                  f'\nnode --modify or -m [nodeID] --label or -l [label] --type or -t [type] '
                  f'\nnode --root or -r [nodeID] \nnode --find or -f [argument] \nexport '
                  f'\nexport --json or -j [filename.json] \nexport --txt [exportfile.txt] '
                  f'\nload [filename.tree / filename.json / filename.txt / ""] \n')

        # PRINT commands
        elif commandList[0] == 'print':
            try:
                args = parser.parse_args(commandList)

                if len(commandList) == 1 or args.all:
                    print(print_description())
                    print(print_separator())
                    print(print_levels(None, None))

                elif args.tree:
                    print(print_levels(None, None))

                elif args.description:
                    print(print_description() + '\n')

                elif args.node:
                    old_id = check_node_get_original_id(args.node)
                    if old_id:
                        print(f"{print_node(old_id)}\n")
                    else:
                        utils.print_message(False, f"Warning: Node {args.node} does not exist!\n")

                elif args.level:
                    # print more levels
                    if "-" in args.level:
                        parsed_arguments = args.level.split("-")
                        if parsed_arguments[0] == 'root' or 0 < int(parsed_arguments[0]) <= max_depth:
                            if ((0 < int(parsed_arguments[1]) <= max_depth and parsed_arguments[0] == 'root') or
                                    (0 < int(parsed_arguments[1]) <= max_depth and
                                     int(parsed_arguments[0]) < int(parsed_arguments[1]))):
                                print(f"{print_levels(parsed_arguments[0], parsed_arguments[1])}")
                            else:
                                utils.print_message(False, f"Warning: Level {parsed_arguments[1]} does not exist or is "
                                                           f"smaller than level {parsed_arguments[0]}!\n")
                        else:
                            utils.print_message(False, f"Warning: Level {parsed_arguments[0]} does not exist!\n")

                    # print single level
                    else:
                        if args.level in ["root", "not_connected"] or 0 < int(args.level) <= max_depth:
                            print(f"{print_levels(args.level, None)}\n")
                        else:
                            utils.print_message(False, f"Warning: Level {args.level} does not exist!\n")

                elif args.notConnected:
                    print(f"{print_levels('not_connected', None)}\n")

            except:
                utils.print_message(False, f"Warning: Something went wrong with command {commandList[0]}!\n")

        # NODE commands
        elif commandList[0] == 'node':
            try:
                args = parser.parse_args(commandList)

                if args.expand or args.scaleDown:
                    if args.expand == "all" or args.scaleDown == "all":
                        if args.expand == "all":
                            expand_all()
                        else:
                            scale_down_all()
                        print(f"{print_levels(None, None)}\n")
                        update_tree_file()
                    else:
                        if args.expand:
                            args_id = args.expand
                        else:
                            args_id = args.scaleDown
                        old_id = check_node_get_original_id(args_id)
                        if old_id:
                            if args.expand:
                                expand_node(old_id)
                            else:
                                scale_down_node(old_id)
                            print(f"{print_node(old_id)}\n")
                            update_tree_file()
                        else:
                            utils.print_message(False, f"Warning: Node {args_id} does not exist!\n")

                # creates a new node
                elif args.create:
                    if args.label:
                        new_label = args.label
                    else:
                        new_label = ""

                    if args.type:
                        new_node_type = args.type
                    else:
                        new_node_type = ""

                    new_node = create_node(new_label, new_node_type)
                    last_node_created = new_node
                    max_depth, node_levels = populate_levels(selected_root_node)
                    update_tree_file()
                    utils.print_message(True, f"Created node: {print_node(new_node)}\n")

                # finds a node
                elif args.find:
                    found_nodes = find_node(args.find)
                    if not found_nodes:
                        utils.print_message(False, f"No node contains: {args.find}\n")
                    else:
                        utils.print_message(True, f"Found nodes:", False)
                        for node in found_nodes:
                            print(f"ID: {node_dictionary[node]['new_id']} - NODE: {print_node(node)}")
                        print('')

                # modifies a node with parameters label or type
                elif args.modify:
                    found_id = check_node_get_original_id(args.modify)
                    if found_id:
                        if not args.label and not args.type:
                            utils.print_message(False, f"Warning: To modify the node {args.modify} the script needs "
                                                       f"one or two arguments!\n")
                        else:
                            if args.label:
                                node_dictionary[found_id].update({"pieces": args.label})
                            if args.type:
                                node_dictionary[found_id].update({"type": args.type})
                            max_depth, node_levels = populate_levels(selected_root_node)
                            update_tree_file()
                            utils.print_message(True, f"Modified node: {print_node(found_id)}\n")
                    else:
                        utils.print_message(False, f"Warning: Node {args.modify} does not exist!\n")

                # connects a node that is already in the diagram with a node that is not connected.
                elif args.connect:
                    parsed_arguments = args.connect.split("-")
                    if len(parsed_arguments) == 2:
                        parent_node_id = check_node_get_original_id(parsed_arguments[0])
                        child_node_id = check_node_get_original_id(parsed_arguments[1])
                        if parent_node_id and (parent_node_id not in node_levels["not_connected"]):
                            if child_node_id and (child_node_id in node_levels["not_connected"]):
                                new_edge = connect_nodes(parent_node_id, child_node_id)
                                last_edge_created = new_edge
                                max_depth, node_levels = populate_levels(selected_root_node)
                                update_tree_file()
                                utils.print_message(True, f"Connected nodes: {parsed_arguments[0]}-"
                                                          f"{parsed_arguments[1]}\n")
                            else:
                                utils.print_message(False, f"Warning: Node {parsed_arguments[1]} does not exist, or "
                                                           f"is already connected!\n")
                        else:
                            utils.print_message(False, f"Warning: Node {parsed_arguments[0]} does not exist, or is not "
                                                       f"yet connected!\n")

                # disconnects two nodes that are connected in the diagram.
                elif args.disconnect:
                    parsed_arguments = args.disconnect.split("-")
                    if len(parsed_arguments) == 2:
                        parent_node_id = check_node_get_original_id(parsed_arguments[0])
                        child_node_id = check_node_get_original_id(parsed_arguments[1])

                        if parent_node_id and (parent_node_id not in node_levels["not_connected"]):
                            if child_node_id and (child_node_id not in node_levels["not_connected"]):
                                edge_to_remove = check_edge(parent_node_id, child_node_id)

                                if edge_to_remove:
                                    disconnect_nodes(edge_to_remove)

                                    max_depth, node_levels = populate_levels(selected_root_node)

                                    update_tree_file()
                                    utils.print_message(True, f"Disconnected nodes: {parsed_arguments[0]}-"
                                                              f"{parsed_arguments[1]} and all the child connections!\n")
                                else:
                                    utils.print_message(False, f"Warning: Edge between {parent_node_id} and "
                                                               f"{child_node_id} does not exist!\n")
                            else:
                                utils.print_message(False, f"Warning: Node {parsed_arguments[1]} does not exist, or is "
                                                           f"not connected!\n")
                        else:
                            utils.print_message(False, f"Warning: Node {parsed_arguments[0]} does not exist, or is not "
                                                       f"connected!\n")

                # deletes a node in thee tree diagram
                elif args.delete:
                    node_id = check_node_get_original_id(args.delete)
                    if node_id:
                        delete_node(node_id)
                        max_depth, node_levels = populate_levels(selected_root_node)
                        update_tree_file()
                        utils.print_message(True, f"Deleted node: {node_id}\n")
                    else:
                        utils.print_message(False, f"Warning: Node {node_id} does not exist!\n")

                # changes the root node, all the other nodes are changed to not connected and all the edges are deleted.
                elif args.root:
                    new_root_node_id = check_node_get_original_id(args.root)
                    selected_root_node = new_root_node_id
                    set_root(selected_root_node)
                    max_depth, node_levels = populate_levels(selected_root_node)
                    update_tree_file()
                    utils.print_message(True, f"Changed root node to: {args.root}\n")

            except:
                utils.print_message(False, f"Warning: Something went wrong with command {commandList[0]}!\n")

        # EXPORT commands
        elif commandList[0] == 'export':
            try:
                args = parser.parse_args(commandList)

                # if command is export or export --json [filename.json]
                if len(commandList) == 1 or args.json:
                    if args.json:
                        if args.json.lower().endswith('.json'):
                            exported_file = export(args.json)
                            rename_tree_file(exported_file)
                            utils.print_message(True, f"Exported tree diagram to file: {exported_file}\n")
                        else:
                            utils.print_message(False, f"Warning: The filename must be of the type filename.json!\n")
                    else:
                        exported_file = export(None)
                        rename_tree_file(exported_file)
                        utils.print_message(True, f"Exported tree diagram to file: {exported_file}\n")

                elif args.txt:
                    if args.txt.lower().endswith('.txt'):
                        export_txt(args.txt)
                        rename_tree_file(args.txt)
                        utils.print_message(True, f"Exported tree diagram to file: {args.txt}\n")
                    else:
                        utils.print_message(False, f"Warning: The filename must be of the type filename.txt!\n")

            except:
                utils.print_message(False, f"Warning: Something went wrong with command {commandList[0]}!\n")

        # LOAD command
        # loads a new file of type json/tree/empty (creation of a new tree)
        elif commandList[0] == 'load':

            if 0 < len(commandList) < 3:
                file_to_read = None
                if len(commandList) == 2:
                    file_to_read = commandList[1]

                last_node_created = '00'  # 00 indicates no nodes
                last_edge_created = '00'  # 00 indicates no edges
                max_depth = 0

                try:
                    read_file, edge_dictionary, node_dictionary = load_file(file_to_read)
                    selected_root_node = read_file.root_node
                    node_connector = read_file.node_connector
                    node_structure = read_file.node_structure
                    last_node_created = read_file.last_node
                    last_edge_created = read_file.last_edge
                    if read_file.treeFileBoolean:
                        max_depth = read_file.max_depth
                        node_levels = read_file.tree_structure
                    else:
                        max_depth, node_levels = populate_levels(selected_root_node)
                        update_tree_file()

                    print(f"loaded file: {read_file.filename} - created file: {read_file.new_filename}\n")
                    print(print_description())
                    print(print_separator())
                    print(print_levels(None, None))

                except FileNotFoundError:
                    utils.print_message(False, f"Warning: File does not exist!\n")
                except TypeError:
                    utils.print_message(False, f"Warning: Accepts only .json, .txt and .tree files!\n")
                except FileExistsError:
                    utils.print_message(False, f"Warning: The nearley parser was not able to parse the file!\n")
            else:
                utils.print_message(False, f"Warning: Expects input of type python3 'ConverterExpressionTreeEditor.py' "
                                           f"or python3 ConverterExpressionTreeEditor.py filename.tree/json!\n")

        # DEBUGGER command
        # prints some helpful states and general information about the program to the terminal for developing purposes.
        elif commandList[0] == 'debugger':
            dev_print_infos()

        else:
            utils.print_message(False, f"Warning: Command {commandList[0]} does not exist!\n")
