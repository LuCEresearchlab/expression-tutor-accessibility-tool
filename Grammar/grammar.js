// Generated automatically by nearley, version 2.20.1
// http://github.com/Hardmath123/nearley
(function () {
function id(x) { return x[0]; }
var grammar = {
    Lexer: undefined,
    ParserRules: [
    {"name": "unsigned_int$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "unsigned_int$ebnf$1", "symbols": ["unsigned_int$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "unsigned_int", "symbols": ["unsigned_int$ebnf$1"], "postprocess": 
        function(d) {
            return parseInt(d[0].join(""));
        }
        },
    {"name": "int$ebnf$1$subexpression$1", "symbols": [{"literal":"-"}]},
    {"name": "int$ebnf$1$subexpression$1", "symbols": [{"literal":"+"}]},
    {"name": "int$ebnf$1", "symbols": ["int$ebnf$1$subexpression$1"], "postprocess": id},
    {"name": "int$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "int$ebnf$2", "symbols": [/[0-9]/]},
    {"name": "int$ebnf$2", "symbols": ["int$ebnf$2", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "int", "symbols": ["int$ebnf$1", "int$ebnf$2"], "postprocess": 
        function(d) {
            if (d[0]) {
                return parseInt(d[0][0]+d[1].join(""));
            } else {
                return parseInt(d[1].join(""));
            }
        }
        },
    {"name": "unsigned_decimal$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "unsigned_decimal$ebnf$1", "symbols": ["unsigned_decimal$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "unsigned_decimal$ebnf$2$subexpression$1$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "unsigned_decimal$ebnf$2$subexpression$1$ebnf$1", "symbols": ["unsigned_decimal$ebnf$2$subexpression$1$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "unsigned_decimal$ebnf$2$subexpression$1", "symbols": [{"literal":"."}, "unsigned_decimal$ebnf$2$subexpression$1$ebnf$1"]},
    {"name": "unsigned_decimal$ebnf$2", "symbols": ["unsigned_decimal$ebnf$2$subexpression$1"], "postprocess": id},
    {"name": "unsigned_decimal$ebnf$2", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "unsigned_decimal", "symbols": ["unsigned_decimal$ebnf$1", "unsigned_decimal$ebnf$2"], "postprocess": 
        function(d) {
            return parseFloat(
                d[0].join("") +
                (d[1] ? "."+d[1][1].join("") : "")
            );
        }
        },
    {"name": "decimal$ebnf$1", "symbols": [{"literal":"-"}], "postprocess": id},
    {"name": "decimal$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "decimal$ebnf$2", "symbols": [/[0-9]/]},
    {"name": "decimal$ebnf$2", "symbols": ["decimal$ebnf$2", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "decimal$ebnf$3$subexpression$1$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "decimal$ebnf$3$subexpression$1$ebnf$1", "symbols": ["decimal$ebnf$3$subexpression$1$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "decimal$ebnf$3$subexpression$1", "symbols": [{"literal":"."}, "decimal$ebnf$3$subexpression$1$ebnf$1"]},
    {"name": "decimal$ebnf$3", "symbols": ["decimal$ebnf$3$subexpression$1"], "postprocess": id},
    {"name": "decimal$ebnf$3", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "decimal", "symbols": ["decimal$ebnf$1", "decimal$ebnf$2", "decimal$ebnf$3"], "postprocess": 
        function(d) {
            return parseFloat(
                (d[0] || "") +
                d[1].join("") +
                (d[2] ? "."+d[2][1].join("") : "")
            );
        }
        },
    {"name": "percentage", "symbols": ["decimal", {"literal":"%"}], "postprocess": 
        function(d) {
            return d[0]/100;
        }
        },
    {"name": "jsonfloat$ebnf$1", "symbols": [{"literal":"-"}], "postprocess": id},
    {"name": "jsonfloat$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "jsonfloat$ebnf$2", "symbols": [/[0-9]/]},
    {"name": "jsonfloat$ebnf$2", "symbols": ["jsonfloat$ebnf$2", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "jsonfloat$ebnf$3$subexpression$1$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "jsonfloat$ebnf$3$subexpression$1$ebnf$1", "symbols": ["jsonfloat$ebnf$3$subexpression$1$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "jsonfloat$ebnf$3$subexpression$1", "symbols": [{"literal":"."}, "jsonfloat$ebnf$3$subexpression$1$ebnf$1"]},
    {"name": "jsonfloat$ebnf$3", "symbols": ["jsonfloat$ebnf$3$subexpression$1"], "postprocess": id},
    {"name": "jsonfloat$ebnf$3", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "jsonfloat$ebnf$4$subexpression$1$ebnf$1", "symbols": [/[+-]/], "postprocess": id},
    {"name": "jsonfloat$ebnf$4$subexpression$1$ebnf$1", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "jsonfloat$ebnf$4$subexpression$1$ebnf$2", "symbols": [/[0-9]/]},
    {"name": "jsonfloat$ebnf$4$subexpression$1$ebnf$2", "symbols": ["jsonfloat$ebnf$4$subexpression$1$ebnf$2", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "jsonfloat$ebnf$4$subexpression$1", "symbols": [/[eE]/, "jsonfloat$ebnf$4$subexpression$1$ebnf$1", "jsonfloat$ebnf$4$subexpression$1$ebnf$2"]},
    {"name": "jsonfloat$ebnf$4", "symbols": ["jsonfloat$ebnf$4$subexpression$1"], "postprocess": id},
    {"name": "jsonfloat$ebnf$4", "symbols": [], "postprocess": function(d) {return null;}},
    {"name": "jsonfloat", "symbols": ["jsonfloat$ebnf$1", "jsonfloat$ebnf$2", "jsonfloat$ebnf$3", "jsonfloat$ebnf$4"], "postprocess": 
        function(d) {
            return parseFloat(
                (d[0] || "") +
                d[1].join("") +
                (d[2] ? "."+d[2][1].join("") : "") +
                (d[3] ? "e" + (d[3][1] || "+") + d[3][2].join("") : "")
            );
        }
        },
    {"name": "_$ebnf$1", "symbols": []},
    {"name": "_$ebnf$1", "symbols": ["_$ebnf$1", "wschar"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "_", "symbols": ["_$ebnf$1"], "postprocess": function(d) {return null;}},
    {"name": "__$ebnf$1", "symbols": ["wschar"]},
    {"name": "__$ebnf$1", "symbols": ["__$ebnf$1", "wschar"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "__", "symbols": ["__$ebnf$1"], "postprocess": function(d) {return null;}},
    {"name": "wschar", "symbols": [/[ \t\n\v\f]/], "postprocess": id},
    {"name": "dqstring$ebnf$1", "symbols": []},
    {"name": "dqstring$ebnf$1", "symbols": ["dqstring$ebnf$1", "dstrchar"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "dqstring", "symbols": [{"literal":"\""}, "dqstring$ebnf$1", {"literal":"\""}], "postprocess": function(d) {return d[1].join(""); }},
    {"name": "sqstring$ebnf$1", "symbols": []},
    {"name": "sqstring$ebnf$1", "symbols": ["sqstring$ebnf$1", "sstrchar"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "sqstring", "symbols": [{"literal":"'"}, "sqstring$ebnf$1", {"literal":"'"}], "postprocess": function(d) {return d[1].join(""); }},
    {"name": "btstring$ebnf$1", "symbols": []},
    {"name": "btstring$ebnf$1", "symbols": ["btstring$ebnf$1", /[^`]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "btstring", "symbols": [{"literal":"`"}, "btstring$ebnf$1", {"literal":"`"}], "postprocess": function(d) {return d[1].join(""); }},
    {"name": "dstrchar", "symbols": [/[^\\"\n]/], "postprocess": id},
    {"name": "dstrchar", "symbols": [{"literal":"\\"}, "strescape"], "postprocess": 
        function(d) {
            return JSON.parse("\""+d.join("")+"\"");
        }
        },
    {"name": "sstrchar", "symbols": [/[^\\'\n]/], "postprocess": id},
    {"name": "sstrchar", "symbols": [{"literal":"\\"}, "strescape"], "postprocess": function(d) { return JSON.parse("\""+d.join("")+"\""); }},
    {"name": "sstrchar$string$1", "symbols": [{"literal":"\\"}, {"literal":"'"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "sstrchar", "symbols": ["sstrchar$string$1"], "postprocess": function(d) {return "'"; }},
    {"name": "strescape", "symbols": [/["\\\/bfnrt]/], "postprocess": id},
    {"name": "strescape", "symbols": [{"literal":"u"}, /[a-fA-F0-9]/, /[a-fA-F0-9]/, /[a-fA-F0-9]/, /[a-fA-F0-9]/], "postprocess": 
        function(d) {
            return d.join("");
        }
        },
    {"name": "graph", "symbols": ["graphDescription", "graphSeparator", "graphLevels"], "postprocess": function(d) {return {description: d[0], graphLevels: d[2]}}},
    {"name": "graphSeparator$ebnf$1$subexpression$1", "symbols": [{"literal":"-"}]},
    {"name": "graphSeparator$ebnf$1", "symbols": ["graphSeparator$ebnf$1$subexpression$1"]},
    {"name": "graphSeparator$ebnf$1$subexpression$2", "symbols": [{"literal":"-"}]},
    {"name": "graphSeparator$ebnf$1", "symbols": ["graphSeparator$ebnf$1", "graphSeparator$ebnf$1$subexpression$2"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "graphSeparator", "symbols": ["graphSeparator$ebnf$1"]},
    {"name": "graphDescription$string$1", "symbols": [{"literal":"t"}, {"literal":"y"}, {"literal":"p"}, {"literal":"e"}, {"literal":":"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphDescription$string$2", "symbols": [{"literal":","}, {"literal":" "}, {"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"s"}, {"literal":":"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphDescription$string$3", "symbols": [{"literal":","}, {"literal":" "}, {"literal":"m"}, {"literal":"a"}, {"literal":"x"}, {"literal":"D"}, {"literal":"e"}, {"literal":"p"}, {"literal":"t"}, {"literal":"h"}, {"literal":":"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphDescription$string$4", "symbols": [{"literal":","}, {"literal":" "}, {"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"S"}, {"literal":"t"}, {"literal":"r"}, {"literal":"u"}, {"literal":"c"}, {"literal":"t"}, {"literal":"u"}, {"literal":"r"}, {"literal":"e"}, {"literal":":"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphDescription$string$5", "symbols": [{"literal":","}, {"literal":" "}, {"literal":"c"}, {"literal":"o"}, {"literal":"n"}, {"literal":"n"}, {"literal":"e"}, {"literal":"c"}, {"literal":"t"}, {"literal":"o"}, {"literal":"r"}, {"literal":":"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphDescription", "symbols": ["_", "graphDescription$string$1", "_", "graphType", "_", "graphDescription$string$2", "_", "nodeNumber", "_", "graphDescription$string$3", "_", "maxDepth", "_", "graphDescription$string$4", "_", "nodeStructure", "_", "graphDescription$string$5", "_", "connector", "_"], "postprocess": function(d) {return {type: d[3], nodeNumber: d[7], maxDepth: d[11], nodeStructure: d[15], connector: d[19]}}},
    {"name": "graphType$string$1", "symbols": [{"literal":"t"}, {"literal":"r"}, {"literal":"e"}, {"literal":"e"}, {"literal":"D"}, {"literal":"i"}, {"literal":"a"}, {"literal":"g"}, {"literal":"r"}, {"literal":"a"}, {"literal":"m"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "graphType", "symbols": ["graphType$string$1"], "postprocess": id},
    {"name": "nodeNumber", "symbols": ["unsigned_int"], "postprocess": id},
    {"name": "maxDepth", "symbols": ["unsigned_int"], "postprocess": id},
    {"name": "nodeStructure$string$1", "symbols": [{"literal":"{"}, {"literal":"p"}, {"literal":"a"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"t"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$2", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$3", "symbols": [{"literal":"c"}, {"literal":"h"}, {"literal":"i"}, {"literal":"l"}, {"literal":"d"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"I"}, {"literal":"D"}, {"literal":"}"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure", "symbols": ["nodeStructure$string$1", "_", {"literal":";"}, "_", "nodeStructure$string$2", "_", {"literal":";"}, "_", "nodeStructure$string$3"], "postprocess": function (d) {return "{parentID; nodeID; childrenID}"}},
    {"name": "nodeStructure$string$4", "symbols": [{"literal":"{"}, {"literal":"p"}, {"literal":"a"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"t"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$5", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$6", "symbols": [{"literal":"c"}, {"literal":"h"}, {"literal":"i"}, {"literal":"l"}, {"literal":"d"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$7", "symbols": [{"literal":"l"}, {"literal":"a"}, {"literal":"b"}, {"literal":"e"}, {"literal":"l"}, {"literal":"}"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure", "symbols": ["nodeStructure$string$4", "_", {"literal":";"}, "_", "nodeStructure$string$5", "_", {"literal":";"}, "_", "nodeStructure$string$6", "_", {"literal":";"}, "_", "nodeStructure$string$7"], "postprocess": function (d) {return "{parentID; nodeID; childrenID; label}"}},
    {"name": "nodeStructure$string$8", "symbols": [{"literal":"{"}, {"literal":"p"}, {"literal":"a"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"t"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$9", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$10", "symbols": [{"literal":"c"}, {"literal":"h"}, {"literal":"i"}, {"literal":"l"}, {"literal":"d"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$11", "symbols": [{"literal":"l"}, {"literal":"a"}, {"literal":"b"}, {"literal":"e"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$12", "symbols": [{"literal":"t"}, {"literal":"y"}, {"literal":"p"}, {"literal":"e"}, {"literal":"}"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure", "symbols": ["nodeStructure$string$8", "_", {"literal":";"}, "_", "nodeStructure$string$9", "_", {"literal":";"}, "_", "nodeStructure$string$10", "_", {"literal":";"}, "_", "nodeStructure$string$11", "_", {"literal":";"}, "_", "nodeStructure$string$12"], "postprocess": function (d) {return "{parentID; nodeID; childrenID; label; type}"}},
    {"name": "nodeStructure$string$13", "symbols": [{"literal":"{"}, {"literal":"p"}, {"literal":"a"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"t"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$14", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$15", "symbols": [{"literal":"c"}, {"literal":"h"}, {"literal":"i"}, {"literal":"l"}, {"literal":"d"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$16", "symbols": [{"literal":"l"}, {"literal":"a"}, {"literal":"b"}, {"literal":"e"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$17", "symbols": [{"literal":"t"}, {"literal":"y"}, {"literal":"p"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure$string$18", "symbols": [{"literal":"v"}, {"literal":"a"}, {"literal":"l"}, {"literal":"u"}, {"literal":"e"}, {"literal":"}"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeStructure", "symbols": ["nodeStructure$string$13", "_", {"literal":";"}, "_", "nodeStructure$string$14", "_", {"literal":";"}, "_", "nodeStructure$string$15", "_", {"literal":";"}, "_", "nodeStructure$string$16", "_", {"literal":";"}, "_", "nodeStructure$string$17", "_", {"literal":";"}, "_", "nodeStructure$string$18"], "postprocess": function (d) {return "{parentID; nodeID; childrenID; label; type; value}"}},
    {"name": "connector", "symbols": ["dqstring"], "postprocess": id},
    {"name": "graphLevels$ebnf$1", "symbols": []},
    {"name": "graphLevels$ebnf$1$subexpression$1", "symbols": ["levelDescription"]},
    {"name": "graphLevels$ebnf$1", "symbols": ["graphLevels$ebnf$1", "graphLevels$ebnf$1$subexpression$1"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "graphLevels", "symbols": ["graphLevels$ebnf$1"], "postprocess": function (d) {return d[0]}},
    {"name": "levelDescription$ebnf$1$subexpression$1", "symbols": ["treeDiagramNode"]},
    {"name": "levelDescription$ebnf$1", "symbols": ["levelDescription$ebnf$1$subexpression$1"]},
    {"name": "levelDescription$ebnf$1$subexpression$2", "symbols": ["treeDiagramNode"]},
    {"name": "levelDescription$ebnf$1", "symbols": ["levelDescription$ebnf$1", "levelDescription$ebnf$1$subexpression$2"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "levelDescription", "symbols": ["_", "depthLevel", "levelDescription$ebnf$1"], "postprocess": function (d) {return {level: d[1], nodes: d[2]}}},
    {"name": "depthLevel", "symbols": [{"literal":"@"}, "unsigned_int"], "postprocess": function (d) {return d[1]}},
    {"name": "depthLevel$string$1", "symbols": [{"literal":"@"}, {"literal":"r"}, {"literal":"o"}, {"literal":"o"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "depthLevel", "symbols": ["depthLevel$string$1"], "postprocess": function (d) {return "root"}},
    {"name": "depthLevel$string$2", "symbols": [{"literal":"@"}, {"literal":"n"}, {"literal":"o"}, {"literal":"t"}, {"literal":"_"}, {"literal":"c"}, {"literal":"o"}, {"literal":"n"}, {"literal":"n"}, {"literal":"e"}, {"literal":"c"}, {"literal":"t"}, {"literal":"e"}, {"literal":"d"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "depthLevel", "symbols": ["depthLevel$string$2"], "postprocess": function (d) {return "not_connected"}},
    {"name": "treeDiagramNode", "symbols": ["_", {"literal":"{"}, "_", "parentDescription", "_", {"literal":";"}, "_", "nodeDescription", "_", {"literal":";"}, "_", "childrenDescription", "_", {"literal":";"}, "_", "nodeLabelDescription", "_", "optionalDescriptions", "_", {"literal":"}"}], "postprocess":  function (d) {return {parentID: d[3], nodeID: d[7], childrenID: d[11], nodeLabel: d[15],
        nodeOptionals: d[17]}} },
    {"name": "parentDescription$string$1", "symbols": [{"literal":"p"}, {"literal":"a"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"t"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "parentDescription", "symbols": ["parentDescription$string$1", "_", {"literal":":"}, "_", "unsigned_int"], "postprocess": function (d) {return d[4]}},
    {"name": "parentDescription", "symbols": ["unsigned_int"], "postprocess": id},
    {"name": "parentDescription$string$2", "symbols": [{"literal":"n"}, {"literal":"u"}, {"literal":"l"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "parentDescription", "symbols": ["parentDescription$string$2"], "postprocess": id},
    {"name": "parentDescription$string$3", "symbols": [{"literal":"r"}, {"literal":"o"}, {"literal":"o"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "parentDescription", "symbols": ["parentDescription$string$3"], "postprocess": id},
    {"name": "nodeDescription$string$1", "symbols": [{"literal":"n"}, {"literal":"o"}, {"literal":"d"}, {"literal":"e"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeDescription", "symbols": ["nodeDescription$string$1", "_", {"literal":":"}, "_", "unsigned_int"], "postprocess": function (d) {return d[4]}},
    {"name": "nodeDescription", "symbols": ["unsigned_int"], "postprocess": id},
    {"name": "nodeDescription$string$2", "symbols": [{"literal":"r"}, {"literal":"o"}, {"literal":"o"}, {"literal":"t"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeDescription", "symbols": ["nodeDescription$string$2"], "postprocess": id},
    {"name": "childrenDescription$string$1", "symbols": [{"literal":"c"}, {"literal":"h"}, {"literal":"i"}, {"literal":"l"}, {"literal":"d"}, {"literal":"r"}, {"literal":"e"}, {"literal":"n"}, {"literal":"I"}, {"literal":"D"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "childrenDescription", "symbols": ["childrenDescription$string$1", "_", {"literal":":"}, "_", "childrenID"], "postprocess": function (d) {return d[4]}},
    {"name": "childrenDescription", "symbols": ["childrenID"], "postprocess": id},
    {"name": "childrenID", "symbols": ["array"], "postprocess": function (d) {return d}},
    {"name": "childrenID", "symbols": ["unsigned_int"], "postprocess": id},
    {"name": "childrenID$string$1", "symbols": [{"literal":"n"}, {"literal":"u"}, {"literal":"l"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "childrenID", "symbols": ["childrenID$string$1"], "postprocess": id},
    {"name": "array$ebnf$1$subexpression$1", "symbols": ["arrayOfInts"]},
    {"name": "array$ebnf$1", "symbols": ["array$ebnf$1$subexpression$1"]},
    {"name": "array$ebnf$1$subexpression$2", "symbols": ["arrayOfInts"]},
    {"name": "array$ebnf$1", "symbols": ["array$ebnf$1", "array$ebnf$1$subexpression$2"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "array", "symbols": [{"literal":"["}, "array$ebnf$1", {"literal":"]"}], "postprocess": function (d) {return d[1]}},
    {"name": "arrayOfInts$ebnf$1", "symbols": []},
    {"name": "arrayOfInts$ebnf$1$subexpression$1", "symbols": [{"literal":","}]},
    {"name": "arrayOfInts$ebnf$1", "symbols": ["arrayOfInts$ebnf$1", "arrayOfInts$ebnf$1$subexpression$1"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "arrayOfInts", "symbols": ["_", "unsigned_int", "_", "arrayOfInts$ebnf$1"], "postprocess": function (d) {return d[1]}},
    {"name": "nodeLabelDescription$string$1", "symbols": [{"literal":"l"}, {"literal":"a"}, {"literal":"b"}, {"literal":"e"}, {"literal":"l"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeLabelDescription", "symbols": ["nodeLabelDescription$string$1", "_", {"literal":":"}, "_", "dqstring"], "postprocess": function (d) {return d[4]}},
    {"name": "nodeLabelDescription", "symbols": ["dqstring"], "postprocess": id},
    {"name": "optionalDescriptions", "symbols": [{"literal":";"}, "_", "nodeTypeDescription", "_", {"literal":";"}, "_", "nodeValueDescription"], "postprocess": function (d) {return {nodeType:d[2], nodeValue:d[6]}}},
    {"name": "optionalDescriptions", "symbols": [], "postprocess": id},
    {"name": "nodeTypeDescription$string$1", "symbols": [{"literal":"t"}, {"literal":"y"}, {"literal":"p"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeTypeDescription", "symbols": ["nodeTypeDescription$string$1", "_", {"literal":":"}, "_", "string"], "postprocess": function (d) {return d[4]}},
    {"name": "nodeTypeDescription", "symbols": ["string"], "postprocess": id},
    {"name": "nodeValueDescription$string$1", "symbols": [{"literal":"v"}, {"literal":"a"}, {"literal":"l"}, {"literal":"u"}, {"literal":"e"}], "postprocess": function joiner(d) {return d.join('');}},
    {"name": "nodeValueDescription", "symbols": ["nodeValueDescription$string$1", "_", {"literal":":"}, "_", "string"], "postprocess": function (d) {return d[4]}},
    {"name": "nodeValueDescription", "symbols": ["string"], "postprocess": id},
    {"name": "nodeValueDescription", "symbols": ["dqstring"], "postprocess": id},
    {"name": "string$ebnf$1", "symbols": []},
    {"name": "string$ebnf$1", "symbols": ["string$ebnf$1", "stringChar"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "string", "symbols": ["string$ebnf$1"], "postprocess": function(d) {return d[0].join(""); }},
    {"name": "stringChar", "symbols": [/[a-zA-Z0-9]/], "postprocess": id}
]
  , ParserStart: "graph"
}
if (typeof module !== 'undefined'&& typeof module.exports !== 'undefined') {
   module.exports = grammar;
} else {
   window.grammar = grammar;
}
})();
