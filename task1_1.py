from task0 import symbols, all_symbols, is_letter, is_atomic_sentence, preprocessing_data, sentence_OK

class Sentence:
  def __init__(self,value,parent):
    self.parent = parent
    self.children = []
    self.value = value
  
  def add_children(self,list_of_children):
    for string in list_of_children:
      self.children.append(Sentence(string,parent=self))

  def get_parent(self):
    return self.parent

  def get_value(self):
    return self.value

  def get_children(self):
    return self.children

  def __str__(self):
    return(self.value)
  
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
  # Returns the 2 parts of the string separated by a connector, excluding outer parentheses
  return string[1:connector_pos], string[connector_pos+1:-1]

def divide_by_main_connector(string):
  # Returns a list of the 2 parts divided by the main connector
  connector_pos = main_connector_pos(string)
  if connector_pos == None:
    return string
  return list(divide_sentence(string, connector_pos))

def handle_not(string):
  # Returns the string without the outer ¬ (not). If no outer ¬, the string is returned
  if string[0] == "¬":
    return string[1:]
  else:
    return string

def sentences_are_atomic(list_sentences):
  for c in list_sentences:
    if not is_atomic_sentence(c.get_value()):
      return False
  return True  

def syntactic_tree(string_founder):
  # Builds recursively the syntactic tree. 
  a = Sentence(string_founder, parent=None)
  list_sentences = [a]
  
  while not sentences_are_atomic(list_sentences):
    list_sentences_new = []
    for sentence in list_sentences:
      divided_string = divide_by_main_connector(sentence.value)
      if divided_string == sentence.value:
        alt_string = handle_not(sentence.value)
        sentence.add_children([alt_string])
      else:
        sentence.add_children(divided_string)
      list_sentences_new.extend(sentence.get_children())
    list_sentences = list_sentences_new[:]
#

def print_tree(tree_lst):
  # Prints recursively the syntactic tree.
  pass

def main_task1_1():
  #string = input("Enter a sentence: ")
  string = "((p&q)|¬r)"
  syntactic_tree(string)
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



#Pseudocode




a = Sentence("((p&q)|¬r)",parent=None)
a.add_children(["(p&q)","¬r"])








