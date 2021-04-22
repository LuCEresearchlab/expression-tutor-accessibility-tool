# This is a Grammar for describing tree diagrams.
@builtin "number.ne"
@builtin "whitespace.ne"
@builtin "string.ne"

# A diagram is composed of a description and the the list of levels where the nodes are contained, the description
# and the list are separated by a separator.
graph -> graphDescription graphSeparator graphLevels {% function(d) {return {description: d[0], graphLevels: d[2]}} %}

# The separator that we use is a repetition of hash symbols.
graphSeparator -> ("#"):+

# The graph description gives some main informations about it, so that the user can imagine what he should expect.
# In detail it tells the user the graph type, the number of nodes that are in the diagram, the maximal depth of the
# diagram and the structure of the nodes present in the diagram.
graphDescription -> _ "type:" _ graphType _ ", nodes:" _ nodeNumber _ ", maxDepth:" _ maxDepth _
					", nodeStructure:" _ nodeStructure _
					{% function(d) {return {type: d[3], nodeNumber: d[7], maxDepth: d[11], nodeStructure: d[15]}} %}

# graphType describes the type of diagram that we are dealing with.
graphType -> "treeDiagram" {% id %}

# nodeNumber is the number of nodes that are in the diagram (defined by a unsigned int).
nodeNumber -> unsigned_int {% id %}

# maxDepth is the maximal depth of the diagram (defined by a unsigned int).
maxDepth -> unsigned_int {% id %}

# The node structure can be different, depending on the usage of the tree diagram.
nodeStructure -> "{parentID" _ ";" _ "nodeID" _ ";" _ "childrenID}"
				{% function (d) {return "{parentID; nodeID; childrenID}"} %}
				| "{parentID" _ ";" _ "nodeID" _ ";" _ "childrenID" _ ";" _ "label}"
				{% function (d) {return "{parentID; nodeID; childrenID; label}"} %}
				| "{parentID" _ ";" _ "nodeID" _ ";" _ "childrenID" _ ";" _ "label" _ ";" _ "type}"
				{% function (d) {return "{parentID; nodeID; childrenID; label; type}"} %}
				| "{parentID" _ ";" _ "nodeID" _ ";" _ "childrenID" _ ";" _ "label" _ ";" _ "type" _ ";" _ "value}"
				{% function (d) {return "{parentID; nodeID; childrenID; label; type; value}"} %}

# graphLevel contains the information about the nodes
graphLevels -> _ (levelDescription):* {% function (d) {return d[1]} %}

# levelDescriptions tells us the depth level we are at and the nodes present in that level.
levelDescription -> depthLevel (treeDiagramNode):+  {% function (d) {return {level: d[0], nodes: d[1]}} %}

# depthLevel tells us the depth level we are at, example @2 means level 2.
depthLevel -> "@" unsigned_int {% function (d) {return d[1]} %}

# The node structure can be different, depending on the usage of the tree diagram, we should recognise also the
# "exploded" nodes and we have some components that are optional and not required in all nodes.
treeDiagramNode ->
				_ "{" _ parentDescription _ ";" _ nodeDescription _ ";" _ childrenDescription _ ";"
				_ nodeLabelDescription _ optionalDescriptions _ "}" _
				{% function (d) {return {parentID: d[3], nodeID: d[7], childrenID: d[11], nodeLabel: d[15],
				nodeOptionals: d[17]}} %}

# parentDescription is the unique ID (defined by a unsigned int) that describes the parent node of the actual node,
# it can also be the string "root" if the parent node is the root of the tree or null if the node has no parent node.
parentDescription -> "parentID" _ ":" _ unsigned_int {% function (d) {return d[4]} %}
					| unsigned_int {% id %}
					| "null" {% id %}
					| "root" {% id %}

# nodeDescription is the unique ID (defined by a unsigned int) that describes the actual node, it can also be the
# string "root" if the actual node is the root of the tree.
nodeDescription -> "nodeID" _ ":" _ unsigned_int {% function (d) {return d[4]} %}
					| unsigned_int {% id %}
					| "root" {% id %}

# childrenDescription is the unique ID or an array of unique IDs that describes the child or children of the actual
# node.
childrenDescription -> "childrenID" _ ":" _ childrenID {% function (d) {return d[4]} %}
					| childrenID {% id %}

# childrenID can be null if the actual node has no children, else an unsigned int if the node has only one child or
# an array of IDs in case the node has many children.
childrenID -> array {% function (d) {return d} %}
			| unsigned_int {% id %}
			| "null" {% id %}

# array is defined by to square brackets.
array -> "[" (arrayOfInts):+ "]" {% function (d) {return d[1]} %}

# arrayOfInts are the IDs of the children present in the array.
arrayOfInts -> _ unsigned_int _ (","):* {% function (d) {return d[1]} %}

# nodeLabelDescription is the value that is displayed in the node (defined by a dqstring - double quote string).
nodeLabelDescription -> "label" _ ":" _ dqstring {% function (d) {return d[4]} %}
						| dqstring {% id %}

# optionalDescriptions contains the optional parameters for a node: nodeTypeDescription and nodeValueDescription.
optionalDescriptions -> ";" _ nodeTypeDescription _ ";" _ nodeValueDescription
						{% function (d) {return {nodeType:d[2], nodeValue:d[6]}} %}
						| null {% id %}

# nodeTypeDescription indicates the type of a node (defined by a string without quotes).
nodeTypeDescription -> "type" _ ":" _ string {% function (d) {return d[4]} %}
						| string {% id %}

# nodeValueDescription indicates the value of a node as a string or dqstring. For example if we have 3 nodes that
# are showing the multiplication of 2 numbers (1)(*)(2) the value of the second node is 2.
nodeValueDescription -> "value" _ ":" _ string {% function (d) {return d[4]} %}
						| string {% id %}
						| dqstring {% id %}

# Definition of string - multiple parsed characters joined to a string.
string -> stringChar:* {% function(d) {return d[0].join(""); } %}

# The accepted characters for a string.
stringChar -> [a-zA-Z0-9] {% id %}
