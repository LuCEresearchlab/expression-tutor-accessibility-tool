#  Accessible Expression Tutor (AET):
##  Usage of the Accessible Expression Tutor:
To use the Accessible Expression Tutor you need first to clone this git repository:
```
https://github.com/LuCEresearchlab/expression-tutor-accessibility-tool
```
Then you should run the following command in your terminal to install the nearley.js parser (it requires the npm -node 
package manager for the JavaScript programming language):
```
$ npm install -g nearley
```
And then you should run the following command to install the Python requirements (it requires the pip - 
package-management system for the Python programming language):
```
$ pip install -r Converter/requirements.txt
```
Once these steps are done, you can run the Accessible Expression Tutor tool from the terminal. 
When the tool is launched from the terminal (with or without a parameter), the script does the conversion of the file 
given as a parameter or creates a new tree diagram and waits for a command given by the user to continue.
To run the script initially use one of the following command in your terminal, without parameter (creation of a blank 
tree) or with a parameter (a JSON file from Expression Tutor, a TREE file which recovers the state of an old execution
of the script or a TXT file that respects the grammar defined for this language):
```
python3 AET.py
python3 AET.py filename.tree
python3 AET.py filename.json
python3 AET.py filename.txt
```
In the folder "example" you can find the files: Example1.json, Example2.json and Example3.json which are three files 
downloaded from the Expression Tutor. There is also a file called Example2.tree which represents the last state of an 
older execution of the AET.
It's possible to call the script: 

## Printed example:
The main idea of the script is to create a visualisation of a tree diagram that is accessible also for people with
visually impairments. This is an example of what is returned by the script:
```
type: treeDiagram, nodes: 10, maxDepth: 2, nodeStructure: {parentID; nodeID; 
childrenID; label; type; value}, connector: "#"
-----------
@root {null;root;[1, 2];"# + #";Number;10} 
@1 {root;1;[3, 4];"# - #";Int;10} {root;2;[5, 6];"# / #";Object;noValue} 
@2 {1;3;null;"1";noType;noValue} {1;4;null;"2";noType;noValue}
{2;5;null;"3";noType;noValue} {2;6;null;"4";noType;noValue} 
@not_connected {null;7;null;"5";noType;NotConnected} 
{null;8;null;"6";noType;NotConnected} {null;9;null;"7";noType;NotConnected}
```
Each time you run the script, a .tree file is generated that stores the last state of the modified diagram.

## List of the commands:
You can use the following commands to explore, modify or analyze the tree diagram. You can input them when the field 
"Insert command: " appears:
```
clear or c
export
export --json or -j [filename.json]
export --txt [exportfile.txt]
help or h
load [filename.tree / filename.json / filename.txt / ""]
node --connnect or -con [parentNodeID]-[childNodeID]
node --create or -c --label or -l [label] --type or -t [type]
node --delete or -del [nodeID]
node --disconnect or -dis [parentNodeID]-[childNodeID]
node --expand or -ex [nodeID or "all"]
node --find or -f [argument]
node --modify or -m [nodeID] --label or -l [label] --type or -t [type]
node --root or -r [nodeID]
node --scaleDown or -sd [nodeID or "all"]
print
print --all or -a
print --description or -des
print --level or -lev [levelNumber] or [fromLevelNumber]-[toLevelNumber]
print --node or -n [nodeID]
print --notConnected or -nc
print --tree or -tr
quit or q
```

### Commands description

```
clear or c
```
The command clear (shortcut c) gives the possibility to "clean up" the terminal.
```
export or export --json or -j [filename.json]
`````
The command export or export with the attribute --json (shortcut -j), exports a JSON file of the tree diagram that is 
compatible with the Expression Tutor. If you use only export the script generates a new filename, if you use the 
attribute --json you can specify the filename of the new file.
```
export --txt [exportfile.txt]
```
The command export with the attribute --txt, exports a TXT file with the actual state of the diagram formatted as we 
normally see it in the terminal.
```
help or h
````
The command help (shortcut h) gives the list of all the possible commands.
```
load [filename.tree / filename.json / filename.txt / ""]
```
The command load loads an existing file of type JSON (from the expression tutor), TREE (last state of a tree diagram) 
or TXT (a file to parse with the nearley.js parser) into the program. If the command load is called without a filename,
 it creates a new empty tree diagram.
```
node --connnect or -con [parentNodeID]-[childNodeID]
```
The command node with the attribute --connect (shortcut -con), creates a new edge in the diagram between the node 
parentNodeID that is already in the diagram and the node childNodeID that is not yet connected.

```
node --create or -c --label or -l [label] --type or -t [type]
```
The command node with the attribute --create (shortcut -c), creates a new node in the diagram. With the attribute 
--label (shortcut -l) we can specify the label of the node and with the attribute --type (shortcut -t) we can specify 
the type of the node.
```
node --delete or -del [nodeID]
```
The command node with the attribute --delete (shortcut -del), deletes the node nodeID and if necessary disconnects the 
sub-nodes affected by this change.
```
node --disconnect or -dis [parentNodeID]-[childNodeID]
```
The command node with the attribute --disconnect (shortcut -dis), disconnects the two nodes parentNodeID and 
childNodeID that are connected in the diagram and removes also the connections of all the sub-nodes.
```
node --expand or -ex [nodeID or "all"]
```
The command node with the attribute --expand (shortcut -ex), makes the labels of the different values of the node 
nodeID visible. If we give as an argument "all", the command is applied to all the nodes of the tree.
```
node --find or -f [argument]
```
The command node with the attribute --find (shortcut -f), prints in the terminal the node IDs and the nodes that 
contain the argument (a letter, number, symbol or word) that is passed to the function in the label of the node.
```
node --modify or -m [nodeID] --label or -l [label] --type or -t [type]
````
The command node with the attribute --modify (shortcut -m), modifies the node nodeID in the diagram. With the 
attribute --label (shortcut -l) we can specify the new label of the node and with the attribute --type (shortcut -t) 
we can specify the new type of the node.
```
node --root or -r [nodeID]
```
The command node with the attribute --root (shortcut -r), changes the root node of the tree diagram to nodeID, all the 
other nodes are changed to status "NotConnected" and all the edges are deleted.
```
node --scaleDown or -sd [nodeID or "all"]
```
The command node with the attribute --scaleDown (shortcut -sd), hides the labels of the different values of the node 
nodeID. If we give as an argument "all", the command is applied to all the nodes of the tree.
```
print
print --all or -a
```
The command print or print with the attribute --all (shortcut -a), prints in the terminal the description of the tree 
diagram, a separation line and the tree diagram itself.
```
print --description or -des
```
The command print with the attribute --description (shortcut -des), prints in the terminal the description of the tree 
diagram.
```
print --level or -lev [levelNumber] or [fromLevelNumber]-[toLevelNumber]
```
The command print with the attribute --level (shortcut -lev), prints the level levelNumber of the tree diagram in the 
terminal if only one level is given as input. If a range of levels is given as input, it prints the range of levels.
```
print --node or -n [nodeID]
```
The command print with the attribute --node (shortcut -n), prints the node nodeID of the tree diagram in the terminal.
```
print --notConnected or -nc
```
The command print with the attribute --notConnected (shortcut -nc), prints the nodes that are not connected of the tree 
diagram in the terminal.
```
print --tree or -tr
```
The command print with the attribute --tree (shortcut -tr), prints in the terminal the tree diagram.
```
quit or q
```
The command quit (shortcut q) is used to terminate the script.
```
debugger
```
We implemented also the command debugger for debugging and developing purposes that can't be found in the official list 
of commands. You can use this command to print some helpful states and general information about the program to the 
terminal.
