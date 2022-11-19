# global variables
symbols = "&|-%+"  # "&|!" (and,or,not,sufficient,necessary,biconditional)
all_symbols = symbols + "()¬"

def is_letter(char):
  return 97<=ord(char)<=122

def is_number(char):
  return 48<=ord(char)<=57

def bad_characters(string):
# Checks if there are bad characters
  for c in string:
    if(not is_letter(c) and c not in all_symbols):
      return True
  return False

def is_atomic_sentence(string):
  if len(string) > 1:
    for c in string[1:]:
      if not is_number(c):
        return False
  return is_letter(string[0])

def preprocessing_data(string):
  #Simplify the expression symbols
  return string.replace(" ", "").replace("<->", "+").replace("->", "-").replace("<-","%").replace("||", "|").replace("&&", "&")

def letters_together(string):
  # Checks if the string contains two letters together
  for i in range(len(string)):
    if is_letter(string[i]) and i < len(string) - 1:
      if is_letter(string[i+1]):
        # If a letter is after a letter
        return True
  return False

def symbols_together(string):
  # Checks if the string contains two symbols together
  for i in range(len(string)):
    if string[i] in symbols and i < len(string) - 1:
      if string[i + 1] in symbols:
        # If a symbol is after a symbol
        return True
  return False

def parentheses_match(string):
  # Checks if parenthesis "(" match with its corresponding ")"
  open_parentheses = 0
  for i in range(len(string)):
    if string[i] == "(":
      open_parentheses += 1
    elif string[i] == ")":
      open_parentheses -= 1
  return open_parentheses == 0

def closed_parentheses(string):
  # Checks that at every position there aren't more closed parentheses than open ones
  closed_parentheses = 0
  open_parentheses = 0
  for i in range(len(string)):
    if string[i] == "(":
      open_parentheses += 1
    elif string[i] == ")":
      closed_parentheses += 1
    if closed_parentheses > open_parentheses:
      return False
  return True

def check_necessary_conditions(string):
  return (parentheses_match(string) and closed_parentheses(string) and not symbols_together(string) and not letters_together(string) and not bad_characters(string))

def check_sufficient_conditions(string):
  return is_atomic_sentence(string)

def sentence_OK(string):
  string = preprocessing_data(string)
  if check_sufficient_conditions(string): # The sentence is OK
    return True
  elif not check_necessary_conditions(string): # The sentence is not OK
    return False
  else: # I don't know if the sentence is OK
    return None

def main_task0():
  print("task 0")
  string = input("Enter a sentence: ")
  string = preprocessing_data(string)
  ok = sentence_OK(string)
  if ok == None:
    print("I don't know if the sentence is OK")
  elif ok:
    print("The sentence is OK")
  else:
    print("The sentence is not OK")
    