from task0 import symbols, all_symbols, is_letter, is_atomic_sentence, preprocessing_data, sentence_OK

class Sentence:
  def __init__(self,value,parent=None):
    # Each sentence object has 3 parameters: the sentence as a string (value), the sentence of which it comes (parent) and the subsentences that can be formed from the sentences (children)
    self.value = value
    self.parent = parent
    self.children = []
  
  def add_children(self,list_of_children):
    for string in list_of_children:
      self.children.append(Sentence(string,parent=self))

  def get_value(self):
    return self.value
    
  def get_parent(self):
    return self.parent

  def get_children(self):
    return self.children

  def __str__(self):
    return self.value
  
def main_connector_pos(string):
  # Returns the position of the main connector (the one inside only 1 parentesis). If no main connector, or first character is "¬", returns None
  if string[0] == "¬":
    return None
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
  elif len(string) >= 2 and string[1] == "¬":
    return string[2:-1]
  else:
    return string

def sentences_are_atomic(list_sentences):
  # Returns True if any of the sentences in the list is atomic
  for sentence in list_sentences:
    if not is_atomic_sentence(sentence.get_value()):
      return False
  return True  

def syntactic_tree(string_founder,list_sentences):
  # Builds the syntactic tree layer by layer (not branch by branch).
  while not sentences_are_atomic(list_sentences): # repeat until all sentences are atomic
    list_sentences_cousins = [] # list to save, as a layer, the children made at every branch
    for sentence in list_sentences:
      divided_string = divide_by_main_connector(sentence.value) # list of the 2 parts of the divided string
      error = "" in divided_string and type(divided_string) == list # If there is "" in divided_string, this means that sentence was not OK
      if error:
        list_sentences_cousins.extend([sentence])
      else:
        if divided_string == sentence.value: # if the sentence has not changed
          alt_string = handle_not(sentence.value) # alternative string without the ¬
          sentence.add_children([alt_string])
        else:
          sentence.add_children(divided_string)
        list_sentences_cousins.extend(sentence.get_children()) # add children to list of cousins (otherwise, we end up only with the children of one of the parents, i.e. only the last branch would be saved)
    # update the list with the list of cousins, so the process can be repeated again with each cousin as a parent
    # Note: we can't do "list_sentences = list_sentences_cousins.copy()" because as lists are mutable, we would lose the adress of the original list by using the "=" operator.
    list_sentences.clear()
    list_sentences.extend(list_sentences_cousins)
    assert (not error), "The expression " + sentence.get_value()+" is not a formula in propositional logic." # exit the function if any error

def print_tree(tree_lst):
  # Prints the syntactic tree.
  for atomic_sentence in tree_lst:
    # Print each atomic sentence in a line, with its branch of parents in its left
    string = atomic_sentence.get_value()
    parent = atomic_sentence
    while parent.get_parent() != None:
      # Adds the parent of the parent in the left of string
      parent = parent.get_parent()
      string = parent.get_value() + " ====> " + string
    print(string)

def main_task1_1():
  #string = input("Enter a sentence: ")
  string = "(||r)"
  string = "¬(¬r)"
  #string = "((p&&q)&&(||r))"
  #string = "((p&&q)&&r)"
  # ================= Things we must do: =================
  #Also "¬" must always be outside parentheses, if it isn't Sentence is not OK. we can solve this:
    #task 0 (sentences not OK when (¬r))
    #handle not pos[1] never happens
  #Also the syntactic tree stops building when there is a not OK sentence. Managing errors.
  # Note: ""(pp&q)"" is OK but "pp" is not OK
  string = preprocessing_data(string)
  a = Sentence(string)
  tree_lst = [a]
  try:
    syntactic_tree(string,tree_lst)
    print_tree(tree_lst)
  except AssertionError as message:
    print_tree(tree_lst)
    print(message)
    print("The Syntactic Tree was aborted.")
