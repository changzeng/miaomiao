#encoding:utf-8

from markov import Markov
from trie import Trie

trie = Trie()
markov = Markov()

trie.positive_max_match("淄博市中级人民法院指定该案由张店区法院管辖")
trie.nagetive_max_match("淄博市中级人民法院指定该案由张店区法院管辖")
cut_map = trie.all_cut("淄博市中级人民法院指定该案由张店区法院管辖")
#print(cut_map)