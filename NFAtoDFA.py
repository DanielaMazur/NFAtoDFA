from texttable import Texttable

SUM_SYMBOL = "Î£"
DELTA = "áºŸ"

finalState = ''

vt = []
vn = []

grammar = dict()

#new states derived from NFA
newStates = []

def ParseGrammar():
  global vt, vn, grammar, finalState

  file = open("varianta21.txt", "r")
  fileContent = file.read()

  vn = (fileContent[fileContent.index("Q")+6:fileContent.index("\n")-2]).split(", ")
  vt = (fileContent[fileContent.index(SUM_SYMBOL)+6:fileContent.index("\n", fileContent.index(SUM_SYMBOL))-3]).strip().split(", ")

  finalState = fileContent[fileContent.index('F')+ 5 :fileContent.index("\n", fileContent.index('F'))-2]
  
  transitionFunction = fileContent[fileContent.index(DELTA):].split("\n")
  for function in transitionFunction:
    #production is of the form (q0, a) = q1,
    production = function.replace(DELTA, "").strip()

    #vertex - q0, tranzitionSymbol - a
    vertex, tranzitionSymbol = production[1:production.index(")")].split(", ")
    #derivedVertex q1
    derivedVertex = production[production.index("=")+1:len(production)-1].strip()
    
    if vertex not in grammar:
      grammar[vertex] = []

    #if there already is a production with this tranzition symbol then concatenate final state
    isProductionExisting = False

    for production in grammar[vertex]:
      if production[0] == tranzitionSymbol:
        orderedNewStateName = "".join(GetSubstates(production[1] + derivedVertex))
        grammar[vertex][grammar[vertex].index(production)] = (tranzitionSymbol, orderedNewStateName)
        newStates.append(orderedNewStateName)
        isProductionExisting = True

    if not isProductionExisting:
      grammar[vertex].append((tranzitionSymbol, derivedVertex))


def NFAtoDFA():
  while len(newStates):
    grammar[newStates[0]] = []
    vn.append(newStates[0])

    subStates = GetSubstates(newStates[0]) 

    for subState in subStates:
      isProductionExisting = False

      for production in grammar[subState]:
        for newProduction in grammar[newStates[0]]:
          
          if newProduction[0] == production[0]:
            newProductionSubstates = GetSubstates(newProduction[1])
            prevProductionSubstates = GetSubstates(production[1])

            #replace repreting states with empty string
            for prevSubstate in prevProductionSubstates:
              if prevSubstate in newProductionSubstates:
                production = (production[1], production[1].replace(prevSubstate, ""))

            orderedNewStateName = "".join(GetSubstates(newProduction[1] + production[1]))
            grammar[newStates[0]][grammar[newStates[0]].index(newProduction)] = (production[0], orderedNewStateName)

            isProductionExisting = True
            break

      #initiate production if no rule for that terminal symbol is defined yet
      if subState in grammar and not isProductionExisting:
        grammar[newStates[0]].extend(grammar[subState])

    #check for new states
    for production in grammar[newStates[0]]:
      if production[1] not in vn:
        newStates.append(production[1])

    newStates.remove(newStates[0])

#from q2q1q3 generates ['q1', 'q2', 'q3'] also order them 
def GetSubstates(state):
  substates = ["q"+stateNumber for stateNumber in filter(None, state.split("q"))]
  substates.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
  
  return substates

def PrintTable(grammar):
  t = Texttable()

  tableHeaders = vt.copy()
  tableHeaders.insert(0, "")
  t.add_row(tableHeaders)

  for state in vn:
    row = []

    if state == 'q0':
      row.append("-> "+state)
    elif finalState in state:
      row.append("*"+state)
    else:
      row.append(state)
    
    for terminalSymbol in vt:
      currentStateTuple = [item for item in grammar[state.strip()] if item[0] == terminalSymbol]
      if len(currentStateTuple) > 0:
        row.append(currentStateTuple[0][1])
      else:
        row.append("-")
    t.add_row(row)
  
  print(t.draw())

ParseGrammar()
NFAtoDFA()
PrintTable(grammar)
