symbols = "&|-%+"  # "&|!" (and,or,sufficient,necessary,biconditional)
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


def preprocessing_data(string):
	#Simplify the expression symbols
	return string.replace(" ", "").replace("<->", "+").replace("->", "-").replace("<-", "%").replace("||", "|").replace("&&", "&")


class Sentence:

	def __init__(self, value, parent=None):
		# Each sentence object has 3 parameters: the sentence as a string (value), the sentence of which it comes (parent) and the subsentences that can be formed from that sentence (children)
		self.value = value
		self.parent = parent
		self.children = []

	def add_children(self, list_of_children):
		for string in list_of_children:
			self.children.append(Sentence(string, parent=self))

	def get_value(self):
		return self.value

	def get_parent(self):
		return self.parent

	def get_children(self):
		return self.children

	def __str__(self):
		return self.value


def main_connector_pos(string):
	# Returns the position of the main connector (the one inside only 0 parentesis). If no main connector, or first character is "¬", returns None
	if string[0] == "¬":
		return None
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
	# Returns the string without the outter unnecessary parentheses
	if string[0] == "¬":
		return None
	open_parentheses = 0
	Lopen_parentheses = []
	for i in range(len(string)):
		if string[i] in symbols:
			Lopen_parentheses.append(open_parentheses)
		if string[i] == "(":
			open_parentheses += 1
		elif string[i] == ")":
			open_parentheses -= 1
	return string[min(Lopen_parentheses):-min(Lopen_parentheses)]
	
#--------------------------------------------------------------------------------------
# We finished here
#--------------------------------------------------------------------------------------


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
	print(sub_sentences)
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
	print(sentence)
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
			is_sentence_OK = is_meta_sentence_OK(sentence.value)  # True if the current sentence has no errors
			if is_sentence_OK and not error and not is_atomic_sentence(
			  sentence.get_value()):
				divided_string = divide_by_main_connector(sentence.value)  # list of the 2 parts of the divided string
				if divided_string == sentence.value:  # if the sentence has not changed
					alt_string = handle_not(sentence.value)  # alternative string without the ¬
					sentence.add_children([alt_string])
				else:
					sentence.add_children(divided_string)
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


def print_tree(tree_lst):
	# Prints the syntactic tree.
	for atomic_sentence in tree_lst:
		# Print each atomic sentence in a line, with its branch of parents in its left
		string = atomic_sentence.get_value()
		parent = atomic_sentence
		while parent.get_parent() != None:  # Until the founder (which has no parent)
			# Adds the parent of the parent in the left of string
			parent = parent.get_parent()
			string = parent.get_value() + "  ==>  " + string
		print(string)


def main_task1_2():
	print("task 1.2")
	string = input("Enter a sentence: ")
	#string = "(((p&q)|r))"
	string = preprocessing_data(string)
	print(remove_outer_parentheses(string))
	# founder = Sentence(string)  # the founder sentence that will build the tree
	# tree_lst = [founder]
	# try:
	# 	syntactic_tree(tree_lst)
	# 	print_tree(tree_lst)
	# except AssertionError as message:
	# 	print_tree(tree_lst)  # here the tree will be printed until the layer with the error
	# 	print(message)
	# 	print("The Syntactic Tree was aborted.")
