# Converter:
## Execution:
To run the script use the following command in your terminal:
```
python3 ConverterExpressionTreeEditor.py Example.json
```
Example.json and Example2.json are two files downloaded from the ExpressionTutor.
It's possible to call the script: without parameter (creation of a blank tree) or with a parameter (a .json file from 
Expression Tutor or a .tree file which recovers the state of an old execution of the script).

## Printed example:
The main idea of the script is to create a visualisation of a tree diagram that is accessible also for people with
impairments. An example of what is returned by the script:
```
type: treeDiagram, nodes: 10, maxDepth: 2, nodeStructure: {parentID; nodeID; childrenID; label, type, value}, connector: "#"
##########
@root {null;root;[1, 2];"# + #";Number;10}
@1 {root;1;[3, 4];"# - #";Boolean;true} {root;2;[5, 6];"# / #";Object;noValue}
@2 {1;3;null;"1";noType;noValue} {1;4;null;"2";noType;noValue} {2;5;null;"3";noType;noValue} {2;6;null;"# + #";noType;noValue}
@not_connected {null;7;null;"5";noType;Not connected} {null;8;null;"6";noType;Not connected} {null;9;null;"7";noType;Not connected}
```
Each time you run the script, a .tree file is generated that stores the last state of the modified diagram.

## List of the working commands:
The following commands are correctly implemented and are working inside the script, when the field "Insert command: " appears:
```
clear or c
quit or q
help or h
print
print --all 
print --tree
print --level [levelNumber]
print --node [nodeID]
print --description
print --notConnected or -nc
node --expand or -ex [nodeID or "all"]
node --scaleDown or -sd [nodeID or "all"]
node --create --l [label] --t [type]
node --connnect [parentNodeID]-[childNodeID]
node --root [nodeID]
export
export --json [filename.json]
```
