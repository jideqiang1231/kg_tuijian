from flask import Flask,render_template,request,redirect,url_for,json,jsonify,session
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.myEncoder import  MyEncoder
#根据用户id去推荐
from api.userid_to_movie import *
#连接数据库
from flask_sqlalchemy import SQLAlchemy
import data_process

app = Flask(__name__)

# #指定数据库连接还有库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/book?charset=utf8'
# #指定配置用来省略提交操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
DEBUG=True
#建立数据库对象
db = SQLAlchemy(app)
#建立数据库类，用来映射数据库表,将数据库的模型作为参数传入
class collection():
    #建立字段函数
    def __init__(self,userTel,seedId):
        self.userTel=userTel
        self.seedId=seedId
        # self.collectionId = collectionId
        #self.fertilizerId=fertilizerId
       # self.pesticideId=pesticideId
       # self.recommendId=recommendId
    def set(self):
        data = []
        for use,seed in zip(self.userTel,self.seedId,):
            d={
                'userTel': use,
                'seedId': seed,
                #'collectionId':col,
                #'fertilizerId':fer,
                #'pesticideId':pes,
                #'recommendId':rec
            }
            data.append(d)
        data_dic = {'result': data}
        return  json.dumps(data_dic)
class seed():
    #建立字段函数
    def __init__(self,id,name,type,url):
        self.id=id
        self.name=name
        self.type=type
        self.url=url

    def set(self):
        data = []
        for id,name,type,url in zip(self.id,self.name,self.type,self.url):
            d={
                'id': id,
                'name': name,
                'type':type,
                'url':url
            }
            data.append(d)
        data_dic = {'result': data}
        return  json.dumps(data_dic,ensure_ascii=False)

# 将用户历史写入csv
def w_collection_csv(a):
    a=json.loads(a)
    #a={"result": [{"seedId": 3, "userTel": "17863203236"}, {"seedId": 26, "userTel": "17863203236"}, {"seedId": 4, "userTel": "17863203236"}]}
    num=len(a['result'])
    userId=[i['userTel'] for i in a['result']]
    movieId=[i['seedId'] for i in a['result']]
    rating=[5.0 for i in range(num)]
    timestamp=[96547412 for i in range(num)]
    dataframe = pd.DataFrame({'userId':userId,'movieId':movieId,'rating':rating,'timestamp':timestamp})
    dataframe.to_csv("./test.csv",index=False,sep=',')
# 将推荐种子项目和推荐的具体名称写入csv
def w_seed_csv(a):
    a = json.loads(a)
    # a={"result": [{"seedId": 3, "userTel": "17863203236"}, {"seedId": 26, "userTel": "17863203236"}, {"seedId": 4, "userTel": "17863203236"}]}
    num = len(a['result'])
    ID = [i['id'] for i in a['result']]
    name = [i['name'] for i in a['result']]
    type = [i['type'] for i in a['result']]
    url = [i['url'] for i in a['result']]
    dataframe = pd.DataFrame({'movie_id': ID, 'title': name, 'genres': type,'imgUrl':url})
    dataframe.to_csv("./seed_info.csv", index=False, sep=',')

@app.route('/db_test',methods=['GET'])
def dbtest():
    a=data_process.select()
    #a=collection.query.all()
    # data=[]
    #collectionId=[i[0] for i in a]
    userTel=[i[0] for i in a]
    seedId=[i[1] for i in a]
    #fertilizerId=[i[3] for i in a]
    #pesticideId=[i[4] for i in a]
    #recommendId=[i[5] for i in a]
    b = collection(userTel,seedId)
    #data_dic={'result':data}
    # for everycollection in a:
    #    for item in everycollection.__dict__.items():s
    #        xyz.append(item)
    #for evrtycollection in a:
     #   print ('\n'.join(['%s:%s' % item for item in evrtycollection.__dict__.items()]))
    w_collection_csv(b.set())
    return b.set()

@app.route('/db_seed',methods=['GET'])
def dbseed():
    a=data_process.selectseed()
    #a=collection.query.all()
    # data=[]
    #collectionId=[i[0] for i in a]
    id=[i[0] for i in a]
    name=[i[1] for i in a]
    type = [i[2] for i in a]
    url = [i[3] for i in a]
    #fertilizerId=[i[3] for i in a]
    #pesticideId=[i[4] for i in a]
    #recommendId=[i[5] for i in a]
    b = seed(id,name,type,url)
    #data_dic={'result':data}
    # for everycollection in a:
    #    for item in everycollection.__dict__.items():s
    #        xyz.append(item)
    #for evrtycollection in a:
     #   print ('\n'.join(['%s:%s' % item for item in evrtycollection.__dict__.items()]))
    w_seed_csv(b.set())
    print(b.set())
    return b.set()

@app.route('/xxx', methods=['GET', 'POST'])
def read(filename):
    with open(filename,'r',encoding='utf-8') as r:
        item=r.read()
    return item

@app.route('/')
def hello_world():
    result=''
    return render_template('tuijian.html',content=result)

@app.route('/tuijian')
def tuijian():
    result=''
    return render_template('tuijian.html',content=result)


@app.route('/recommend',methods=['GET', 'POST'])
def ajax():
    rating_file = 'data/ml-latest-small/ratings.csv'
    # 获取url中？后边的数据值
    user_id= (request.get_data())

    userCF = UserBasedCF()
    # 得到评分数据集
    userCF.get_dataset(rating_file)
    # 计算相似度
    userCF.calc_user_sim()
    # user_id = '99' 进行实验评估
    final_result = userCF.evaluate(user_id)
    print(final_result)  # 三个电影的名称

    final_result='；'.join(final_result)
    return jsonify({'recommend_data': final_result})
    #return jsonify({"message": "ok", "url": "127.0.0.1:5000", 'id':user_id,'event_get': final_result})

@app.route('/myrecommend',methods=['GET', 'POST'])
def recommend():
    # 将collection表的所有内容写入csv,./test.csv
    a = data_process.select()
    userTel = [i[0] for i in a]
    seedId = [i[1] for i in a]
    b = collection(userTel, seedId)
    w_collection_csv(b.set())
    # 将seed表的id对应的内容content写入csv,./seed_info.csv
    a = data_process.selectseed()
    id = [i[0] for i in a]
    name = [i[1] for i in a]
    type = [i[2] for i in a]
    url = [i[3] for i in a]
    b = seed(id,name,type,url)
    w_seed_csv(b.set())

    # print(b.set())
    rating_file = './test.csv'
    # 获取url中？后边的数据值
    user_id= (request.get_data())

    userCF = UserBasedCF()
    # 得到评分数据集
    userCF.get_dataset(rating_file)
    # 计算相似度
    userCF.calc_user_sim()
    # user_id = '99' 进行实验评估
    final_result,final_result_id,url = userCF.evaluate(user_id)
    print(final_result)  # 三个电影的名称
    print(final_result_id)
    print(url)
    #final_result='；'.join(final_result)
    #final_result_id='；'.join(final_result_id)
    data=[]
    for id,result,image_url in zip(final_result_id,final_result,url):
        dic={}
        dic['seed_id']=id
        dic['seed_name']=result
        dic['image_url']=image_url
        data.append(dic)
    final_data={}
    final_data['seed_result']=data
    result=json.dumps({'recommend_data': final_data},ensure_ascii=False)
    return result
if __name__ == '__main__':
    app.run(port=8080)
