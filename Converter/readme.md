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

## List of the commands:
You can use the following commands to explore, modify or analyze the tree diagram. You can input them when the field 
"Insert command: " appears:
```
clear or c
quit or q
help or h
print
print --all or -a
print --tree or -tr
print --level or -lev [levelNumber] or [fromLevelNumber]-[toLevelNumber]
print --node or -n [nodeID]
print --description or -des
print --notConnected or -nc
node --expand or -ex [nodeID or "all"]
node --scaleDown or -sd [nodeID or "all"]
node --create or -c --label or -l [label] --type or -t [type]
node --connnect or -con [parentNodeID]-[childNodeID]
node --disconnect or -dis [parentNodeID]-[childNodeID]
node --delete or -del [nodeID]
node --modify or -m [nodeID] --label or -l [label] --type or -t [type]
node --root or -r [nodeID]
node --find or -f [argument]
export
export --json or -j [filename.json]
export --txt [exportfile.txt]
load [filename.tree / filename.json / filename.txt / ""]
```

###Commands description

```
clear or c
```
The command clear (shortcut c) gives the possibility to "clean up" the terminal.

```
quit or q
`````
The command quit (shortcut q) is used to terminate the script.

```
help or h
```
The command help (shortcut h) gives the list of all the possible commands.

```
print
print --all or -a
````
The command print or print with the attribute --all (shortcut -a), prints in the terminal the description of the tree diagram, a separation line and the tree diagram itself.

```
print --tree or -tr
```
The command print with the attribute --tree (shortcut -tr), prints in the terminal the tree diagram.

```
print --description or -des
````
The command print with the attribute --description (shortcut -des), prints in the terminal the description of the tree diagram.

```
print --level or -lev [levelNumber] or [fromLevelNumber]-[toLevelNumber]
```
The command print with the attribute --level (shortcut -lev), prints the level levelNumber of the tree diagram in the terminal if only one level is given as input. If a range of levels is given as input, it prints the range of lines.
```
print --notConnected or -nc
````
The command print with the attribute --notConnected (shortcut -nc), prints the nodes that are not connected of the tree diagram in the terminal.

```
print --node or -n [nodeID]
```
The command print with the attribute --node (shortcut -n), prints the node nodeID of the tree diagram in the terminal.

```
node --create or -c --label or -l [label] --type or -t [type]
````
The command node with the attribute --create (shortcut -c), creates a new node in the diagram. With the attribute --label (shortcut -l) we can specify the label of the node and with the attribute --type (shortcut -t) we can specify the type of the node.

```
node --connnect or -con [parentNodeID]-[childNodeID]
```
The command node with the attribute --connect (shortcut -con), creates a new edge in the diagram between the node parentNodeID that is already in the diagram and the node childNodeID that is not yet connected.

```
node --disconnect or -dis [parentNodeID]-[childNodeID]
````
The command node with the attribute --disconnect (shortcut -dis), disconnects the two nodes parentNodeID and childNodeID that are connected in the diagram and removes also the connections of all the sub-nodes.

```
node --delete or -del [nodeID]
```
The command node with the attribute --delete (shortcut -del), deletes the node nodeID and if necessary disconnects the sub-nodes affected from this change.

```
node --modify or -m [nodeID] --label or -l [label] --type or -t [type]
```
The command node with the attribute --modify (shortcut -m), modifies the node nodeID in the diagram. With the attribute --label (shortcut -l) we can specify the new label of the node and with the attribute --type (shortcut -t) we can specify the new type of the node.

```
node --root or -r [nodeID]
```
The command node with the attribute --root (shortcut -r), changes the root node of the tree diagram to nodeID, all the other nodes are changed to "not connected" and all the edges are deleted.

```
node --find or -f [argument]
```
The command node with the attribute --find (shortcut -f), prints in the terminal the node ID's and the nodes that contains the argument (a letter, number, symbol or word) that is passed to the function.

```
node --expand or -ex [nodeID or "all"]
````
The command node with the attribute --expand (shortcut -ex), makes the labels of the different values of the node nodeID visible. If we give as argument "all", the command is applied to all the nodes of the tree.

```
node --scaleDown or -sd [nodeID or "all"]
```
The command node with the attribute --scaleDown (shortcut -sd), hides the labels of the different values of the node nodeID. If we give as argument "all", the command is applied to all the nodes of the tree.

```
export or export --json or -j [filename.json]
````
The command export or export with the attribute --json (shortcut -j), exports a json file of the tree diagram that is compatible with the expression tutor. If you use only export the script generates a filename, if you use he attribute --json you can specify the filename of the new file.

```
export --txt [exportfile.txt]
```
The command export with the attribute --txt, exports a txt file with the actual state of the diagram formatted as we normally see it in the terminal.

```
load [filename.tree / filename.json / filename.txt / ""]
```
The command load loads an existing file of type .json (from the expression tutor), .tree (last state of a tree diagram) or .txt (a file to parse with the nearley parser) into the program. If the command load is called without a filename, it creates a new empty tree diagram.

```
debugger
```
We implemented also the command debugger for debugging and developing purposes that can't be found in the official list of commands. You can use this command to print some helpful states and general information about the program to the terminal.