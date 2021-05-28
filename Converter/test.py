import json
import subprocess

# file_to_open = './../Grammar/acceptedExample2.txt'
# bashCommand = ['nearley-test', './../Grammar/grammar.js', '-q']

file_to_open = './acceptedExample2.txt'
bashCommand = ['nearley-test', './grammar.js', '-q']

input_file = open(file_to_open)
process = subprocess.Popen(bashCommand, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stderr)
print(stdout)


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
    '{"parentID"; "nodeID"; "childrenID"}': '{parentID; nodeID; childrenID}',
    "'": '"'
}

for m, n in replacements.items():
    stdout = stdout.replace(m, n)

print(stdout)

file_dictionary = json.loads(stdout)

# print(file_dictionary)
#
# print(file_dictionary['description']['type'])
# print(file_dictionary['description']['nodeNumber'])
# print(file_dictionary['description']['maxDepth'])
# print(file_dictionary['description']['nodeStructure'])

levels = {}
for level in file_dictionary['graphLevels']:
    # print(level[0]['level'])
    levels[level[0]['level']] = level[0]['nodes']
file_dictionary['graphLevels'] = levels
print(levels)

print(file_dictionary)


