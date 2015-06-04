################################
#    Homework 6 - Problem 3    #
################################
# Chet Lemon (A10895241)       #
# Kesav Mulakaluri (A10616114) #
# Chris Zelazo (A10863450)     #
################################

# Classes
class Email:
	def __init__(self, raw):
		self.vector = map(int, raw[:-1])
		self.label = raw[-1]

# Data Parsing
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

# We're going to use these a lot
train = getTrain()
test = getTest()
dictionary = getDict()

# Helper functions
def getWordsFromEmail(email_):
	return [dictionary[i] for (i, w) in enumerate(email_.vector) if w == 1]

print getWordsFromEmail(train[53])
