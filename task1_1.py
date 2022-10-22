from task0 import symbols, all_symbols, is_letter, is_atomic_sentence, preprocessing_data, sentence_OK

def main_connector_pos(string):
  # Returns the position of the main connector (the one inside only 1 parentesis). If no main connector, returns None
  open_parentheses = 0
  for i in range(len(string)):
    if open_parentheses == 1 and string[i] in symbols:
      return i
    if string[i] == "(":
      open_parentheses += 1
    elif string[i] == ")":
      open_parentheses -= 1
  return None
  
def divide_sentence(string, connector_pos):
  # Returns the two parts of the string separated by the main connector, excluding outer parentheses
  return string[1:connector_pos], string[connector_pos+1:-1]
  # ((p&q)|¬r)

def handle_not(string):
  # Returns the string without the outer ¬ (not). If no outer ¬, the string is returned
  if string[0] == "¬":
    return string[1:]
  else:
    return string


def main_task1_1():
  #string = input("Enter a sentence: ")
  string = "((p&q)|¬r)"
  string = preprocessing_data(string)
  connector_pos = main_connector_pos(string)
  print(divide_sentence(string,connector_pos))
  # input = "(p&&q)"
  # input = "((p || q) && ¬(p && q))"
  # input = "¬¬¬¬¬p"
  # input = "¬¬(¬¬(p && ¬q))"
  # input = "((p-> ¬r) && ¬¬(p || r)) <-> (p && ¬q)"
  # input = "p && q"
  # input = "(p)"
  # input = "(p -> q) || (p -> r)"
  # input = "p -> ((q || p) -> r)"
  # input = "(p -> ¬r) && ¬(¬(p || r) <-> (p && ¬ q))"
  # input = "(p -> ¬r) && ¬(¬(p || R) <-> (p && ¬ q))"
  # input = "p454"
  # input = "p123"
  # input = "123"
