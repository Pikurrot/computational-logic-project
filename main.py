# global variables
letters = "abcdefghijklmnñopqrstuvwxyz"
symbols = "^v¬"  # "&|!" (and,or,not)


# functions
def letters_together(string):
  letters = "abcdefghijklmnñopqrstuvwxyz"
  isLet = True
  let = 1
  s = string[0:let]
  if s not in letters:
    isLet = False
  elif s in letters and (len(s) > 1 or len(s) < 1):
    isLet = True
    let > 1
    print("Not OK")
  elif s in letters and len(s) == 1:
    isLet = True
    let = 1
    print("OK")
  return 0


def symbols_together(string):
  # Checks if the string contains two symbols together
  all_symbols = symbols + "()"
  for i in range(len(string)):
    if string[i] in all_symbols and i < len(string) - 1:
      if string[i + 1] in all_symbols:
        # If a symbol is after a symbol
        return True
  return False


def parentheses_match(string):
  # Checks if parenthesis "(" match with its corresponding ")"
  lst_parentesis = []
  for i in range(len(string)):
    if string[i] == "(":
      lst_parentesis.append(1)
    elif string[i] == ")":
      del lst_parentesis[-1]
  # falta acabar


# main
string = input("Enter a sentence: ")
