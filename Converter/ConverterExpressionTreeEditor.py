import json
import sys
import os
import argparse


class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class File:
    def __init__(self, filename, data_input, node_number, edge_number, root_node, node_connector, node_structure):
        self.filename = filename
        self.data_input = data_input
        self.node_number = node_number
        self.edge_number = edge_number
        self.root_node = root_node
        self.node_connector = node_connector
        self.node_structure = node_structure


# ArgumentParser commands
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='types of print')

print_parser = subparsers.add_parser("print")
node_parser = subparsers.add_parser("node")

print_parser.add_argument("--all", help="Prints the description and the tree diagram.", action="store_true")
print_parser.add_argument("--tree", help="Prints the tree diagram.", action="store_true")
print_parser.add_argument("--level", help="Prints the node.")
print_parser.add_argument("--node", help="Prints the node.")
print_parser.add_argument("--description", help="Prints the description.", action="store_true")

# parser.add_argument('-l', '--label', help="Label of a node.")
# parser.add_argument('-v', '--value', help="Value of a node.", default='Not connected')
# parser.add_argument('-t', '--type', help="Type of a node.")


def load_file(filename=sys.argv[1]):
    # read the json file
    with open(filename, 'r') as f:
        input_data = json.loads(f.read())

    file_node_number = len(input_data['nodes'])
    file_edge_number = len(input_data['edges'])

    file_selected_root_node = input_data['selectedRootNode']
    file_node_connector = input_data['nodeConnector']
    file_node_structure = "{parentID; nodeID; childrenID; label, type, value}"

    new_file = File(filename, input_data, file_node_number, file_edge_number, file_selected_root_node,
                    file_node_connector, file_node_structure)

    f.close()
    return new_file


# give some general info for developing purposes
def dev_print_infos():
    print("-------------------------------------------------------")
    print("INFO FOR DEVELOPING PURPOSE ONLY:")
    print(f"Number of nodes: {node_number}")
    print(f"Number of edges: {edge_number}")
    print(f"Root node: {selected_root_node}")
    print(f"Node connector: {node_connector}")
    print("\n Nodes:")
    for node in (data_in['nodes']):
        print(f" {node} - {data_in['nodes'][node]}")
    print("\n Edges:")
    for edge in (data_in['edges']):
        print(f" {edge} - {data_in['edges'][edge]}")
    print("-------------------------------------------------------\n")


def populate_levels(root_node):
    node_counter = 0
    new_id_counter = 1
    max_found_depth = 0
    node_levels["not_connected"] = []
    for node in (data_in['nodes']):
        if data_in['nodes'][node]['value'] == 'Not connected':
            node_levels["not_connected"].append(node)
            node_counter += 1

    node_levels["root"] = [root_node]
    actual_level = "root"
    node_counter += 1

    while node_counter < node_number:
        for actual_node in node_levels[actual_level]:
            next_level = 1 if actual_level == "root" else actual_level + 1

            for edge in (data_in['edges']):
                if data_in['edges'][edge]['parentNodeId'] == actual_node:
                    if next_level not in node_levels:
                        node_levels[next_level] = []
                        max_found_depth += 1
                    node_levels[next_level].append(data_in['edges'][edge]['childNodeId'])
                    id_dictionary[data_in['edges'][edge]['childNodeId']] = {'new_id': new_id_counter, 'expanded': False}
                    node_counter += 1
                    new_id_counter += 1

        actual_level = 1 if actual_level == "root" else actual_level + 1

    # assign new id to not connected nodes and set expanded value to False.
    if "not_connected" in node_levels:
        for not_connected_node in node_levels["not_connected"]:
            id_dictionary[not_connected_node] = {'new_id': new_id_counter, 'expanded': False}
            new_id_counter += 1

    return max_found_depth


def print_description():
    print(f'type: treeDiagram, nodes: {node_number}, maxDepth: {max_depth}, nodeStructure: {node_structure}, '
          f'connector: "{node_connector}"')


def print_separator(number_of_separators=10, separator="#"):
    print(separator * number_of_separators)


# change expanded value to true
def expand_node(node_id):
    id_dictionary[node_id].update({"expanded": True})


# change expanded value to true
def scale_down_node(node_id):
    id_dictionary[node_id].update({"expanded": False})


def get_parent_node(node_id):
    find_parent = False
    for edge in (data_in['edges']):
        if data_in['edges'][edge]['childNodeId'] == node_id:
            return id_dictionary[data_in['edges'][edge]['parentNodeId']]['new_id']
    if not find_parent:
        return 'null'


def get_children_nodes(node_id):
    find_children = False
    list_of_children = []
    for edge in (data_in['edges']):
        if data_in['edges'][edge]['parentNodeId'] == node_id:
            find_children = True
            list_of_children.append(id_dictionary[data_in['edges'][edge]['childNodeId']]['new_id'])
    if find_children:
        if len(list_of_children) == 1:
            return list_of_children[0]
        else:
            return list_of_children
    else:
        return 'null'


# Convert list to string
def list_to_string(list_of_elements):
    new_string = '"' + (' '.join([str(elem) for elem in list_of_elements])) + '"'
    return new_string


def get_label(node_id):
    if data_in['nodes'][node_id]['pieces'] == '':
        return 'noLabel'
    return list_to_string(data_in['nodes'][node_id]['pieces'])


def get_type(node_id):
    if data_in['nodes'][node_id]['type'] == '':
        return 'noType'
    return data_in['nodes'][node_id]['type']


def get_value(node_id):
    if data_in['nodes'][node_id]['value'] == '':
        return 'noValue'
    return data_in['nodes'][node_id]['value']


def print_node(node_id):
    if id_dictionary[node_id]['expanded']:
        # return formatted expanded node
        return ('{' + 'parentID: ' + str(get_parent_node(node_id)) + '; ' +
                'nodeID: ' + str(id_dictionary[node_id]['new_id']) + '; ' +
                'childrenID: ' + str(get_children_nodes(node_id)) + '; ' +
                'label: ' + str(get_label(node_id)) + '; ' +
                'type: ' + str(get_type(node_id)) + '; ' +
                'value: ' + str(get_value(node_id)) + '}')
    else:
        # return formatted scaled down node
        return ('{' + str(get_parent_node(node_id)) + ';' +
                str(id_dictionary[node_id]['new_id']) + ';' +
                str(get_children_nodes(node_id)) + ';' +
                str(get_label(node_id)) + ';' +
                str(get_type(node_id)) + ';' +
                str(get_value(node_id)) + '}')


def print_level(level):
    string = ""
    for node in node_levels[level]:
        string += print_node(node) + " "
    return string


def print_levels(selected_level=False):
    if selected_level:
        if selected_level in ["root", "not_connected"]:
            print(f"@{selected_level} {print_level(selected_level)}")
        else:
            print(f"@{int(selected_level)} {print_level(int(selected_level))}")
    else:
        for level in node_levels:
            if level != "not_connected":
                print(f"@{level} {print_level(level)}")
        level = "not_connected"
        print(f"@{level} {print_level(level)}")


def clear():
    _ = os.system('clear')


def get_string(message):
    while True:
        string = input(message)
        if string != '':
            return string
        else:
            print(f"{TerminalColors.FAIL}Warning: Your input was empty!{TerminalColors.ENDC}")


def check_node_get_original_id(node_id_to_test):
    if node_id_to_test == "root":
        for node in id_dictionary:
            if id_dictionary[node]['new_id'] == "root":
                return node

    if node_id_to_test.isnumeric():
        if 0 < int(node_id_to_test) < node_number:
            for node in id_dictionary:
                if id_dictionary[node]['new_id'] == int(node_id_to_test):
                    return node

    else:
        return False


if __name__ == "__main__":
    # dev_print_infos()

    read_file = load_file()
    data_in = read_file.data_input
    node_number = read_file.node_number
    edge_number = read_file.edge_number
    selected_root_node = read_file.root_node
    node_connector = read_file.node_connector
    node_structure = read_file.node_structure
    id_dictionary = {selected_root_node: {'new_id': 'root', 'expanded': False}}
    node_levels = {}
    max_depth = populate_levels(selected_root_node)
    print(f"loaded file: {read_file.filename}\n")

    # print(f"Dictionary of nodes: {node_levels} \n")
    # print(f"Dictionary of id's: {id_dictionary}")

    print_description()
    print_separator()
    print_levels()
    print('')

    while True:
        command = get_string("Insert command: ")
        commandList = command.strip().split(" ")

        # helper commands
        if commandList[0] in ['clear', 'c']:
            clear()

        elif commandList[0] in ['quit', 'q']:
            break

        elif commandList[0] in ['help', 'h']:
            print('here should be the list of possible commands')
            print('')

        # print commands
        elif commandList[0] == 'print':
            args = parser.parse_args(commandList)

            if len(commandList) == 1 or args.all:
                print_description()
                print_separator()
                print_levels()
                print('')

            elif args.tree:
                print_levels()
                print('')

            elif args.description:
                print_description()
                print('')

            elif args.node:
                old_id = check_node_get_original_id(args.node)
                if old_id:
                    print(f"{print_node(old_id)}")
                    print('')
                else:
                    print(f"{TerminalColors.FAIL}Warning: Node {args.node} does not exist!{TerminalColors.ENDC}")
                    print('')

            elif args.level:
                if args.level in ["root", "not_connected"] or 0 < int(args.level) <= max_depth:
                    print_levels(args.level)
                    print('')
                else:
                    print(f"{TerminalColors.FAIL}Warning: Level {args.level} does not exist!{TerminalColors.ENDC}")
                    print('')

        # elif commandList[0] == 'expandNode':
        #     if len(commandList) == 2:
        #         if check_node(commandList[1]):
        #             expand_node(commandList[1])
        #             print(f"{TerminalColors.OKGREEN}Expanded node: {commandList[1]}{TerminalColors.ENDC}")
        #             print('')
        #         else:
        #             print(f"{TerminalColors.FAIL}Warning: Node {commandList[1]} does not exist!{TerminalColors.ENDC}")
        #     else:
        #         print(f"{TerminalColors.FAIL}Wrong syntax: expandNode nodeID{TerminalColors.ENDC}")

        # elif commandList[0] == 'createNode':
        #     # args = parser.parse_args(commandList)
        #     # print(args)
        #     break

        # elif commandList[0] == 'scaleDownNode':
        #     scale_down_node(commandList[1])
        #     print('')

        # elif commandList[0] == 'load':
        #     if os.path.isfile(commandList[1]):
        #         read_file = load_file(commandList[1])
        #         data_in = read_file.data_input
        #         node_number = read_file.node_number
        #         edge_number = read_file.edge_number
        #         selected_root_node = read_file.root_node
        #         node_connector = read_file.node_connector
        #         node_structure = read_file.node_structure
        #         id_dictionary = {selected_root_node: {'new_id': 'root', 'expanded': False}}
        #         node_levels = {}
        #         max_depth = populate_levels(selected_root_node)
        #         print(f"loaded file: {read_file.filename}\n")
        #         print_description()
        #         print_separator()
        #         print_levels()
        #         print('')
        #     else:
        #         print(f"{TerminalColors.FAIL}File {commandList[1]} not accessible.{TerminalColors.ENDC}")

# TODO
# - printare le info dei nodi in base alla node Structure scelta

# - migliorare il main program che gestisce gli input dalla shell con argparse e definire bene i commandi
# - check if input one of the recognized commands
# - standard command: command node -> to check
# - gestire gli errori di argparse

# - esporta diagramma in un file txt o json

# - stampa un intervallo di linee

# - check 'parentPieceId' order

# - per i comandi usare il dizionario per tradurre i valori dei nodi nelle nuove id assegnate

# carattere spazio - modificarlo nella grammatica

# vedere con federico lunghezza linea (nodo spezzato?)

# - gestire node creation
# 1 create -l label -v value -t type
# 2 connect nodeID1 nodeID2
# -> se fattibile decidere quale parentPieceId

# - implementare node deletion

# - indicare parentPieceId
# {2:1;6;null;"# + #";noType;noValue} 2:1 per indicare parentPieceId?

# - update value of a node
# node n0 label:"newLabel"  o  node n0 -l "newLabel"
