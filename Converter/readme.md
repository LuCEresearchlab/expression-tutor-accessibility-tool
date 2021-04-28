# Converter:
## Execution:
To run the script use the following command in your terminal:
```
python3 ConverterExpressionTreeEditor.py Example.json
```
Example.json and Example2.json are two files downloaded from the ExpressionTutor.

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

## List of the working commands:
The following commands are correctly implemented and are working inside the script, when the field "Insert command:" appears;
```
clear or c
quit or q
help or h
print --all
print --tree
print --level [levelNumber]
print --node [nodeID]
print --description
node --expand [nodeID or "all"]
node --scaleDown [nodeID or "all"]
```
