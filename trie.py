#encoding:utf-8

import os,json,math

class Trie:
	def __init__(self):
		self.max_length = 4
		self.dic = {}

		if os.path.exists("trie.data"):
			#read from file
			with open("trie.data") as fd:
				self.dic = json.load(fd)
		else:
			#build trie tree
			self.buildTrie()

	# set probability
	def setProbability(self,dic):
		for key in dic:
			if dic[key][0] == 1:
				# print(dic[key][0],dic[key][2],sep="  ")
				dic[key][2] = -math.log2(dic[key][2] / self.total_count)
			self.setProbability(dic[key][1])

	# build Trie
	def buildTrie(self):
		self.total_count = 0

		with open("dict.txt",encoding="utf8",errors="ignore") as fd:
			line = fd.readline()
			while line is not '':
				line = line.strip()
				items = line.split(" ")
				self.putIntoDic(items[0],int(items[1]),items[2])
				self.total_count += int(items[1])
				line = fd.readline()

		self.setProbability(self.dic)

		# dump dictionary into file
		with open("trie.data","w") as fd:
			json.dump(self.dic,fd)

	#write a word to dic
	def putIntoDic(self,word,freq,p):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				if i == len(word)-1:
					tmp[char][0] = 1
					tmp[char] += [freq,p]
				else:
					tmp = tmp[char][1]
			except:
				if i == len(word)-1:
					tmp[char] = [1,{},freq,p]
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

	#positive match
	def positive_max_match(self,sentence):
		i=0
		j=i+self.max_length
		words = []
		while True:
			#print(sentence[i:j])
			if self.isAWord(sentence[i:j]):
				words.append(sentence[i:j])
				i = j
				j += self.max_length
			else:
				j -= 1
				if j==i+1:
					# print(words[i:j])
					words.append(sentence[i:j])
					i = j
					j += self.max_length
			if i>=len(sentence):
				break
			while j>len(sentence):
				j -= 1

		print(words)
		return words

	#nagetive match
	def nagetive_max_match(self,sentence):
		j = len(sentence)
		i = j - self.max_length
		words = []
		while True:
			#print(sentence[i:j])
			if self.isAWord(sentence[i:j]):
				#print(sentence[i:j])
				words.insert(0,sentence[i:j])
				j = i
				i -= self.max_length
			else:
				i += 1
				if i == j-1:
					words.insert(0,sentence[i:j])
					j = i
					i = j - self.max_length
			if j<= 0:
				break
			while i<0:
				i += 1

		return words

	def getFre(self,word):
		tmp = self.dic
		for i,char in enumerate(word):
			try:
				if i == len(word)-1:
					return tmp[char][2]
				else:
					tmp = tmp[char][1]
			except:
				print("word not exists")

				return None


	#all conditions will be acquired
	def all_cut(self,sentence):
		unknow_words = []

		length = len(sentence)
		cut_map = []

		for i in range(len(sentence)):
			tmp = []
			for j in range(i+1,i+self.max_length+1):
				if j > len(sentence):
					break
				if self.isAWord(sentence[i:j]):
					tmp.append(j)
			cut_map.append(tmp)

		# adjust cut map
		i = 0
		while i < len(sentence):
			if len(cut_map[i]) is 0:
				j = i
				for i in range(i+1,len(sentence)):
					if len(cut_map[i]) is 0:
						continue
					else:
						cut_map[j].append(i)
						unknow_words.append([j,i])

			i += 1

		# Dijkstra
		visited = set()
		visited.add(0)
		dis = [ math.inf for i in range(len(sentence)+1) ]
		pre = [ -1 for i in range(len(sentence)+1) ]

		# get distance with start node
		for item in cut_map[0]:
			pre[item] = 0;
			dis[item] = self.getFre(sentence[0:item])

		#print(cut_map)
		while True:
			min_number = math.inf
			min_index = 0
			for i in range(1,length+1):
				if i not in visited and dis[i] != math.inf:
					if(dis[i] < min_number):
						min_number = dis[i]
						min_index = i

			if min_index == length:
				break

			visited.add(min_index)
			for item in cut_map[min_index]:
				if self.getFre(sentence[min_index:item]) + dis[min_index] < dis[item]:
					pre[item] = min_index
					dis[item] = self.getFre(sentence[min_index:item]) + dis[min_index]

		result = []
		cur_position = length
		pre_position = pre[cur_position]
		while pre_position != -1:
			result.insert(0,sentence[pre_position:cur_position])
			cur_position = pre_position
			pre_position = pre[cur_position]

		return result

# testing example
# trie = Trie()
# with open("dict.txt",encoding="utf8",errors="ignore") as fd:
# 	line = fd.readline()
# 	while line is not '':
# 		line = line.strip()
# 		items = line.split(" ")
# 		print(trie.getFre(items[0]))
# 		line = fd.readline()
# result = trie.all_cut("中华人民共和国香港特别行政区")
# print(result)