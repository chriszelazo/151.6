################################
#    Homework 6 - Problem 3    #
################################
# Chet Lemon (A10895241)       #
# Kesav Mulakaluri (A10616114) #
# Chris Zelazo (A10863450)     #
################################

import math

# Classes #
class Email:
	def __init__(self, raw):
		self.corpus = map(int, raw[:-1])
		self.label = raw[-1]

class Best:
	def __init__(self, word, error, label):
		self.word = int(word)
		self.error = float(error)
		self.label = int(label)

# Data Parsing #
def parseEmailData(file_):
	with open(file_) as f:
		return [Email(l.split()) for l in f]

def getTrain():
	return parseEmailData("hw6train.txt")

def getTest():
	return parseEmailData("hw6test.txt")

def getDict():
	with open("hw6dictionary.txt") as f:
		return [l.strip() for l in f]

# We're going to use these a lot #
train = getTrain()
test = getTest()
dictionary = getDict()

# Helper functions #
def getWordsFromEmail(email_):
	return [dictionary[i] for (i, w) in enumerate(email_.corpus) if w == 1]

def classifyExists(word_):
	return 1 if (word_ == 1) else -1

def classifyDoesntExist(word_):
	return -1 * classifyExists(word_)


def calcError(word_, emails_, weights_):
	error = 0.0

	for (i, email) in enumerate(emails_):
		if (classifyExists(email.corpus[word]) != email.label):
			error += weights_[i]

	return error

def boost(t_, emails_, weights_):
	best = Best(-1, 100.0, 0)

	# Handle error
	for word in emails[0].corpus:
		error = calcError(word, emails_, weights_)

		if (error < best.error):
			best.word = word
			best.error = error
			best.label = 1
		elif((1.0 - error) < best.error):
			best.word = word
			best.error = 1.0 - error
			best.label = -1



###############################################################################

# V-Tec just kicked in
t_set = [3, 7, 10, 15, 20]
weights = [(1.0/len(train) for email in train]

for t in t_set:
