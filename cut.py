#from markov.py import Markov
from trie import Trie

trie = Trie()

#positive match
def positive_match(sentence):
	i=0
	j=1
	words = []
	while True:
		#print(sentence[i:j])
		if trie.isAWord(sentence[i:j]):
			print(sentence[i:j])
			words.append(sentence[i:j])
			i = j
		j += 1
		if j> len(sentence):
			if i>=len(sentence):
				break
			words.append(sentence[i])
			i += 1
			j = i+1
			if i>= len(sentence):
				break
	print(words)
	return words

#nagetive match
def nagetive_match(sentence):
	i = len(sentence)
	j = i-1
	words = []
	while True:
		#print(sentence[i:j])
		if trie.isAWord(sentence[i:j]):
			print(sentence[i:j])
			words.insert(0,sentence[i:j])
			j = i
		i -= 1
		if i < 0:
			if j <= 0:
				break
			words.append(sentence[j-1])
			j -= 1
			i = j-1
			if j <= 0:
				break

	print(words)
	return words

positive_match("迈向充满希望的新世纪")
nagetive_match("迈向充满希望的新世纪")