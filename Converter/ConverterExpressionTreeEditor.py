import json
import sys
import os
import argparse
import datetime


# colors used to display messages in the terminal.
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


# defines the file struct that is used to parse a file and return a struct of that file.
class File:
    def __init__(self, filename, new_filename, data_input, node_number, edge_number, root_node, node_connector,
                 node_structure):
        self.filename = filename
        self.new_filename = new_filename
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
export_parser = subparsers.add_parser("export")

# print parser commands
print_parser.add_argument("--all", help="Prints the description and the tree diagram.", action="store_true")
print_parser.add_argument("--tree", help="Prints the tree diagram.", action="store_true")
print_parser.add_argument("--level", help="Prints the node.")
print_parser.add_argument("--node", help="Prints the node.")
print_parser.add_argument("--description", help="Prints the description.", action="store_true")
print_parser.add_argument("--notConnected", "-nc", help="Prints the not connected nodes.", action="store_true")

# node parser commands
node_parser.add_argument("--expand", "-ex", help="Expands the node.")
node_parser.add_argument("--scaleDown", "-sd", help="Scales down the node.")
# TODO to implement:
node_parser.add_argument("--create", help="Creates a node.")
node_parser.add_argument("--modify", help="Modifies a node.")
node_parser.add_argument("--delete", help="Deletes a node.")

# export parser commands
export_parser.add_argument("--json", help="Exports the modified tree to .json format.")
# TODO to implement:
export_parser.add_argument("--txt", help="Exports the modified tree to .txt format.")


# Creates a new file in .tree extension where the current status of the program is saved.
# if called with an argument it returns name_treediagram.tree, else datetime_treediagram.tree
def create_new_file(existing_filename=None):
    if existing_filename:
        new_file_name = existing_filename.split('.')[0] + "_treediagram.tree"
    else:
        new_file_name = get_date_time() + "_treediagram.tree"
    f = open(new_file_name, "w")
    f.close()
    return new_file_name


def get_date_time():
    x = datetime.datetime.now()
    return (x.strftime("%Y") + x.strftime("%m") + x.strftime("%d") + "_" + x.strftime("%H") + x.strftime("%M")
            + x.strftime("%S"))


# given a file loads all the information from the file necessary to run the program.
def load_file(filename=None):
    edge_dictionary = {}
    node_dictionary = {}

    # TODO - option if file is .tree how to parse it?

    if len(sys.argv) == 2:
        if sys.argv[1].lower().endswith('.json'):
            filename = sys.argv[1]
            new_filename = create_new_file(sys.argv[1])

            # read the json file and copies the content to local variables, creating a dictionary for the nodes and one
            # for the edges
            with open(filename, 'r') as f:
                input_data = json.loads(f.read())

            file_node_number = len(input_data['nodes'])
            file_edge_number = len(input_data['edges'])

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

            for node in (input_data['nodes']):
                node_dictionary[node] = {'new_id': None,
                                         'expanded': False,
                                         'pieces': input_data['nodes'][node]['pieces'],
                                         'type': input_data['nodes'][node]['type'],
                                         'value': input_data['nodes'][node]['value']}
            f.close()

        # raise an error if file is not json file
        else:
            raise ValueError

    # if load_file called without argument (initialization of a blank tree diagram)
    else:
        new_filename = create_new_file()
        filename = None

        file_node_number = 0
        file_edge_number = 0
        file_selected_root_node = None
        file_node_connector = "#"
        input_data = None

    file_node_structure = "{parentID; nodeID; childrenID; label, type, value}"

    new_file = File(filename, new_filename, input_data, file_node_number, file_edge_number, file_selected_root_node,
                    file_node_connector, file_node_structure)

    return new_file, edge_dictionary, node_dictionary


# gives some general info for developing purposes
def dev_print_infos():
    print("-------------------------------------------------------")
    print("DATABASE AND INFO FOR DEVELOPING PURPOSES:")
    print(f"Number of nodes: {node_number}")
    print(f"Number of edges: {edge_number}")
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


# TODO descrizione
def populate_levels(root_node):
    node_levels = {}
    max_found_depth = 0

    if root_node:
        node_counter = 0
        new_id_counter = 1
        node_levels["not_connected"] = []
        for node in node_dictionary:
            if node_dictionary[node]['value'] == 'Not connected':
                node_levels["not_connected"].append(node)
                node_counter += 1

        node_dictionary[root_node].update({'new_id': 'root'})
        node_levels["root"] = [root_node]
        actual_level = "root"
        node_counter += 1

        while node_counter < node_number:
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
                node_dictionary[node].update({'new_id': new_id_counter, 'value': 'Not connected'})
                node_levels["not_connected"].append(node)
            delete_connection("all")

    return max_found_depth, node_levels


# exports the tree diagram to json format so that it can be imported to the expression tutor
# if it is called with an argument filename he keeps that argument as name, else he creates one.
# the file format is the same as the input json files that we read.
def export(export_filename):
    if not export_filename:
        export_filename = get_date_time() + "_treediagram.json"

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


def delete_connection(connection):
    if connection == "all":
        edge_dictionary.clear()


def print_description():
    print(f'type: treeDiagram, nodes: {node_number}, maxDepth: {max_depth}, nodeStructure: {node_structure}, '
          f'connector: "{node_connector}"')


def print_separator(number_of_separators=10, separator="#"):
    print(separator * number_of_separators)


# change expanded value to true
def expand_node(node_id):
    node_dictionary[node_id].update({"expanded": True})


def expand_all():
    for node_id in node_dictionary:
        node_dictionary[node_id].update({"expanded": True})


# change expanded value to true
def scale_down_node(node_id):
    node_dictionary[node_id].update({"expanded": False})


def scale_down_all():
    for node_id in node_dictionary:
        node_dictionary[node_id].update({"expanded": False})


def get_parent_node(node_id):
    find_parent = False
    for edge in edge_dictionary:
        if edge_dictionary[edge]['childNodeId'] == node_id:
            return node_dictionary[edge_dictionary[edge]['parentNodeId']]['new_id']
    if not find_parent:
        return 'null'


def get_children_nodes(node_id):
    find_children = False
    list_of_children = []
    for edge in edge_dictionary:
        if edge_dictionary[edge]['parentNodeId'] == node_id:
            find_children = True
            list_of_children.append(node_dictionary[edge_dictionary[edge]['childNodeId']]['new_id'])
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
    if node_dictionary[node_id]['pieces'] == '':
        return 'noLabel'
    return list_to_string(node_dictionary[node_id]['pieces'])


def get_type(node_id):
    if node_dictionary[node_id]['type'] == '':
        return 'noType'
    return node_dictionary[node_id]['type']


def get_value(node_id):
    if node_dictionary[node_id]['value'] == '':
        return 'noValue'
    return node_dictionary[node_id]['value']


def print_node(node_id):
    if node_dictionary[node_id]['expanded']:
        # return formatted expanded node
        return ('{' + 'parentID: ' + str(get_parent_node(node_id)) + '; ' +
                'nodeID: ' + str(node_dictionary[node_id]['new_id']) + '; ' +
                'childrenID: ' + str(get_children_nodes(node_id)) + '; ' +
                'label: ' + str(get_label(node_id)) + '; ' +
                'type: ' + str(get_type(node_id)) + '; ' +
                'value: ' + str(get_value(node_id)) + '}')
    else:
        # return formatted scaled down node
        return ('{' + str(get_parent_node(node_id)) + ';' +
                str(node_dictionary[node_id]['new_id']) + ';' +
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

        if "not_connected" in node_levels:
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
        for node in node_dictionary:
            if node_dictionary[node]['new_id'] == "root":
                return node

    if node_id_to_test.isnumeric():
        if 0 <= int(node_id_to_test) < node_number:
            for node in node_dictionary:
                if node_dictionary[node]['new_id'] == int(node_id_to_test):
                    return node

    else:
        return False


if __name__ == "__main__":

    node_levels = {}
    node_dictionary = {}
    edge_dictionary = {}
    max_depth = 0

    try:
        read_file, edge_dictionary, node_dictionary = load_file()
        data_in = read_file.data_input
        node_number = read_file.node_number
        edge_number = read_file.edge_number
        selected_root_node = read_file.root_node
        node_connector = read_file.node_connector
        node_structure = read_file.node_structure
        max_depth, node_levels = populate_levels(selected_root_node)

        print(f"loaded file: {read_file.filename}")
        print(f"created file: {read_file.new_filename}")

    except ValueError:
        print(f"{TerminalColors.FAIL}Warning: Accepts only .json and .tree files!{TerminalColors.ENDC}")

    dev_print_infos()
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
            try:
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

                elif args.notConnected:
                    print_levels("not_connected")
                    print('')

            except:
                print(
                    f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                    f"{TerminalColors.ENDC}")

        # node commands
        elif commandList[0] == 'node':
            try:
                args = parser.parse_args(commandList)

                if args.expand or args.scaleDown:
                    if args.expand == "all" or args.scaleDown == "all":
                        if args.expand == "all":
                            expand_all()
                        else:
                            scale_down_all()
                        print_levels()
                        print('')
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
                            print(f"{print_node(old_id)}")
                            print('')
                        else:
                            print(f"{TerminalColors.FAIL}Warning: Node {args_id} does not exist!{TerminalColors.ENDC}")
                            print('')

            except:
                print(
                    f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                    f"{TerminalColors.ENDC}")

        # export commands
        elif commandList[0] == 'export':
            try:
                args = parser.parse_args(commandList)

                # if command is export or export --json [filename.json]
                if len(commandList) == 1 or args.json:
                    if args.json:
                        if args.json.lower().endswith('.json'):
                            exported_file = export(args.json)
                            print(f"{TerminalColors.OKGREEN}Exported tree diagram to file: {exported_file}"
                                  f"{TerminalColors.ENDC}")
                            print('')
                        else:
                            print(
                                f"{TerminalColors.FAIL}Warning: The filename must be of the type filename.json!"
                                f"{TerminalColors.ENDC}")
                    else:
                        exported_file = export(None)
                        print(f"{TerminalColors.OKGREEN}Exported tree diagram to file: {exported_file}"
                              f"{TerminalColors.ENDC}")
                        print('')

            except:
                print(f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                      f"{TerminalColors.ENDC}")

        else:
            print(f"{TerminalColors.FAIL}Warning: Command {commandList[0]} does not exist!{TerminalColors.ENDC}")
            print('')

        # elif commandList[0] == 'createNode':
        #     # args = parser.parse_args(commandList)
        #     # print(args)
        #     break

        # elif commandList[0] == 'load':
        #     if os.path.isfile(commandList[1]):
        #         read_file = load_file(commandList[1])
        #         data_in = read_file.data_input
        #         node_number = read_file.node_number
        #         edge_number = read_file.edge_number
        #         selected_root_node = read_file.root_node
        #         node_connector = read_file.node_connector
        #         node_structure = read_file.node_structure
        #         node_dictionary = {selected_root_node: {'new_id': 'root', 'expanded': False}}
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
# - improve argparse error handling

# - esporta diagramma in un file txt

# - stampa un intervallo di linee

# - check 'parentPieceId' order

# carattere spazio - modificarlo nella grammatica

# vedere con federico lunghezza linea (nodo spezzato?)

# - gestire node creation
# 1 create -l label -v value -t type
# 2 connect nodeID1 nodeID2
# -> se fattibile decidere quale parentPieceId

# - indicare parentPieceId
# {2:1;6;null;"# + #";noType;noValue} 2:1 per indicare parentPieceId?

# - update value of a node
# node n0 label:"newLabel"  o  node n0 -l "newLabel"

# TODO capire cosa mettere nel file .tree e quando aggiornarlo (dopo ogni modifica)

# TODO delete_connection nodeID-nodeID, ricorsivo controllare se ha figli e cancellare anche quelle connessioni e
#  fare nodi not connected

# TODO delete_node nodeID, cancellare nodo, ricorsivo controllare se ha figli e cancellare anche quelle connessioni e
#  fare nodi not connected, se cancello root, tutti i nodi non connected
