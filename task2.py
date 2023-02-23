# user input
input = '¬¬p&q-r|¬q+s'
input_connectors = ['|','+'] # e.g disjuntion of a conditional
print_process = False

# initial variables
possible_connectors = "&|-%+"  # (and,or,sufficient,necessary,biconditional)
dict_expressions = dict()
connector_count = 0
start_ord = ord("A")
letter_ord = start_ord

def count_main_connectors(string):
	# Returns the number of main connectors in a string
	open_parentheses = 0
	count = 0
	for i in range(len(string)):
		if open_parentheses == 0 and string[i] in possible_connectors:
			count += 1
		if string[i] == "(":
			open_parentheses += 1
		elif string[i] == ")":
			open_parentheses -= 1
	return count


def main_connector_pos(string):
	# Returns the position of the main connector (the one inside only 0 parentesis). If no main connector, or first character is "¬", returns None
	open_parentheses = 0
	for i in range(len(string)):
		if open_parentheses == 0 and string[i] in possible_connectors:
			return i
		if string[i] == "(":
			open_parentheses += 1
		elif string[i] == ")":
			open_parentheses -= 1
	return None


def getMetaSentences(current_letter_ord, connector, input_exp = None):
	# returns the current expression in metalanguage with parentheses arund the given connector
	if input_exp == None:
		expression = dict_expressions[chr(current_letter_ord)]
		current_letter_ord = ord(list(dict_expressions.keys())[-1])
	else:
		expression = input_exp
	# print("expression:",expression)
	
	pos = -1
	new_sentence = expression
	if connector == None:
		# print("Exiting function (nothing changed here)...")
		return new_sentence, False
	elif connector in possible_connectors:
		pos = expression.find(connector)
	elif connector == '¬':
		pos = 0

	# pos: the position of the current connector
	if pos == 0:
		# connector is ¬
		current_letter_ord = current_letter_ord + 1
		alt_sentence = expression[1:]
		has_connector = any([c in alt_sentence for c in possible_connectors])
		letter = chr(current_letter_ord)
		# print("Found ¬, creating", letter, "as", alt_sentence)
		dict_expressions[letter] = alt_sentence
		if has_connector:
			letter = '('+ letter + ')'
		new_sentence = "¬" + letter # e.g ¬(B)
	elif pos > 0:
		# any other connector
		counter = 0
		while counter < 2:
			# do it for left and right half of the connector
			counter +=1
			current_letter_ord += 1
			if counter == 1:
				half = expression[:pos] # left half
			elif counter == 2:
				half = expression[pos+1:] # right half
			has_connector = any([c in half for c in possible_connectors])
			letter = chr(current_letter_ord)
			# print("found", connector, "creating", letter, "as", half)
			dict_expressions[letter] = half
			n = count_main_connectors(half)
			if n > 1:
				input_connectors.append(half[main_connector_pos(half)])
			if has_connector:
				letter = '('+ letter + ')'
			new_sentence = new_sentence*(counter==2) + letter + expression[pos]*(counter==1) 
	# print("returning", new_sentence) # e.g C&(D)
	return new_sentence, pos != -1

def main_task2():
	global connector_count, letter_ord, input
	# print(dict_expressions)
	# print("Checking",input, "for", input_connectors[connector_count])
	input,changed = getMetaSentences(letter_ord - 1, input_connectors[connector_count], input)
	# print("changed:",changed)
	
	connector_count += 1
	letter_ord += len(dict_expressions) - 1
	letter_count = 0
	
	while True:
		print(dict_expressions)
		connector = None
		if len(input_connectors) > connector_count:
			connector = input_connectors[connector_count]
		# print("Checking",chr(letter_ord), "for", connector)
		dict_expressions[chr(letter_ord)],changed = getMetaSentences(letter_ord, connector)
		# print("changed:",changed)
		letter_ord += 1
		letter_count += 1
		if letter_count == len(dict_expressions):
			# print("END")
			break
		elif changed:
			# print("passing to next connector")
			connector_count += 1
			letter_count -= 1
		if letter_ord - start_ord == len(dict_expressions):
			# print("setting letter to", chr(start_ord), "(something changed, so let's check the dict again)")
			letter_ord = start_ord
			letter_count = 0
			
	
	print(dict_expressions)
	output = input
	for key in dict_expressions.keys():
		output = output.replace(key, dict_expressions[key])
	
	print("output:",output)
