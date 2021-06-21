import pymysql

    # 打开数据库连接
conn = pymysql.connect( host="localhost", user="root", password="",
                 database="register")
    # 使用 cursor() 方法创建一个游标对象 cursor
    # 使用 execute()  方法执行 SQL 查询
def select():
	cursor = conn.cursor()
	sql = """SELECT * FROM mytable;"""
	conn.commit()
	cursor.execute(sql)
	data=cursor.fetchall()
	cursor.close()
	return (len(data))
#从数据库中根据账号查询出所有的信息并返回
def select_all(zh):
	cursor = conn.cursor()
	sql = """SELECT * FROM mytable where zh=%s;"""%zh
	conn.commit()
	cursor.execute(sql)
	data = cursor.fetchall()
	cursor.close()
	return data
	pass
def insert(name,password,phone,mail,zh):
	cursor = conn.cursor()
	befor_length=select()+1
	sql = """SELECT * FROM xg where date='%s';"""%(name)
	conn.commit()
	cursor.execute(sql)
	data=cursor.fetchall()	
	num=len(data)
	if num==0:
		sql = """INSERT INTO mytable values('%s', '%s',  %s,  '%s','%s');"""%(name,password,phone,mail,zh)
		conn.commit()
		cursor.execute(sql)
	# 使用 fetchone() 方法获取单条数据.
		after_length=select()
	#输出查询的数据：
		cursor.close()
		if after_length == befor_length:
			return True
	else:
		return False
	#关闭数据库连接
def login(zh,password):
	cursor = conn.cursor()
	sql = """SELECT * FROM mytable where zh='%s' and mima='%s';"""%(zh,password)
	conn.commit()
	cursor.execute(sql)
	data=cursor.fetchall()
	cursor.close()
	if data:
		return  True

#删除数据库表中的账户信息
def delete_mytable(zh):
	try:
		cursor = conn.cursor()
		sql = """delete * FROM mytable where zh='%s';""" % (zh)
		conn.commit()
		cursor.execute(sql)
		data = cursor.fetchall()
		cursor.close()
		return "删除成功"
	except Exception as e:
		return "删除数据失败"

#进行个人信心的修改
def  alter_information(nc,zh,password,phone,mail):
	"""
	根据账号去修改个人信息
	:param zh:
	:return:
	"""
	# print(zh)
	# print(password)
	# print(phone)
	# print(mail)
	# a=zh
	try:
		cursor = conn.cursor()
		#将数据的插入
		sql = """UPDATE mytable set nc='%s',mima='%s',phone='%s',mail='%s'  where  zh='%s' ;""" % (nc,password,phone,mail,zh)
		#sql = "UPDATE mytable set nc={0},mima={1},phone={2},mail={3}  where  zh={4} ;" .format(nc,password,phone,mail,zh)
		#sql = """UPDATE mytable set nc='%s,mima=%s,phone=%s,mail=%s  where  zh='%s' ;""" % (nc,password,phone,mail,zh)
		conn.commit()
		cursor.execute(sql)
		"""
		下面是测试数据库中的值是否是实时更新了
		"""
		# sql = """SELECT * FROM mytable where zh='%s' ;""" % (zh)
		# conn.commit()
		# cursor.execute(sql)
		# data=cursor.fetchall()
		# print(data)
		#
		# cursor.close()
		# a=data
		#
		return True
	except Exception as e:
		return  False
#将不同用户的不同的动作信息插入到数据库中
def zhuce_insertAction(zh):
	#根据账号去插入到对应的表中
	try:
		cursor = conn.cursor()
		#根据注册后的账号初始化动作表
		sit,run,squat,tumble,walk=0,0,0,0,0#初始化都是0
		sql = """INSERT INTO action values('%s','%s', '%s',  %s,  '%s','%s');"""%(zh,sit,run,squat,tumble,walk)
		conn.commit()
		cursor.execute(sql)
		data = cursor.fetchall()
		cursor.close()
		return True
	except Exception as e:
		return False

#查询数据库mytable表中的所有信息，得到所有的用户的信息
def serarch_mytable():
	try:
		cursor = conn.cursor()
		sql = """SELECT * FROM mytable  ;"""
		conn.commit()
		cursor.execute(sql)
		data=cursor.fetchall()
		# print(data)
		cursor.close()
		return data#返回的是一个tuple类型
	except Exception as e:
		print(Exception)



#根据用户信息去数据库中去查找数据
def select_action(zh):
	cursor = conn.cursor()
	sql = """SELECT * FROM action where zh='%s' ;""" % zh
	conn.commit()
	cursor.execute(sql)
	data=cursor.fetchall()
	# print("查到的动作信息是%s"%data)
	cursor.close()
	return data[0]

#根据用户信息和上传的文件测试的结果动态更新动作表中的值
def update_action(zh,action):
	cursor = conn.cursor()
	sql = """SELECT * FROM action where zh='%s' ;""" % zh
	conn.commit()
	cursor.execute(sql)
	data = cursor.fetchall()
	print(data)
	# print("查到的动作信息是%s" % data[0])
	# cursor.close()
	#sit，run,squat,tumble,walk
	#更新数据库之前，需要把账户中的五个动作值取出来，然后执行加一操作
	get_sit=data[0][1]
	get_run=data[0][2]
	get_squat=data[0][3]
	get_tumble=data[0][4]
	get_walk=data[0][5]
	# print(type(get_run))
	if action=='sit':
		new_get_sit= int(get_sit) + 1
		new_get_sit = str(new_get_sit)
		sql = """UPDATE action set sit=%s  where  zh='%s' ;""" % (new_get_sit,zh)
		conn.commit()
		cursor.execute(sql)
	elif action=='run':
		new_get_run=int(get_run)+1
		# print(new_get_run)
		# print(type(new_get_run))
		new_get_run=str(new_get_run)
		# print(new_get_run)
		sql = """UPDATE action set run=%s  where  zh='%s' ;""" %(new_get_run,zh)
		conn.commit()
		cursor.execute(sql)
	elif action=='squat':
		new_get_squat=int(get_squat)+1
		sql = """UPDATE action set squat=%s  where  zh='%s' ;""" % (new_get_squat,zh)
		conn.commit()
		cursor.execute(sql)
	elif action=='tumble':
		new_get_tumble=int(get_tumble)+1

		sql = """UPDATE action set tumble=%s  where  zh='%s' ;""" % (new_get_tumble,zh)
		conn.commit()
		cursor.execute(sql)
	else:
		new_get_walk = int(get_walk) + 1
		sql = """UPDATE action set walk=%s  where  zh='%s' ;""" % (new_get_walk,zh)
		conn.commit()
		cursor.execute(sql)

	#更新完之后继续查询取得最新的值可视化到前端
	cursor = conn.cursor()
	sql = """SELECT * FROM action where zh='%s' ;""" % zh
	conn.commit()
	cursor.execute(sql)
	data = cursor.fetchall()
	print("查到的动作信息是%s" % data)
	cursor.close()
	return data[0]

if __name__ == '__main__':
	print(insert('a','123','11111111111','111','12345678912'))
	#print(login('12345678912','123'))
	#print(select())
	#login('xxx','xx')