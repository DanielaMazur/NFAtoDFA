import networkx as nx
import plotly.graph_objects as go

vt = []
vn = []

grammar = dict()

def ParseGrammar():
  global vt, vn, grammar

  file = open("v12.txt", "r")
  fileContent = file.read()

  vn = (fileContent[fileContent.index("VN")+4:fileContent.index("\n")-2]).split(", ")
  vt = (fileContent[fileContent.index("VT")+4:fileContent.index("\n", fileContent.index("VT"))-2]).split(", ")

  grammarList = (fileContent[fileContent.index("P")+3:fileContent.index("\n", fileContent.index("P"))-1]).split(", ")

  for grammarRule in grammarList:
    grammarComponents = grammarRule.split(" - ")

    nextVertex = grammarComponents[1]
    for char in grammarComponents[1]:
      if char in vt:
        nextVertex = nextVertex.replace(char, "")

    if grammarComponents[0] not in grammar:
      grammar[grammarComponents[0]] = []

    grammar[grammarComponents[0]].append((grammarComponents[1][0], nextVertex))

def ConvertNDFAtoDFA():
  initialGrammar = list(grammar.items())

  #key is the non terminal symbol from which derives value
  #ex: q0 - aq1, here q0 is key and [(a, q1)] is value
  for key, value in initialGrammar:
    #initially grammar was grouped by nonTerminalSymbols
    #[('q0', [('a', 'q0'), ('a', 'q1')])]
    #groupByTerminalSymbol will store {'a': ['q0', 'q1']}
    groupByTerminalSymbol = GroupProductionsByTerminalSymbol(value)

    for terminalSymbolGroupedBy, nonTerminalSymbolList in groupByTerminalSymbol.items():
      newNonTerminalSymbol = JoinListIntoString(nonTerminalSymbolList)
      print("nonTerminalSymbolList", nonTerminalSymbolList)
      if newNonTerminalSymbol not in vn:
        #remove productions which with the same terminalSymbol goes to differnet states
        for nonTerminalSymbol in nonTerminalSymbolList:
          grammar[key].remove((terminalSymbolGroupedBy, nonTerminalSymbol))

        grammar[key].append((terminalSymbolGroupedBy, newNonTerminalSymbol))

        newProductions = []
        for nonTerminalSymbol in nonTerminalSymbolList:
          newProductions.extend(grammar[nonTerminalSymbol])

        groupedNewProductionsByNonTerminal = GroupProductionsByTerminalSymbol(newProductions)

        for nonTerminal, state in groupedNewProductionsByNonTerminal.items():
          newStateName = JoinListIntoString(state)
          if newNonTerminalSymbol not in grammar.keys():
             grammar[newNonTerminalSymbol] = []
             vn.append(newNonTerminalSymbol)

          grammar[newNonTerminalSymbol].append((nonTerminal, newStateName))


def GroupProductionsByTerminalSymbol(productions):
  groupByTerminalSymbol = dict()

  for terminalS, nonTerminalS in productions:
    if terminalS not in groupByTerminalSymbol:
      groupByTerminalSymbol[terminalS] = []
      
    groupByTerminalSymbol[terminalS].append(nonTerminalS)

  return groupByTerminalSymbol

def JoinListIntoString(initialList):
  return "".join(initialList)

def ShowGraph():
  G = nx.DiGraph()
  node_labels = []
  
  for nonTerminalSymbol in vn:
    if grammar[nonTerminalSymbol]:
      for adjacencyTuple in grammar[nonTerminalSymbol]:
        vertex =  adjacencyTuple[1] if adjacencyTuple[1] != None else "$"

        node_labels.append(((nonTerminalSymbol, vertex), adjacencyTuple[0]))
        G.add_edge(nonTerminalSymbol, vertex)

  layout = nx.circular_layout(G)

 # nx.draw(G, layout, with_labels=True, font_weight='bold', connectionstyle="arc3,rad=0.1")
  #nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=dict(node_labels), label_pos=0.2)
  edge_y = G.edges()


ParseGrammar();
ConvertNDFAtoDFA();
ShowGraph()
