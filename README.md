### MiaoMiao

As the first step of NLP.Word segmentation is one of the most import part of Chinese word segmentation.There have a lot of way to do this work.In this project I have implemented a word segmenter based on **Hidden Markov Model**.  
In fact,this project was inspired by jieba which is a Chinese word segmentation tool.Sometimes I was wondering how jieba implement this segmentation process.But since I had written this project I had got a lot of knowledge about this filed.  
Let's take a look at how jieba was implemented.First jieba uses a word dictionary cut the text into word map and then it uses a DP algorithm to choose the cut result with highest probability.If a word was not found in the dictionary then jieba uses **Hiddent Markov Model** to recognize unknow words.

#### Build Trie Tree



#### Build Cut Map



#### Using Dijkstra To Find Highest Cut Result



#### Markov Recognize Unknow Words


