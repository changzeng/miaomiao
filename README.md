## MiaoMiao

As the first step of NLP.Word segmentation is one of the most import part of Chinese word segmentation.There have a lot of way to do this work.In this project I have implemented a word segmenter based on **Hidden Markov Model**.  
In fact,this project was inspired by jieba which is a Chinese word segmentation tool.Sometimes I was wondering how jieba implement this segmentation process.But since I had written this project I had got a lot of knowledge about this filed.  
Let's take a look at how jieba was implemented.First jieba uses a word dictionary cut the text into word map and then it uses a DP algorithm to choose the cut result with highest probability.If a word was not found in the dictionary then jieba uses **Hiddent Markov Model** to recognize unknow words.  

### Funny Things
In the beginning,I was using my own dictionary.But that dicionary was very very terrble result in this program has a very very low accuracy and had made this program looks like a toy but not a practical tool.In a few mounth,I recognized that wouldn't be my mistake but the data.So I changed the data and then it works pretty much better.

### Build Trie Tree
Trie tree is a very effective data structure for string matching.We used **Trie Tree** here to obtain the frequence of a given Chinese word.

### Build Cut Map
I used Trie Tress as a dicionary to cut sentence into a number of words.First program try every possible way of word segmentation.I set a current position to denote the start of a word and then uses a offest to denote the end of a word.If a word is an unknow word his next node list will be empty.So we can use this feature to recgnize unknow words and pass this words to **Markov Model**.

### Using Dijkstra
After obtained the cut map.I used Dijkstra algorithm to chose the most possible cut result.The parameter of this markov model was not trained by myself but from jieba since training a markov model is expensive and I don't have enough time.

### Markov Recognize Unknow Words
This part was implemented by using viterbi algorithm.
