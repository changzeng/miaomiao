import os,json

class Trie:
	def __init__(self):
		self.dic = {}

		if os.path.exists("trie.data"):
			#read from file
			with open("trie.data") as fd:
				self.dic = json.load(fd)
		else:
			#parse from file
			with open("word_warehouse.txt") as fd:
				for line in fd.readlines():
					word = line.split("\t")[1]
					self.put_into_dic(word)

			#write dic to file
			with open("trie.data","w") as fd:
				json.dump(self.dic,fd)

	#write a word to dic
	def put_into_dic(self,word):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				tmp = tmp[char][1]
			except:
				if i == len(word)-1:
					tmp[char] = [1,{}]
				else:
					tmp[char] = [0,{}]
				tmp = tmp[char][1]

	#validity judgement
	def is_a_word(self,word):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				if i == len(word)-1:
					return tmp[char][0] == 1
				tmp = tmp[char][1]
			except:
				return False
