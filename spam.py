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

		# print "C_Label: %d | E_Label: %d" % (class_label, email.label)
		if (class_label != email.label):
			error += weights_[i]

	return error

def boost(t_, emails_, weights_):
	best = Best(-1, 100.0, 0)

	# Handle error
	for (i, word) in enumerate(emails_[0].corpus):
		error = calcError(i, emails_, weights_)
		# print "Error (boost) %f" % error

		if (error < best.error):
			best.word = i
			best.error = error
			best.label = 1
		elif((1.0 - error) < best.error):
			best.word = i
			best.error = 1.0 - error
			best.label = -1

	# Hittin' the gym
	try:
		alpha = 0.5 * math.log((1.0 - best.error) / best.error)
	except ValueError:
		print "Alpha crashed with %f" % best.error
		exit(1)

	print "Alpha: %f" % alpha

	for (i, email) in enumerate(emails_):
		classification = 0

		if best.label == 1:
			classification = classifyExists(email.corpus[best.word])
		else:
			classification = classifyDoesntExist(email.corpus[best.word])

		weights_[i] = weights_[i] * math.exp(-alpha * email.label * classification)

	print "Weights: %f" % sum(weights_)

	# Normalize
	sum_w = sum(weights_)
	weights_ = [(1.0 * weight / sum_w) for weight in weights_]

	return (alpha, best)

###############################################################################

def classifyFinal(email_, results_):
	total = 0.0
	for (alpha, best) in results_:
		if email_.corpus[best.word] == best.label:
			total += alpha
		else:
			total -= alpha

	return (total / math.fabs(total))

# V-Tec just kicked in
t_set = [3] #[3, 7, 10, 15, 20]
weights = [(1.0/len(train)) for email in train]

for t in t_set:
	results = [boost(t, train, weights) for i in range(t)]

	errors = 0
	for email in train:
		label = classifyFinal(email, results)

		if label != email.label:
			errors += 1

	print "t: %d | Error: %f" % (t, (1.0 * errors / len(train)))

	for (alpha, best) in results:
		if best.label == 1:
			print "Word not spam: %s" % dictionary[best.word]
		else:
			print "Word is spam: %s" % dictionary[best.word]
