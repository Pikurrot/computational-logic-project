# global variables
symbols = "&|¬-%+"  # "&|!" (and,or,not,sufficient,necessary,biconditional)
all_symbols = symbols + "()"

def is_letter(char):
  return 97<=ord(char)<=122

def preprocessing_data(string):
  #Simplify the expression symbols
  return string.replace(" ", "").replace("<->", "+").replace("->", "-").replace("<-","%").replace("||", "|").replace("&&", "&")

# functions

# Mustapha function (i don't know if its ok)  
""""
def letters_together(string):
  isLet = True
  let = 1
  for c in string:
  #s = string[0:let]
    if not is_letter(c):
      isLet = False
    elif is_letter(c): #and (len(c)==1):
      isLet = True
      #let > 1
      print("Not OK")
    elif is_letter(s) and len(s) == 1:
      isLet = True
      let = 1
      print("OK")
  return 0"""
def letters_together(string):
  # Checks if the string contains two letters together
  for i in range(len(string)):
    if is_letter(string[i]) and i < len(string) - 1:
      if string[i + 1] in all_symbols:
        # If a letter is after a letter
        return True
  return False

def symbols_together(string):
  # Checks if the string contains two symbols together
  for i in range(len(string)):
    if string[i] in all_symbols and i < len(string) - 1:
      if string[i + 1] in all_symbols:
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

def bad_characters(string):
# Checks if there are bad characters
  for c in string:
    if(not is_letter(c) and c not in all_symbols):
      return True
  return False
      
# main
string = input("Enter a sentence: ")

if (parentheses_match(string) and closed_parentheses(string) and not symbols_together(string) and not letters_together(string) and not bad_characters()):
  print("The sentence is OK")
else:
  print("The sentence is not OK")
#Dona error p&q