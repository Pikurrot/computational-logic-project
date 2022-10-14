dicExpressions = dict()
input = '¬¬p&q-r|¬q'
input = 'p|q+r-r&t'
connectors = ['-', '&']
startConnector = 0
startIndex = 65

def getExpressions(currentIndex, connector, input_exp = None):
    expression = input_exp if input_exp is not None else dicExpressions[chr(currentIndex)]

    if input_exp is None:
        currentIndex = ord(list(dicExpressions.keys())[-1])
    position = -1
    new_expression = expression

    if connector == '&' or connector is None and '&' in expression:
        position = expression.find('&')
    elif connector == '|' or connector is None and '|' in expression:
        position = expression.find('|')
    elif connector == '-' or connector is None and '-' in expression:
        position = expression.find('-')
    elif connector == '+' or connector is None and '+' in expression:
        position = expression.find('+')
    elif connector == '¬':
        position = 0

    if position == 0:
        currentIndex = currentIndex + 1
        has_brackets = '&' in expression[1:] or '|' in expression[1:] or '-' in expression[1:] or '+' in expression[1:]
        dicExpressions[chr(currentIndex)] = expression[1:]
        letter_expression = chr(currentIndex)
        if has_brackets:
            letter_expression = '('+ letter_expression + ')'
        new_expression = expression[position] + letter_expression
    elif position > 0:
        currentIndex = currentIndex + 1
        has_brackets = '&' in expression[0:position] or '|' in expression[0:position] or '-' in expression[0:position] or '+' in expression[0:position]
        dicExpressions[chr(currentIndex)] = expression[0:position]
        letter_expression = chr(currentIndex)
        if has_brackets:
            letter_expression = '('+ letter_expression + ')'
        new_expression = letter_expression + expression[position]
        currentIndex = currentIndex + 1
        has_brackets = '&' in expression[position + 1:] or '|' in expression[position + 1:] or '-' in expression[position + 1:] or '+' in expression[position + 1:]
        dicExpressions[chr(currentIndex)] = expression[position + 1:]
        letter_expression = chr(currentIndex)
        if has_brackets:
            letter_expression = '('+ letter_expression + ')'
        new_expression = new_expression + letter_expression
    return new_expression

# print(input)

input = getExpressions(startIndex - 1, connectors[startConnector], input)
startConnector = startConnector + 1
startIndex = startIndex + len(dicExpressions) - 1

while True:
    connector = None
    if len(connectors) > startConnector:
        connector = connectors[startConnector]
    dicExpressions[chr(startIndex)] = getExpressions(startIndex, connector)
    startIndex = startIndex + 1
    startConnector = startConnector + 1
    if chr(startIndex) not in dicExpressions.keys():
        break

for key in dicExpressions.keys():
    input = input.replace(key, dicExpressions[key])

print(input)