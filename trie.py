#encoding:utf-8

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
					self.putIntoDic(word)

			self.save()

	#write a word to dic
	def putIntoDic(self,word):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				if i == len(word)-1:
					tmp[char][0] = 1
				tmp = tmp[char][1]
			except:
				if i == len(word)-1:
					tmp[char] = [1,{}]
				else:
					tmp[char] = [0,{}]
				tmp = tmp[char][1]

	#validity judgement
	def isAWord(self,word):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				if i == len(word)-1:
					return tmp[char][0] == 1
				tmp = tmp[char][1]
			except:
				return False

	#alter file encoding
	def alterFileEncoding(self,file_name):
		#read
		with open(file_name,encoding="gbk") as fd:
			text = fd.read()
		#rewrite
		with open(file_name,"w",encoding="utf8") as fd:
			fd.write(text)

	#add word from file
	def addFromFile(self,file_name):
		with open(file_name) as fd:
			for line in fd.readlines():
				line = line.strip()
				if "→" in line:
					tmp = line.split("→")
					self.putIntoDic(tmp[0])
					self.putIntoDic(tmp[1])
				else:
					self.putIntoDic(line)

		self.save()

	#write dic to file
	def save(self):
		with open("trie.data","w") as fd:
			json.dump(self.dic,fd)