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
		self.label = int(raw[-1])

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
def corpusOfEmail(email_):
	return [dictionary[i] for (i, w) in enumerate(email_.corpus) if w == 1]

def classifyExists(word_):
	return 1 if (word_ == 1) else -1

def classifyDoesntExist(word_):
	return 1 if (word_ == 0) else -1


def calcError(word_, emails_, weights_):
	error = 0.0
 
	for (i, email) in enumerate(emails_):
		class_label = classifyExists(email.corpus[word_])

		if (class_label != email.label):
			error += weights_[i]

	return error

def handleError(emails_, weights_, best_):
	for (i, word) in enumerate(emails_[0].corpus):
		error = calcError(i, emails_, weights_)

		negated = 1.0 - error
		if (error < best_.error):
			best_.word = i
			best_.error = error
			best_.label = 1
		elif(negated < best_.error):
			best_.word = i
			best_.error = negated
			best_.label = -1

	return best_

def boost(emails_, weights_):
	# Handle error
	best = handleError(emails_, weights_, Best(-1, 100.0, 0))

	# Hittin' the gym
	alpha = 0.5 * math.log((1.0 - best.error) / best.error)

	for (i, email) in enumerate(emails_):
		word = email.corpus[best.word]
		const = -alpha * email.label

		if best.label == 1:
			weights_[i] *= math.exp(const * classifyExists(word))
		else:
			weights_[i] *= math.exp(const * classifyDoesntExist(word))

	# Normalize
	sum_w = sum(weights_)
	for i in range(len(weights_)):
		weights_[i] /= sum_w

	return (alpha, best)

def signOf(num_):
	return (num_ / math.fabs(num_))

def classifyFinal(email_, results_):
	total = 0.0
	for (alpha, best) in results_:
		if best.label == 1:
			if email_.corpus[best.word] == 1:
				total += alpha
			else:
				total -= alpha
		else:
			if email_.corpus[best.word] == 0:
				total += alpha
			else:
				total -= alpha

	return signOf(total)

def countErrors(data_):
	errors = 0
	for email in data_:
		label = classifyFinal(email, results)

		if label != email.label:
			errors += 1

	return errors

###############################################################################

# V-Tec just kicked in
t_set = [3, 7, 10, 15, 20]

for t in t_set:
	weights = [(1.0/len(train)) for email in train]
	results = [boost(train, weights) for i in range(t)]

	# Training
	print "\nt: %d | Training Error: %f" % (t, (1.0 * countErrors(train) / len(train)))

	# Test
	print "t: %d | Testing Error: %f" % (t, (1.0 * countErrors(test) / len(test)))

	# Print words from dictionary
	for (alpha, best) in results:
		print (" + %s" if best.label == 1 else " - %s") % dictionary[best.word]
