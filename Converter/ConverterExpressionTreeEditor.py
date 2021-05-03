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
    def __init__(self, filename, new_filename, root_node, node_connector, node_structure, last_node, last_edge,
                 max_depth, treeFileBoolean, tree_structure):
        self.filename = filename
        self.new_filename = new_filename
        self.root_node = root_node
        self.node_connector = node_connector
        self.node_structure = node_structure
        self.last_node = last_node
        self.last_edge = last_edge
        self.max_depth = max_depth
        self.treeFileBoolean = treeFileBoolean
        self.tree_structure = tree_structure


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
node_parser.add_argument("--create", help="Creates a node.", action="store_true")
node_parser.add_argument("--label", "-l", help="Specifies label of a node.")
node_parser.add_argument("--type", "-t", help="Specifies type of a node.")
node_parser.add_argument("--connect", help="Creates an edge between two nodes.")
node_parser.add_argument("--root", help="Sets a new root node in the diagram.")
node_parser.add_argument("--modify", "-m", help="Modifies a node.")

# TODO to implement:
node_parser.add_argument("--delete", help="Deletes a node.")
node_parser.add_argument("--disconnect", help="Deletes an edge between two nodes.")

# export parser commands
export_parser.add_argument("--json", help="Exports the modified tree to .json format.")
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
    edge_dictionary.clear()
    node_dictionary.clear()
    file_node_structure = "{parentID; nodeID; childrenID; label, type, value}"
    tree_boolean = False
    file_max_depth = 0

    if filename:
        if filename.lower().endswith('.json'):
            # if file exists
            if os.path.isfile(filename):
                new_filename = create_new_file(filename)
                # read the json file and copies the content to local variables, creating a dictionary for the nodes and one
                # for the edges
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
                    node_dictionary[node] = {'new_id': None,
                                             'expanded': False,
                                             'pieces': input_data['nodes'][node]['pieces'],
                                             'type': input_data['nodes'][node]['type'],
                                             'value': input_data['nodes'][node]['value']}
                    last_node_created = node
                f.close()

            # raise an error if file does not exist
            else:
                raise ValueError

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
                raise ValueError

        # raise an error if file is not json file
        else:
            raise ValueError

    # if load_file called without argument (initialization of a blank tree diagram)
    else:
        new_filename = create_new_file()

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


# TODO descrizione
def populate_levels(root_node):
    max_found_depth = 0
    node_levels.clear()

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
                node_dictionary[node].update({'new_id': new_id_counter, 'value': 'Not connected'})
                node_levels["not_connected"].append(node)
                new_id_counter += 1
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


# exports a txt file with the actual state of the diagram that we normally see in the terminal
def export_txt(export_txt_filename):
    with open(export_txt_filename, 'w') as txt_file:
        txt_file.write(f"{print_description()}\n")
        txt_file.write(f"{print_separator()}\n")
        txt_file.write(print_levels())
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


# returns the description of the tree diagram as a string (for printing)
def print_description():
    return (f'type: treeDiagram, nodes: {len(node_dictionary)}, maxDepth: {max_depth}, '
            f'nodeStructure: {node_structure}, connector: "{node_connector}"')


# returns the separator between the description and the tree diagram as a string (for printing)
def print_separator(number_of_separators=10, separator="#"):
    return "" + separator * number_of_separators


# changes the root node, all the other nodes are changed to not connected and all the edges are deleted.
def set_root(new_root):
    node_dictionary[new_root].update({'new_id': 'root', 'value': ''})
    new_id_counter = 0
    for node in node_dictionary:
        if node != new_root:
            node_dictionary[node].update({'new_id': new_id_counter, 'value': 'Not connected'})
            new_id_counter += 1
    delete_connection("all")


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
                                 'value': "Not connected"}
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


# TODO finish the function
def delete_connection(connection):
    if connection == "all":
        edge_dictionary.clear()
        global last_edge_created
        last_edge_created = '00'


# change expanded value to true
def expand_node(node_id):
    node_dictionary[node_id].update({"expanded": True})


# expands all the nodes in the tree diagram
def expand_all():
    for node_id in node_dictionary:
        node_dictionary[node_id].update({"expanded": True})


# change expanded value to false
def scale_down_node(node_id):
    node_dictionary[node_id].update({"expanded": False})


# scales down all the nodes in the tree diagram
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
    new_string = '"' + (''.join([str(elem) for elem in list_of_elements])) + '"'
    return new_string


# returns the label of a node
def get_label(node_id):
    if node_dictionary[node_id]['pieces'] == '':
        return 'noLabel'
    return list_to_string(node_dictionary[node_id]['pieces'])


# returns the type of a node
def get_type(node_id):
    if node_dictionary[node_id]['type'] == '':
        return 'noType'
    return node_dictionary[node_id]['type']


# returns value of a node
def get_value(node_id):
    if node_dictionary[node_id]['value'] == '':
        return 'noValue'
    return node_dictionary[node_id]['value']


# prints a node, expanded or not
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


# prints the node present in a level
def print_level(level):
    string = ""
    for node in node_levels[level]:
        string += print_node(node) + " "
    return string


# prints the level indicator and the nodes present in a level
def print_levels(selected_level=False):
    string_to_return = ''
    if selected_level:
        if selected_level in ["root", "not_connected"]:
            string_to_return = f"@{selected_level} {print_level(selected_level)}"
        else:
            string_to_return = f"@{int(selected_level)} {print_level(int(selected_level))}"
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
        if 0 <= int(node_id_to_test) < len(node_dictionary):
            for node in node_dictionary:
                if node_dictionary[node]['new_id'] == int(node_id_to_test):
                    return node

    else:
        return False


if __name__ == "__main__":

    if 0 < len(sys.argv) < 3:
        file_to_read = None
        if len(sys.argv) == 2:
            file_to_read = sys.argv[1]

        node_levels = {}
        node_dictionary = {}
        edge_dictionary = {}
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

            print(f"loaded file: {read_file.filename} - created file: {read_file.new_filename}")
            # dev_print_infos()
            print(print_description())
            print(print_separator())
            print(print_levels())

        except ValueError:
            print(f"{TerminalColors.FAIL}Warning: Accepts only .json and .tree files or file does not exist!"
                  f"{TerminalColors.ENDC}")
    else:
        print(f"{TerminalColors.FAIL}Warning: Expects input of type python3 'ConverterExpressionTreeEditor.py' or "
              f"python3 ConverterExpressionTreeEditor.py filename.tree/json!{TerminalColors.ENDC}")



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
            print(f'List of existing commands: \nclear or c \nquit or q \nhelp or h \nprint \nprint --all '
                  f'\nprint --tree \nprint --level[levelNumber] \nprint --node[nodeID] \nprint --description '
                  f'\nprint --notConnected or -nc \nnode --expand or -ex[nodeID or "all"] '
                  f'\nnode --scaleDown or -sd[nodeID or "all"] '
                  f'\nnode --create --label or -l[label] --type or -t[type] '
                  f'\nnode --connnect [parentNodeID]-[childNodeID] '
                  f'\nnode --modify or -m [nodeID] --label or -l [label] --type or -t [type] \nnode --root [nodeID] '
                  f'\nexport \nexport --json[filename.json] \nexport --txt [exportfile.txt] '
                  f'\nload [filename.tree / filename.json / ""] \n')

        # PRINT commands
        elif commandList[0] == 'print':
            try:
                args = parser.parse_args(commandList)

                if len(commandList) == 1 or args.all:
                    print(print_description())
                    print(print_separator())
                    print(print_levels())

                elif args.tree:
                    print(print_levels())

                elif args.description:
                    print(print_description() + '\n')

                elif args.node:
                    old_id = check_node_get_original_id(args.node)
                    if old_id:
                        print(f"{print_node(old_id)}\n")
                    else:
                        print(f"{TerminalColors.FAIL}Warning: Node {args.node} does not exist!{TerminalColors.ENDC}\n")

                elif args.level:
                    if args.level in ["root", "not_connected"] or 0 < int(args.level) <= max_depth:
                        print(f"{print_levels(args.level)}\n")
                    else:
                        print(f"{TerminalColors.FAIL}Warning: Level {args.level} does not exist!{TerminalColors.ENDC}"
                              f"\n")

                elif args.notConnected:
                    print(f"{print_levels('not_connected')}\n")

            except:
                print(
                    f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                    f"{TerminalColors.ENDC}\n")

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
                        print(f"{print_levels()}\n")
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
                            print(f"{TerminalColors.FAIL}Warning: Node {args_id} does not exist!{TerminalColors.ENDC}"
                                  f"\n")

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
                    print(f"{TerminalColors.OKGREEN}Created node: {print_node(new_node)}"
                          f"{TerminalColors.ENDC}\n")

                # modifies a node with parameters label or type
                elif args.modify:
                    found_id = check_node_get_original_id(args.modify)
                    if found_id:
                        if not args.label and not args.type:
                            print(f"{TerminalColors.FAIL}Warning: To modify the node {args.modify} the script needs "
                                  f"one or two arguments!{TerminalColors.ENDC}\n")
                        else:
                            if args.label:
                                node_dictionary[found_id].update({"pieces": args.label})
                            if args.type:
                                node_dictionary[found_id].update({"type": args.type})
                            max_depth, node_levels = populate_levels(selected_root_node)
                            update_tree_file()
                            print(f"{TerminalColors.OKGREEN}Modified node: {print_node(found_id)}"
                                  f"{TerminalColors.ENDC}\n")
                    else:
                        print(f"{TerminalColors.FAIL}Warning: Node {args.modify} does not exist!{TerminalColors.ENDC}"
                              f"\n")

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
                                print(f"{TerminalColors.OKGREEN}Connected nodes: {parsed_arguments[0]}-"
                                      f"{parsed_arguments[1]}{TerminalColors.ENDC}\n")
                            else:
                                print(f"{TerminalColors.FAIL}Warning: Node {parsed_arguments[1]} does not exist, or "
                                      f"is already connected!{TerminalColors.ENDC}\n")
                        else:
                            print(f"{TerminalColors.FAIL}Warning: Node {parsed_arguments[0]} does not exist, or is not "
                                  f"yet connected!{TerminalColors.ENDC}\n")

                # changes the root node, all the other nodes are changed to not connected and all the edges are deleted.
                elif args.root:
                    new_root_node_id = check_node_get_original_id(args.root)
                    selected_root_node = new_root_node_id
                    set_root(selected_root_node)
                    max_depth, node_levels = populate_levels(selected_root_node)
                    update_tree_file()
                    print(f"{TerminalColors.OKGREEN}Changed root node to: {args.root}{TerminalColors.ENDC}\n")

            except:
                print(
                    f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                    f"{TerminalColors.ENDC}\n")

        # EXPORT commands
        elif commandList[0] == 'export':
            try:
                args = parser.parse_args(commandList)

                # if command is export or export --json [filename.json]
                if len(commandList) == 1 or args.json:
                    if args.json:
                        if args.json.lower().endswith('.json'):
                            exported_file = export(args.json)
                            print(f"{TerminalColors.OKGREEN}Exported tree diagram to file: {exported_file}"
                                  f"{TerminalColors.ENDC}\n")
                        else:
                            print(
                                f"{TerminalColors.FAIL}Warning: The filename must be of the type filename.json!"
                                f"{TerminalColors.ENDC}\n")
                    else:
                        exported_file = export(None)
                        print(f"{TerminalColors.OKGREEN}Exported tree diagram to file: {exported_file}"
                              f"{TerminalColors.ENDC}\n")

                elif args.txt:
                    if args.txt.lower().endswith('.txt'):
                        export_txt(args.txt)
                        print(f"{TerminalColors.OKGREEN}Exported tree diagram to file: {args.txt}"
                              f"{TerminalColors.ENDC}\n")
                    else:
                        print(f"{TerminalColors.FAIL}Warning: The filename must be of the type filename.txt!"
                              f"{TerminalColors.ENDC}\n")


            except:
                print(f"{TerminalColors.FAIL}Warning: Something went wrong with command {commandList[0]}!"
                      f"{TerminalColors.ENDC}\n")

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

                    print(f"loaded file: {read_file.filename} - created file: {read_file.new_filename}")
                    print(print_description())
                    print(print_separator())
                    print(print_levels())

                except ValueError:
                    print(f"{TerminalColors.FAIL}Warning: Accepts only .json and .tree files or file does not exist!"
                          f"{TerminalColors.ENDC}")
            else:
                print(
                    f"{TerminalColors.FAIL}Warning: Expects input of type python3 'ConverterExpressionTreeEditor.py' or "
                    f"python3 ConverterExpressionTreeEditor.py filename.tree/json!{TerminalColors.ENDC}")

        else:
            print(f"{TerminalColors.FAIL}Warning: Command {commandList[0]} does not exist!{TerminalColors.ENDC}\n")

# TODO s:
# - printare le info dei nodi in base alla node Structure scelta

# - migliorare il main program che gestisce gli input dalla shell con argparse e definire bene i commandi
# - check if input one of the recognized commands
# - standard command: command node -> to check
# - improve argparse error handling

# - stampa un intervallo di linee

# carattere spazio - modificarlo nella grammatica

# vedere con federico lunghezza linea (nodo spezzato?)

# quando connect nodeID1 nodeID2
# -> se fattibile decidere quale parentPieceId

# - check 'parentPieceId' order

# - indicare parentPieceId
# {2:1;6;null;"# + #";noType;noValue} 2:1 per indicare parentPieceId?

# - in connect node specificare parent piece order

# TODO delete_connection nodeID-nodeID, ricorsivo controllare se ha figli e cancellare anche quelle connessioni e
#  fare nodi not connected

# TODO delete_node nodeID, cancellare nodo, ricorsivo controllare se ha figli e cancellare anche quelle connessioni e
#  fare nodi not connected, se cancello root, tutti i nodi non connected
