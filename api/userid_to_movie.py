# coding = utf-8

# 基于用户的协同过滤推荐算法实现
import random

import math
from operator import itemgetter
import pandas as pd


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的5个用户，为其推荐10部电影
        self.n_sim_user = 5#20
        self.n_rec_movie = 10#10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.movie_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded movie number = %d' % self.n_rec_movie)


    # 读文件得到“用户-电影”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):#加载ratings表中对应的用户id，movieID
            user, movie, rating, timestamp = line.split(',')
            #得到数据的训练集和测试集
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][movie] = rating#对应的用户对应的电影对应的评分数
                #数据格式'1':{'231':'5.0','12':'1.3'}
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)
        train=self.trainSet
        test=self.testSet
        # for key,value in self.trainSet.items():
        #     print(key,value)
        # #输出训练集和测试集中的对应的id
        # #print("trainSet_len 包含的userID是%s"%list(self.trainSet)[0:20])
        # print("*"*50)

        # print("testSet_len 包含的userID是%s" % self.trainSet)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)


    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“电影-用户”倒排索引
        # key = movieID, value = list of userIDs who have seen this movie
        print('Building movie-user table ...')
        movie_user = {}
        for user, movies in self.trainSet.items():
            print(user,movies)
            for movie in movies:#movies是一个字典，遍历每一个key
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)#字典中放置字典，形式是电影id：用户ID
        print('Build movie-user table success!')

        self.movie_count = len(movie_user)#查看电影ID中的长度
        print('Total movie number = %d' % self.movie_count)
        print('Build user co-rated movies matrix ...')
        #遍历电影用户字典
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated movies matrix success!')
        juzhen=self.user_sim_matrix
        # 计算相似性
        print('Calculating user similarity matrix ...')
        middle_value=self.user_sim_matrix
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')


    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user#找到
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for movie in self.trainSet[v]:
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv

        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]#返回的是一个元祖，分别是电影的id,用户相似度评分


    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self,user):
        print("Evaluation start ...")
        N = self.n_rec_movie
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_movies = set()
        # 改成种子对应的信息
        movie_file='./seed_info.csv'
        # movie_file='data/ml-latest-small/movies.csv'
        for i, user, in enumerate(self.trainSet):
            # user='56'
            test_movies = self.testSet.get(user, {})
            rec_movies = self.recommend(user)#针对目标用户去推荐电影id，用户的id通过接口去使用
            print("目标用户推荐%s"%rec_movies)#rec_movies是推荐的三部电影
            ## 找到与目标用户兴趣相似的5个用户，为其推荐3部电影
            id_list = []
            for tuple in rec_movies:
                movie_id = tuple[0]
                # print(movie_id)
                id_list.append(movie_id)
            #根据这三个id去寻找对应的电影名字
            df_movies=pd.read_csv(movie_file,encoding='utf-8')
            alldata = df_movies.loc[:, :].values
            movie_name=[]
            # print(id_list)
            single=0
            for item in id_list:
                for data in alldata:
                    # print(data[0])
                    # print(type(data[0]))
                    if item==str(data[0]):
                        movie_name.append(data[1])
                        single=1
                        break
                if single==1:
                    pass
                else:
                    movie_name.append('null')
            url = []
            # print(id_list)
            single_image = 0
            for item in id_list:
                for data in alldata:
                    # print(data[0])
                    # print(type(data[0]))
                    if item == str(data[0]):
                        url.append(data[3])
                        single_image = 1
                        break
                if single_image == 1:
                    pass
                else:
                    url.append('null')
            return movie_name,id_list,url
            # for movie, w in rec_movies:#遍历对应的电影id和相似度矩阵中的分数
            #     if movie in test_movies:
            #         hit += 1
            #     all_rec_movies.add(movie)
            # rec_count += N
            # test_count += len(test_movies)
        # precision = hit / (1.0 * rec_count)
        # recall = hit / (1.0 * test_count)
        # coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        # print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))

if __name__ == '__main__':

    rating_file = 'data/ml-latest-small/ratings.csv'

    userCF = UserBasedCF()
    userCF.get_dataset(rating_file)#得到评分数据集
    userCF.calc_user_sim()#计算相似度
    user_id='99'
    final_result=userCF.evaluate(user_id)#进行实验评估
    print(final_result)#三个电影的名称
    pass


        # for item in tuple:
        #     movie_id=item[0]
        #     print(movie_id)
    # result=[tuple for tuple in final_result]
    # print(result[0][0])
    #将得到的对应的三个电影Id去拿到去找到对应的电影的名字，去movies中查找
