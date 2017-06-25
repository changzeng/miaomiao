from trie import Trie
from markov import Markov
import jieba

trie = Trie()
markov = Markov()

#result,unkow_words = trie.all_cut("")
with open("data/test.txt",encoding="utf8") as fd:
	text = fd.read()

punctuation = ("，","。","！","？","、","；","：")
space = ("\n","\t"," ")
# 标号：引号（“ ” ‘ ’）、括号〔（ ） [ ] { } ,,── ,、,······,、,,、,,《,》,〈,〉,、,·,、,—,____

tmp = ""
sentence = []
for c in text:
	if c is space:
		continue

	if c in punctuation:
		sentence.append((c,tmp))
		tmp = ""
	else:
		tmp += c

result = []
for item in sentence:
	trie_cut = trie.cut(item[1])
	markov_cut = markov.cut(item[1])
	jieba_cut = list(jieba.cut(item[1]))

	print("----------------------------")
	print("trie:",trie_cut)
	print("markov:",markov_cut)
	print("jieba:",jieba_cut)
	print("----------------------------")

# some thing need to improve
# emit matrix key error