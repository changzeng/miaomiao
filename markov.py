import json,time,os
import numpy as np
from random import randint
from math import log2

class Markov:
    #确定每一个字在emit_matrix中的序列号
    def get_emit_index(self):
        #--发射矩阵索引
        self.emit_index = {}
        with open("new_train.data") as fd:
            self.str = fd.read()
            
        #这个数字用来显示索引和进度
        index = 0
        while self.str != '':
            self.emit_index[self.str[0]] = index
            self.str = self.str.replace(self.str[0],'')
            index += 1
            print("get character index "+str(index))
        
        #--汉字集合的大小
        self.emit_num = index

    #初始化markov模型的所有参数
    def initial_parameter(self):
        self.MIN = -1e100;
        #初始状态矩阵
        self.pi = np.array([-1.0,self.MIN,self.MIN,-1.0])
        #如果存在文件
        if os.path.exists("markov.data"):
            with open("markov.data") as fd:
                markov = json.load(fd)
                self.emit_index = markov["emit_index"]
                self.emit_num = markov["emit_num"]
                self.state_num = markov["state_num"]
                self.state_index = markov["state_index"]
                self.emit_matrix = np.array(markov["emit_matrix"])
                self.transfer_matrix = np.array(markov["transfer_matrix"])
        else:
            #获得索引
            self.get_emit_index()
            #--状态索引
            self.state_num = 4
            #---状态数目
            self.state_index = {'B':0,'M':1,'E':2,'S':3}
            self.index_to_state = {0:'B',1:'M',2:'E',3:'S'}
            #--初始化发射矩阵
            self.emit_matrix = self.get_random_matrix(self.state_num,self.emit_num)
            #--状态转移矩阵
            self.transfer_matrix = self.get_random_matrix(self.state_num,self.state_num)
        #读入数据并计算长度
        with open("new_train.data") as fd:
            self.str = np.array(list(fd.read()))
            self.str_length = len(self.str)

    #返回一个和为1的随机向量
    def get_random_matrix(self,r,c):
        vector = []
        #总量
        RANGE = 100000000*c

        for i in range(r):
            #剩余量
            LEFT = RANGE
            tmp = []
            for j in range(c-1):
                #-----------------------------------------------#
                tmp_int = randint(1,int(2*LEFT/(c-j)))
                LEFT = LEFT - tmp_int
                tmp.append(log2(tmp_int/RANGE))
            tmp.append(log2(LEFT/RANGE))
            vector.append(tmp)

        return np.array(vector)

    #训练
    def train(self):
        #前序矩阵
        a = np.zeros((self.state_num,self.str_length),dtype=np.float64)
        #后序矩阵
        b = np.zeros((self.state_num,self.str_length),dtype=np.float64)

        #初始化前后向变量
        a[:,0] = self.pi + self.emit_matrix[:,self.emit_index[self.str[0]]]
        b[:,self.str_length-1] = 0

        progress = 1
        #计算前后向变量
        for i in range(1,self.str_length):
            print("calculate forward and backward matrix "+str(progress)+"/"+str(self.str_length))
            progress += 1
            for j in range(self.state_num):
                #计算向前变量
                tmp = a[:,i-1]+self.transfer_matrix[j,:]
                a[j,i] = self.add(tmp)+self.get_emit_probability(j,i)
                #计算向后变量
                tmp = b[:,self.str_length-i]+self.get_emit_probability(-1,i)+self.transfer_matrix[j,:]
                b[j,self.str_length-i-1] = self.add(tmp)

        #初始化条件矩阵概率
        progress = 1
        self.condition_matrix = np.zeros((self.str_length-1,self.state_num,self.state_num))
        self.probability = np.zeros((self.state_num,self.str_length-1))
        #计算条件概率
        for i in range(self.str_length-1):
            print("calculate condition matrix "+str(progress)+"/"+str(self.str_length-1))
            progress += 1
            for j in range(self.state_num):
                for k in range(self.state_num):
                    #待优化
                    self.condition_matrix[i,j,k] = a[j,i]+self.transfer_matrix[j,k]+self.get_emit_probability(k,i+1)+b[k,i+1]
                
            self.condition_matrix[i,:,:] -= self.add(self.condition_matrix[i,:,:])
            for k in range(self.state_num):
                self.probability[k,i] = self.add(self.condition_matrix[i,k,:])
                
        self.probability_sum = np.zeros((self.state_num,1))
        for i in range(self.state_num):
            print("calculate condition probability's summary "+str(i+1)+"/"+str(self.state_num))
            self.probability_sum[i,0] = self.add(self.probability[i,:])
    
        #重新估计transfer_matrix和emit_matrix
        for i in range(self.state_num):
            #重新估计transfer_matrix
            progress = 1
            for j in range(self.state_num):
                self.transfer_matrix[i,j] = self.add(self.condition_matrix[:,i,j]) - self.probability_sum[i,0]
                progress += 1

        #重新估计emit_matrix
        progress = 1
        for key in self.emit_index:
            print("calculate emit matrix "+str(progress)+"/"+str(self.emit_num))
            key_index = self.emit_index[key]

            bool_array_1 = self.str[:-1] == key
            bool_array_2 = (bool_array_1 == False)*self.MIN*-1
            bool_array = bool_array_1 + bool_array_2

            progress += 1
            for i in range(self.state_num):
                self.emit_matrix[i,key_index] = self.add((bool_array)*self.probability[i,:]) - self.probability_sum[i,0]
        
        for i in range(self.state_num):
            print(self.add(self.transfer_matrix[i,:]))
            print(self.add(self.emit_matrix[i,:]))

        print(self.transfer_matrix)
        print(self.emit_matrix)
        input()

    #将ndarray中各元素相加
    def add(self,array):
        return array.max()+log2((2**(array-array.max())).sum())

    #获得发射概率 i为状态序号 j为字符在字符串中的序号
    def get_emit_probability(self,i,j):
        #如果i为-1则返回结果为所有状态到序列为j的字符的发射概率
        if i == -1:
            return self.emit_matrix[:,self.emit_index[self.str[j]]]
        else:
            return self.emit_matrix[i,self.emit_index[self.str[j]]]

    #转换为list
    def to_list(self,array):
        result = []
        for item in list(array):
            result.append(list(item))
        return result

    #分词
    def cut(self,string):
        #维特比算法的临时数组
        tmp = np.zeros((len(string),self.state_num))
        #记录父节点
        parents = np.zeros((len(string),self.state_num))
        parents[0,:] = -1
        tmp[0,:] = self.pi + self.emit_matrix[:,item_index]
        #维特比算法向前
        for i in range(len(string)-1):
            for j in range(self.state_num):
                former = tmp[i-1,:]+self.transfer_matrix[:,j]
                tmp[i,j] = former.max()+self.emit_index[j,string[i]]
                parents[i,j] = self.max_index(former)
        #维特比算法向后
        previous = self.max_index(tmp[-1,:])
        state_chain = self.index_to_state[previous]
        for i in list(range(1,len(string)))[::-1]:
            previous = tmp[i,previous]
            state_chain += self.index_to_state[previous]
        state_chain = state_chain[::-1]

    #返回最大值索引
    def max_index(self,array):
        max_value = array.max()
        for i in range(len(array)):
            if max_value == array[i]:
                return i

        return -1

    #将数据写入文件
    def save(self):
        markov = {}
        markov["emit_index"] = self.emit_index
        markov["emit_num"] = self.emit_num
        markov["state_num"] = self.state_num
        markov["state_index"] = self.state_index
        markov["emit_matrix"] = self.to_list(self.emit_matrix)
        markov["transfer_matrix"] = self.to_list(self.transfer_matrix)
        with open("markov.data","w") as fd:
            json.dump(markov,fd)
        
markov = Markov()
markov.initial_parameter()
while True:
    markov.train()
    markov.save()
