import xlrd,json,math

book1 = xlrd.open_workbook("CorpusWordlist.xls")
book2 = xlrd.open_workbook("CorpusWordPOSlist.xls")

sheet1 = book1.sheet_by_index(0)
sheet2 = book2.sheet_by_index(0)

fre_dict = {}

for i in range(7,sheet1.nrows):
	word = sheet1.cell_value(i,1)
	freq = sheet1.cell_value(i,3)
	fre_dict[word] = -math.log2(freq)

with open("trie.data") as fd:
	trie = json.load(fd)

for key in fre_dict:
	tmp = trie
	for i,char in enumerate(key):
		if i==len(key)-1:
			try:
				tmp = tmp[char]
			except:
				tmp[char] = [1,{}]
				tmp = tmp[char]
			try:
				tmp[2] = fre_dict[key]
			except:
				tmp.append(fre_dict[key])
		else:
			try:
				tmp = tmp[char][1]
			except:
				tmp[char] = [0,{}]

with open("trie.data",'w') as fd:
	json.dump(trie,fd)