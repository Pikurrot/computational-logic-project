# <summary>
# Get the white spaces out.
# </summary>
# <param name="input">Input introduced by the user.</param>
# <returns>Expression with no blank spaces, and with connectors just occupying one digit.</returns>
def PreProcessingData(expression):
    return expression.replace(" ", "").replace("<->", "+").replace("->", "-").replace("||", "|").replace("&&", "&");

# <summary>
# Check the Sufficient Conditions to figure out if the input is a Formula in Propositional Logic.
# </summary>
# <param name="expression">Pre-processed input.</param>
# <returns>True if is an Atomic Sentence.</returns>
def CheckSufficientConditions(expression):
    return IsAtomicSentence(expression);

# <summary>
# Check some basic necessaty conditions.
# </summary>
# <param name="expression">Expression to be analyzed.</param>
def CheckNecessaryConditions(expression):
    startBrackets = 0
    endBrackets = 0
    badCharacter = 0

    # Atomic Sentence that indicates if in some moment we have more closing than opening brackets.
    m = False

    for i in range(len(expression)):
        c = expression[i]

        # First-order logic would be better here...
        if (not IsLowerLetter(c) and not IsNumber(c) and not IsBracket(c) and not IsConnector(expression[i])):
            badCharacter += 1
        elif (IsOpeningBracket(c)):
            startBrackets += 1
        elif (IsClosingBracket(c)):
            endBrackets += 1

        if (startBrackets < endBrackets):
            m = True
            break

    # s = Same Number of Parenthesis.
    s = startBrackets == endBrackets

    # b = There is one bad character.
    b = badCharacter > 0

    return s and not b and not m


# <summary>
# Check if the Sentence is an atomic sentence.
# </summary>
# <param name="expression">Expression to be analyzed.</param>
# <returns>Treu if is an atomic sentence.</returns>
def IsAtomicSentence(expression):
    numberOfLetters = 0
    badCharacters = 0

    # First-order logic would be better here...
    for i in range(len(expression)):
        c = expression[i]
        if (not(IsLowerLetter(c) or IsNumber(c))):
            badCharacters = badCharacters + 1
        elif (IsLowerLetter(c)):
            numberOfLetters += 1

    # f = First character of the expression is a letter.
    f = IsLowerLetter(expression[0]);

    # m = There is more than one letter.
    m = numberOfLetters > 1;

    # b = Has some Bad Character.
    b = badCharacters > 0;

    return f and not m and not b;

# <summary>
# Indicates if the character is a propositional logic connector.
# </summary>
# <param name="character">character to be analyzed.</param>
# <returns>True if is a connector.</returns>
def IsConnector(character):
    return character == '|' or character == '&' or character == '-' or character == '+' or IsNegation(character)

# <summary>
# Indicates if the character is a negation in propositional logic.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if is a Negation.</returns>
def IsNegation(character):
    return character == '¬'

# <summary>
# Indicates if the character is a Lower Letter.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if it is a letter.</returns>
def IsLowerLetter(character):
    return ord(character) >= 97 and ord(character) <= 122

# <summary>
# Indicates if the character is a Number from 0 to 9.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if it is a number.</returns>
def IsNumber(character):
    return ord(character) >= 48 and ord(character) <= 57

# <summary>
# Indicates if the character is a opening bracket.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if it is a opening bracket.</returns>
def IsOpeningBracket(character):
    return character == '('

# <summary>
# Indicates if the character is a opening bracket.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if it is a opening bracket.</returns>
def IsClosingBracket(character):
    return character == ')'

# <summary>
# Indicates if the character is a bracket.
# </summary>
# <param name="character">Character to be analyzed.</param>
# <returns>True if it is a bracket.</returns>
def IsBracket(character):
    return IsOpeningBracket(character) or IsClosingBracket(character)

str_input = "(((p-> ¬r) && ¬¬(p || r)) <-> (p && ¬q))"
'''
input = "(p&&q)"
input = "((p || q) && ¬(p && q))"
input = "¬¬¬¬¬p"
input = "¬¬(¬¬(p && ¬q))"
input = "((p-> ¬r) && ¬¬(p || r)) <-> (p && ¬q)"
input = "p && q"
input = "(p)"
input = "(p -> q) || (p -> r)"
input = "p -> ((q || p) -> r)"
input = "(p -> ¬r) && ¬(¬(p || r) <-> (p && ¬ q))"
input = "(p -> ¬r) && ¬(¬(p || R) <-> (p && ¬ q))"
input = "p454"
input = "p123"
input = "123"
'''
str_input = input("Enter a logic sentence: ")

str_input = PreProcessingData(str_input)

print(str_input)

if CheckSufficientConditions(str_input):
    print("The Sentence is ok")
elif not CheckNecessaryConditions(str_input):
    print("The Sentence is NOT ok")
else:
    print("I don't know if the sentence is OK")