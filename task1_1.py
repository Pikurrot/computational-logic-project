# global variables
symbols = "&|-%+"  # "&|!" (and,or,not,sufficient,necessary,biconditional)
all_symbols = symbols + "()¬"

def preprocessing_data(string):
  #Simplify the expression symbols
  return string.replace(" ", "").replace("<->", "+").replace("->", "-").replace("<-","%").replace("||", "|").replace("&&", "&")

def is_letter(char):
  return 97<=ord(char)<=122

def is_atomic_sentence(string):
  if len(string) == 1:
    return is_letter(string)
  else:
    return False

def main_connector_pos(string):
  open_parentheses = 0
  for i in range(len(string)):
    if open_parentheses == 1 and string[i] in symbols:
      return i
    if string[i] == "(":
      open_parentheses += 1
    elif string[i] == ")":
      open_parentheses -= 1
  
def divide_sentence(string, connector_pos):
  return string[1:connector_pos], string[connector_pos+1:-1]
  # ((p&q)|¬r)

def handle_not(string):
  for c in string:
    if c == "¬":
      return string[1:]

#¬(p&q)
# main

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
'''