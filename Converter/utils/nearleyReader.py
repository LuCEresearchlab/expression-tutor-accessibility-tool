# import libraries
import json
import subprocess

# import helper files
import utils


# given a number or string generates the node id
def get_node_ID(nodeID):
    if nodeID == 'root':
        return 'n0'
    else:
        return 'n' + str(nodeID)


# function that reads a formatted .txt file using the nearley.js parser
# the .txt file must follow the grammar rules that we defined.
def read_txt_file_nearley(file_to_open):
    # bash command that is needed to read a .txt file using the nerley.js parser with the grammar.js grammar in
    # the terminal
    bash_command = ['nearley-test', './../Grammar/grammar.js', '-q']

    # try to read the input file, if nearley.js is not able to read it we raise a FileExistsError
    input_file = open(file_to_open)
    process = subprocess.Popen(bash_command, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        raise FileExistsError

    else:
        # First we make some transformations to the output that we become from nearley, so that the output is in a
        # regular json standard.
        stdout = stdout.decode("utf-8")
        stdout = stdout[2:-3]

        replacements = {
            'description': '"description"',
            'type': '"type"',
            'nodeNumber': '"nodeNumber"',
            'maxDepth': '"maxDepth"',
            'nodeStructure': '"nodeStructure"',
            'graphLevels': '"graphLevels"',
            'level': '"level"',
            'nodes': '"nodes"',
            'parentID': '"parentID"',
            'nodeID': '"nodeID"',
            'childrenID': '"childrenID"',
            'nodeType': '"nodeType"',
            'nodeValue': '"nodeValue"',
            'nodeLabel': '"nodeLabel"',
            'nodeOptionals': '"nodeOptionals"',
            'undefined': '"undefined"',
            'connector': '"connector"',
            'label': '"label"',
            'value': '"value"',
            "'": '"',
            '{"parentID"; "nodeID"; "childrenID"; "label"; "type"; "value"}':
                '{parentID; nodeID; childrenID; label; type; value}',
            '{"parentID"; "nodeID"; "childrenID"; "label"; "type"}': '{parentID; nodeID; childrenID; label; type}',
            '{"parentID"; "nodeID"; "childrenID"; "label"}': '{parentID; nodeID; childrenID; label}',
            '{"parentID"; "nodeID"; "childrenID"}': '{parentID; nodeID; childrenID}'
        }

        for m, n in replacements.items():
            stdout = stdout.replace(m, n)

        # we parse the json input
        file_dictionary = json.loads(stdout)

        # we remove some redundant parenthesis
        levels = {}
        for level in file_dictionary['graphLevels']:
            levels[level[0]['level']] = level[0]['nodes']
        file_dictionary['graphLevels'] = levels

        # we parse the different parts of the file
        filename = file_to_open
        new_filename = utils.create_new_file(filename)
        file_node_connector = file_dictionary['description']['connector']
        file_node_structure = file_dictionary['description']['nodeStructure']
        tree_boolean = False
        file_max_depth = 0
        file_selected_root_node = None
        type_of_node = ''
        value_of_node = ''
        node_dictionary = {}
        edge_dictionary = {}
        edge_counter = 0

        # we parse the nodes and the edges
        for sub_level in file_dictionary['graphLevels']:
            if sub_level not in ['root', 'not_connected']:
                file_max_depth = sub_level
            for node in file_dictionary['graphLevels'][sub_level]:
                sub_node = node[0]
                if sub_node['nodeID'] == 'root':
                    file_selected_root_node = 'n0'
                if 'nodeOptionals' in sub_node:
                    type_of_node = sub_node['nodeOptionals']['nodeType']
                    value_of_node = sub_node['nodeOptionals']['nodeValue']

                node_id = get_node_ID(sub_node['nodeID'])

                node_dictionary[node_id] = {'new_id': None,
                                            'expanded': False,
                                            'pieces': sub_node['nodeLabel'],
                                            'type': type_of_node,
                                            'value': value_of_node
                                            }
                last_node_created = node_id

                # to parse the edges we use the children that we find in the different nodes
                children = sub_node['childrenID']
                if children != 'null':
                    children = sub_node['childrenID'][0]
                    parent_piece_id = 0
                    for child in children:
                        edge = 'e' + str(edge_counter)
                        edge_dictionary[edge] = {'parentNodeId': node_id,
                                                 'childNodeId': get_node_ID(child[0]),
                                                 'parentPieceId': parent_piece_id}
                        last_edge_created = edge
                        parent_piece_id += 1
                        edge_counter += 1

        # we return all the parsed data
        return (filename, new_filename, node_dictionary, last_node_created, edge_dictionary, last_edge_created,
                file_selected_root_node, file_node_connector, file_node_structure, file_max_depth, tree_boolean)
