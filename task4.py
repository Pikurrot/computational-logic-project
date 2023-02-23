import numpy as np
symbols = "&|-%+"  # (and,or,sufficient,necessary,biconditional)
all_symbols = symbols + "()¬"


def is_letter(char):
	return 97 <= ord(char) <= 122


def is_number(char):
	return 48 <= ord(char) <= 57


def is_atomic_sentence(string):
	if len(string) > 1:
		for c in string[1:]:
			if not is_number(c):
				return False
	return is_letter(string[0])

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

def preprocessing_data(string):
	#Simplify the expression symbols
	string = string.replace(" ", "").replace("<->", "+").replace("->", "-").replace("<-", "%").replace("||", "|").replace("&&", "&")
	if check_correspondance(string) == "Error" or not parentheses_match(string) or not closed_parentheses(string):
		return "Error"
	else:
		string = remove_outer_parentheses(replace_square_brackets_parentheses(string))
		if string == False:
			return "Error2"
	return string

class Sentence:

	def __init__(self, value, parent=None):
		# Each sentence object has 3 parameters: the sentence as a string (value), the sentence of which it comes (parent) and the subsentences that can be formed from that sentence (children)
		self._value = value
		self._parent = parent
		self._children = []
		if self._parent == None: self._depth = 0
		else: self._depth = self._parent.get_depth() + 1

	def add_children(self, list_of_children):
		for string in list_of_children:
			string = remove_outer_parentheses(string)
			if string == False:
				return "Error2"
			self._children.append(Sentence(string,parent=self))
	
	def get_value(self):
		return self._value

	def get_parent(self):
		return self._parent

	def get_children(self):
		return self._children

	def get_depth(self):
		return self._depth

	def get_truth_value(self,values):
		# Returns the truth value of the sentence
		if len(values) == 1:
			return not values[0]
		A,B = values
		if meta_sentence(self._value) == "A&B": # and
			return A and B
		elif meta_sentence(self._value) == "A|B": # or
			return A or B
		elif meta_sentence(self._value) == "A-B": # ->
			return not(A) or B
		elif meta_sentence(self._value) == "A+B": # <->
			return A == B
		elif meta_sentence(self._value) == "A%B": # <-
			return A or not(B) 

	def __str__(self):
		return self._value

def count_main_connectors(string):
	# Returns the number of main connectors in a string
	open_parentheses = 0
	count = 0
	for i in range(len(string)):
		if open_parentheses == 0 and string[i] in symbols:
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
		if open_parentheses == 0 and string[i] in symbols:
			return i
		if string[i] == "(":
			open_parentheses += 1
		elif string[i] == ")":
			open_parentheses -= 1
	return None


def remove_outer_parentheses(string):
	# Returns the string without the outer unnecessary parentheses
	if is_atomic_sentence(string):
		return string
	if string[0] == "¬":
		return string
	open_parentheses = 0
	Lopen_parentheses = []
	Lpositions = []
	maximum = 0
	for i in range(len(string)):
		if string[i] in (symbols + "¬"):
			Lopen_parentheses.append(open_parentheses)
			Lpositions.append(i)
		if string[i] == "(":
			open_parentheses += 1
			maximum += 1
		elif string[i] == ")":
			open_parentheses -= 1

	if len(Lopen_parentheses) == 0: return string[maximum:-maximum]

	minimum = min(Lopen_parentheses)
	main_connectors = [Lpositions[i] for i in range(len(Lpositions)) if Lopen_parentheses[i] == minimum]
	if count_main_connectors(string) > 1 and not \
		(all([string[i] in "¬&" for i in main_connectors]) 
		or all([string[i] in "¬|" for i in main_connectors])
		or all([string[i] in "¬+" for i in main_connectors])): 
		return False # If +1 main conectors and not all are AND or not all are OR

	if minimum == 0: return string
	return string[minimum:-minimum]


def check_correspondance(string):
	counter = 0
	parentheses = []
	for i in range(len(string)):
		if string[i] == "[" or string[i] == "(":
			counter += 1
			parentheses.append(string[i] == "(")
		if string[i] == "]":
			if parentheses[counter - 1] == False:
				counter -= 1
				parentheses.pop()
			else:
				return "Error"
		elif string[i] == ")":
			if parentheses[counter - 1] == True:
				counter -= 1
				parentheses.pop()
			else:
				return "Error"


def replace_square_brackets_parentheses(string):
	return string.replace("[","(").replace("]",")")


def divide_sentence(string, connector_pos):
	# Returns the 2 parts of the string separated by a connector, excluding outer parentheses
	return string[:connector_pos], string[connector_pos + 1:]


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


def meta_sentence(string):
	# Returns a string with the subsentences as meta language. Ex: (pp&q) = (A&B)
	# Note: it is assumed that string has been preprocessed
	meta_language = "AB"
	# extract subsentences
	sub_sentences = divide_by_main_connector(string)
	if sub_sentences == string:
		sub_sentences = [handle_not(string)]
		if sub_sentences[0] == string:
			if is_atomic_sentence(string):
				return meta_language[0]
			else:
				return string
	# substitute subsentences with meta language
	for sub_sentence, meta_letter in zip(sub_sentences, meta_language):
		string = string.replace(sub_sentence, meta_letter, 1)
	return string


def is_meta_sentence_OK(string):
	# True if the meta sentence of string is in the set of OK_sentences
	sentence = meta_sentence(string)
	OK_sentences = ("A", "¬A", "A&B", "A|B", "A-B", "A%B", "A+B")
	return sentence in OK_sentences


def sentences_are_atomic(list_sentences):
	# Returns True if any of the sentences in the list is atomic
	for sentence in list_sentences:
		if not is_atomic_sentence(sentence.get_value()):
			return False
	return True


def syntactic_tree(list_sentences):
	# Builds the syntactic tree layer by layer (not branch by branch).
	# Nothing is returned, but the tree grows in the list_sentences passed as parameter
	error = False
	while not sentences_are_atomic(list_sentences):  # repeat until all sentences are atomic
		list_sentences_cousins = []  # list to save, as a layer, the children made at every branch
		for sentence in list_sentences:
			is_sentence_OK = is_meta_sentence_OK(sentence.get_value())  # True if the current sentence has no errors
			if is_sentence_OK and not error and not is_atomic_sentence(sentence.get_value()):
				divided_string = divide_by_main_connector(sentence.get_value())  # list of the 2 parts of the divided string
				if divided_string == sentence.get_value():  # if the sentence has not changed
					alt_string = handle_not(sentence.get_value())  # alternative string without the ¬
					if sentence.add_children([alt_string]) == False:
						return "Error2"
				else:
					if sentence.add_children(divided_string) == False:
						return "Error2"
				list_sentences_cousins.extend(sentence.get_children())  # add children to list of cousins (otherwise, we end up only with the children of one of the parents, i.e. only the last branch would be saved)
			else:
				list_sentences_cousins.extend([sentence])  # add the sentence itself to the list
				if not is_sentence_OK and not error:
					not_OK_sentence = sentence  # save the sentence with the error
					error = True
		# update the list with the list of cousins, so the process can be repeated again with each cousin as a parent
		# Note: we can't do "list_sentences = list_sentences_cousins.copy()" because as lists are mutable, we would lose the adress of the original list by using the "=" operator.
		list_sentences.clear()
		list_sentences.extend(list_sentences_cousins)
		assert (not error), "The expression " + not_OK_sentence.get_value() + " is not a formula in propositional logic."  # exit the function if there was a not OK sentence detected in the layer


def remove_repeated_sentences(lst):
	# return a list with the sentences which their values are not repeated
	values = [sentence.get_value() for sentence in lst]
	not_repeated = [sentence for i,sentence in enumerate(lst) if sentence.get_value() not in values[:i]]
	return not_repeated


def get_branch(sentence):
	# return the sentence with all its branch until the founder
	if sentence.get_parent() == None: return (sentence,)
	else: return (sentence,)+get_branch(sentence.get_parent())


def get_header(tree_lst):
	# returns a list with the sentences ordered from the deepest to the first in the tree (without repeating)
	header = tree_lst[:]
	all_sentences = []
	for branch in header: all_sentences.extend(get_branch(branch))
	counter = max([branch.get_depth() for branch in header]) # start counter from the last depth
	while counter > 0: # iterate from the deepest to the 0 depth
		counter -= 1
		header.extend([sentence for sentence in all_sentences if sentence.get_depth() == counter])
	return remove_repeated_sentences(header)


def get_main_matrix(header, n_atomic):
	matrix = np.zeros((2**n_atomic,len(header))) # initialize empty matrix
	counter = int(2**n_atomic // 2) # e.g., ...4,2,1
	# put T/F to the atomic sentences columns
	for col in range(n_atomic):
		row = 0
		counter2 = True
		while row < 2**n_atomic:
			matrix[row:row+counter,col] = counter2 # set to T/F a group of ...4,2,1 rows
			row += counter
			counter2 = not(counter2) # flip every ...4,2,1 rows
		counter //= 2

	for col in range(n_atomic,len(header)):
		# get the sub_sentence
		sub_sentence = divide_by_main_connector(header[col].get_value())
		if sub_sentence == header[col].get_value():
			sub_sentence = [handle_not(header[col].get_value())]
		for e in range(len(sub_sentence)):
			sub_sentence[e] = remove_outer_parentheses(sub_sentence[e])
		
		# check for the column of the sub_sentence
		columns_pos = [c for s in sub_sentence for c in range(len(header)) if header[c].get_value() == s]
		columns = matrix[:,columns_pos].T
		for r in range(len(matrix)):
			matrix[r,col] = header[col].get_truth_value(tuple(columns[:,r]))
	return matrix
	

	
def is_tautology(matrix, n_atomic):
	# returns if it's a tautology and counter-examples
	last_col = matrix[:,-1]
	if all(last_col):
		return True,[]
	else:
		r = list(last_col).index(0)
		row = matrix[r]
		atomic_sentences = row[:n_atomic]
		return False,atomic_sentences


def is_contradiction(matrix, n_atomic):
	# returns if it's a contradiction and counter-examples
	last_col = matrix[:,-1]
	if not any(last_col):
		return True,[]
	else:
		r = list(last_col).index(1)
		row = matrix[r]
		atomic_sentences = row[:n_atomic]
		return False,atomic_sentences


def is_satisfiable(matrix, n_atomic):
	# returns if the sentence is satisfiable (if it can be T) and an example
	last_col = matrix[:,-1]
	if any(last_col):
		r = list(last_col).index(1)
		row = matrix[r]
		atomic_sentences = row[:n_atomic]
		return True,atomic_sentences
	else:
		return False,[]


def main_connectors_pos(string):
	# Returns a list with the position of the main connectors (multiple) (the ones inside only 1 parentesis)
	open_parentheses = 0
	positions = []
	for i in range(len(string)):
		if open_parentheses == 0 and string[i] in symbols:
			positions.append(i)
		if string[i] == "(":
			open_parentheses += 1
		elif string[i] == ")":
			open_parentheses -= 1
	return positions

def separate_parts_dict(string,funct):
	# returns a dictionary with keys: original parts of the expression separated by the main/s connector/s; and values: these parts with a the given function applied
	connectors_pos = main_connectors_pos(string)
	parts = {}
	prev_pos = 0
	for pos in connectors_pos:
		part = string[prev_pos:pos]
		parts[part] = funct(part)
		prev_pos = pos+1
	part = string[prev_pos:]
	parts[part] = funct(part)
	return parts

def remove_unnecessary_parentheses(string, origin=True):
	# returns a string without unnecessary parentheses (outer and inner) without changing the original structure
	if string[0] == "¬":
		return "¬" + remove_unnecessary_parentheses(string[1:],False)
	elif string[0] == "(":
		inside = remove_outer_parentheses(string)
		if count_main_connectors(inside) == 0:
			return remove_unnecessary_parentheses(inside,False)
		else:
			parts = separate_parts_dict(inside, lambda x: remove_unnecessary_parentheses(x,False))
			for part,new in parts.items():
				inside = inside.replace(part,new)
			if origin:
				return inside
			else:
				return "(" + inside + ")"
	else:
		return string


def main_task4():
	print("task 4")

	menu_num = int(input("PLEASE, CHOOSE AN OPTION:\n1 - Tautology\n2 - Contradiction\n3 - Logical Equivalence\n4 - Satisfiability\n5 - Logical Consequence\n"))
	if menu_num == 1:
		string = input("Enter sentence: ")
	elif menu_num == 2:
		string = input("Enter sentence: ")
	elif menu_num == 3:
		string1 = input("Enter sentence 1: ")
		string2 = input("Enter sentence 2: ")
		string = "(" + string1 + ")<->(" + string2 + ")"
		print(string)
	elif menu_num == 4:
		num_sentences = int(input("Enter number of sentences: "))
		sentences = []
		for i in range(num_sentences):
			sentences.append(input("Enter sentence " + str(i) + ": "))
		string = "(" + ")&(".join(sentences) + ")"
	elif menu_num == 5:
		num_premises = int(input("Enter number of premises:"))
		premises = []
		for i in range(num_premises):
			premises.append(input("Enter premise " + str(i) + ": "))
		consequence = input("Enter consequence: ")
		string = "(" + ")&(".join(premises) + ")"
		string = "(" + string + ")-(" + consequence + ")"
	else:
		print("The option doesn't exist")
		return


	string = preprocessing_data(string)
	string = remove_unnecessary_parentheses(string)
	if string == "Error":
		print("Error with parentheses or brackets! :(")
		return
	founder = Sentence(string)  # the founder sentence that will build the tree
	tree_lst = [founder]
	try:
		syntactic_tree(tree_lst)
	except AssertionError as message:
		print(message)
		print("The Syntactic Tree was aborted.")
		return
	
	header = get_header(tree_lst)
	n_atomic = len(remove_repeated_sentences(tree_lst))
	matrix = get_main_matrix(header,n_atomic)

	if menu_num == 1:
		is_true,counter_examples = is_tautology(matrix, n_atomic)
		if is_true:
			print("Congratulations. The sentence is a Tautology")
		else:
			print("The sentence is not a Tautology. You can find the next counter-example:")
			for i,atomic in enumerate(counter_examples):
				print(str(header[i]), "=", bool(atomic))
	elif menu_num == 2:
		is_true,counter_examples = is_contradiction(matrix, n_atomic)
		if is_true:
			print("Congratulations. The sentence is a Contradiction")
		else:
			print("The sentence is not a Contradiction. You can find the next counter-example:")
			for i,atomic in enumerate(counter_examples):
				print(str(header[i]), "=", bool(atomic))
	elif menu_num == 3:
		is_true,counter_examples = is_tautology(matrix, n_atomic)
		if is_true:
			print("Congratulations. The sentences are logically equivalent")
		else:
			print("The sentence are not logically equivalent. You can find the next counter-example:")
			for i,atomic in enumerate(counter_examples):
				print(str(header[i]), "=", bool(atomic))
	elif menu_num == 4:
		is_true,examples = is_satisfiable(matrix, n_atomic)
		if is_true:
			print("Congratulations. The sentences are satisfiable. You can find the next example:")
			for i,atomic in enumerate(examples):
				print(str(header[i]), "=", bool(atomic))
		else:
			print("The sentences are not satisfiable.")
	elif menu_num == 5:
		is_true,counter_examples = is_tautology(matrix, n_atomic)
		if is_true:
			print("Congratulations. The conclusion is a logical consequence from the premises.")
		else:
			print("The Conclusion is not a logical consequence from the premises. You can find the next counter-example:")
			for i,atomic in enumerate(counter_examples):
				print(str(header[i]), "=", bool(atomic))