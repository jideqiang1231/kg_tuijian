#from pyecharts.charts import Bar,Pie,Line,Map
#from pyecharts import options as opts
import pymysql
conn = pymysql.connect( host="localhost", user="root", password="123456",
                 database="book")
def get_time():
	cursor = conn.cursor()
	sql = """SELECT date FROM xg;"""
	cursor.execute(sql)
	conn.commit()
	data=cursor.fetchall()
	cursor.close()
	return data
	#return (len(data))

def select():
	cursor = conn.cursor()
	sql = """SELECT user_tel,seed_id FROM collection where seed_id is not null;"""
	cursor.execute(sql)
	conn.commit()
	data=cursor.fetchall()
	cursor.close()
	return (data)

def selectseed():
	cursor = conn.cursor()
	sql = """SELECT seed_id,seed_name,seed_type,seed_image FROM seed ;"""
	cursor.execute(sql)
	conn.commit()
	data=cursor.fetchall()
	cursor.close()
	return (data)


def insert(date1,qz,wzz,lc,bscsqz,xzcy,qslj,jwsr,mqzy):
	cursor = conn.cursor()
	befor_length=select()+1
	sql = """INSERT INTO xg values('%s','%s','%s','%s','%s','%s','%s','%s','%s');"""%(date1,qz,wzz,lc+'市',bscsqz,xzcy,qslj,jwsr,mqzy)
	cursor.execute(sql)
	conn.commit()
	after_length=select()
	cursor.close()
	if after_length == befor_length:
			return True
	# 使用 fetchone() 方法获取单条数据.
	#输出查询的数据：
	else:
		False

def query(date):
	cursor = conn.cursor()
	sql = """SELECT * FROM xg where date='%s';"""%(date)
	cursor.execute(sql)
	conn.commit()
	data = cursor.fetchall()
	cursor.close()
	return data

def to_mysql():
	with open('./clean_data.txt','r',encoding='utf-8-sig') as f:
		line=f.readlines()
	l=[]
	d={}
	for i in line:
		if i!='\n':
			if len(i.split(':'))!=1:
				d[i.split(':')[0]]=i.split(':')[1].strip('\n')
			else:
				d[i.split('：')[0]]=i.split('：')[1]
		else:
			l.append(d)
			d={}
	for i in l:
		if i!={}:
			insert(i['日期'],i['确诊病例'],i['无症状感染者'],i['报告城市'],i['报告城市确诊数'],i['新增出院'],i['全省累计报告新冠肺炎确诊病例'],i['全省累计报告新冠肺炎确诊病例（境外输入）'],i['目前在院'])

def generate_map(sj):
	data1=query(sj)
	date={}
	for d in data1:
		if '报告城市' not in date:
			if d[3]!='无市':
				date['报告城市']=[d[3]]
				date['确诊病例']=[d[1]] if d[1] !="" else [0]
		else:
			date['报告城市'].append(d[3])
			date['确诊病例'].append(d[1])
	if date !={}:
		data={sj:date}
		c = (
    	Map()
    	.add(sj, [[ii,int(jj)] for ii,jj in zip(data[sj]['报告城市'],data[sj]['确诊病例'])], "广东")
    	.set_global_opts(
        	title_opts=opts.TitleOpts(title='确诊病例'), visualmap_opts=opts.VisualMapOpts()
  	  	)
		).render('./static/{}_map.html'.format(sj))

def generate_content(sj):
	data1=query(sj)
	date={}
	for d in data1:
		if '报告城市' not in date:
			date['报告城市']=[d[3]]
			date['确诊病例']=[d[1]] if d[1] !="" else [0]
			date['无症状感染者']=[d[2]]
			date['报告城市确诊数']=[d[4]]
			date['新增出院']=[d[5]]
			date['全省累计报告新冠肺炎确诊病例']=[d[6]]
			date['境外输入']=[d[7]]
			date['目前在院']=[d[8]]
		else:
			date['报告城市'].append(d[3])
			date['确诊病例'].append(d[1])
			date['无症状感染者'].append(d[2])
			date['报告城市确诊数'].append(d[4])
			date['新增出院'].append(d[5])
			date['全省累计报告新冠肺炎确诊病例'].append(d[6])
			date['境外输入'].append(d[7])
			date['目前在院'].append(d[8])
	return date	
	#for d in data1:
	#	if d[3] not in data:
	#return 

def get_all_time():
	s=sorted(list(set([i[0] for i in get_time()])))
	return(s)
#print(selectseed())