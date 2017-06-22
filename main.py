from trie import Trie
from markov import Markov

trie = Trie()
result,unkow_words = trie.all_cut("今天天气真好")
print(result)
print("unknow words", unkow_words, sep=":")
for item in result:
    print(trie.isAWord(item))
markov = Markov()