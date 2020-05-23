# --------------连接数据库----------###2222
from sqlalchemy import create_engine,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import pymysql
HOSTNAME = '111.229.253.42'
PORT = '3306'
DATABASE = 'dream'
USERNAME = 'root'
PASSWORD = 'Feiloveying99!'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD, HOSTNAME, PORT, DATABASE)
engine = create_engine(DB_URI)
# ------------声明映像-----------------
# 表名 ，字段名，类型，约束
# 类 属性
Base = declarative_base(engine)
# ----------创建数据表对应的类-----------
class table_Goods(Base):
    __tablename__ = 'goods'
    TurnId = Column(Integer)
    goodcode = Column(Integer)
    SerialNumber = Column(String(50),primary_key = True)
    factory = Column(String(50))
    Brand = Column(String(50))
    Color = Column(String(50))
    Standards = Column(String(50))
    shizai = Column(Float(10))
    UnitPrice = Column(Float(10))
    OrderId = Column(String(50),nullable=False)
    owener = Column(Integer)
    TotalSoldRmb = Column(Float(10))
    TotalSoldGh = Column(Float(10))
    issold = Column(Integer)
    gooduid = Column(String(50))
    GoodsType = Column(String(50))
    EstimatePrice = Column(Integer)
    Pic1Name1 = Column(String(200))
    Pic1Name2 = Column(String(200))
    ishaspic = Column(Integer)
    saler = Column(String(200))
    SoledPrice = Column(Float(10))
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
    # 或者使用如下的这种
    #def to_dict(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class IcomeOrder(Base):
    __tablename__ = 'IcomeOrder'
    OrderId = Column(String(50),primary_key = True)
    transportionfee = Column(Float(10))
    TurnId = Column(Integer)
    real_paid = Column(Float(10))
    factory = Column(String(50))
class table_MyCart(Base):
    __tablename__ = 'MyCart'
    usr_id = Column(String(50),primary_key = True)
    goodcode = Column(Integer,primary_key = True)
    buyamount = Column(Integer)
    EstimatePrice = Column(Float)
    UnitPrice = Column(Float)
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
class table_Order(Base):
    __tablename__ = 'Order'
    rowid = Column(Integer,primary_key = True)
    usr_id = Column(String(50))
    orderuid = Column(String(50))
    goodcode = Column(Integer,)
    UnitPrice = Column(Float)
    amount = Column(Integer)
    timestp = Column(Integer,)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
class table_Order_summary(Base):
    __tablename__ = 'OrderSummary'
    rowid = Column(Integer,primary_key = True)
    usr_id = Column(String(50))
    turnid = Column(Integer)
    orderuid = Column(String(50))
    delivery_fee_from_factory = Column(Float)
    delivery_fee_to_agent = Column(Float)
    delivery_fee_China_to_abord = Column(Float)
    delivery_fee__custom_to_Seller = Column(Float)
    other_fee = Column(Float)
    isclosed = Column(Integer)
    timestp = Column(String(50))
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
class user(Base):
    __tablename__ = 'usr'
    usr_id = Column(String(50), primary_key = True)
    pwd = Column(String(50), nullable=False)
    usr_type = Column(String(10))
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
class deliverinfo(Base):
    __tablename__ = 'deliverinfo'
    turnid = Column(Integer,primary_key = True)
    InteriorTransportationCHN = Column(Float(10))
    duty_fee = Column(Float(10))
    transportation_CHN_to_GH = Column(Float(10))
    InteriorTransportationGH = Column(Float(10))

class table_Goodinfo(Base):
    __tablename__ = 'goodinfo'
    goodcode = Column(Integer,primary_key = True)
    factory = Column(String(250))
    Brand = Column(String(250))
    Color = Column(String(250))
    Standards = Column(String(250))
    shizai = Column(Float(102))
    UnitPrice = Column(Float(102))
    CustomPrice = Column(Float(102))
    GoodsType = Column(String(250))
    EstimatePrice = Column(Integer)
    Pic1Name1 = Column(String(200))
    Pic1Name2 = Column(String(200))
    ishaspic = Column(Integer)
    OrderId = Column(String(200))
    GoodsTitle = Column(String(200))
    TypeOfLace = Column(String(200))
    HairStyle = Column(String(200))
    Category = Column(String(200))
    Density = Column(Integer)
    Length = Column(Integer)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
    # 或者使用如下的这种
    #def to_dict(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Session = sessionmaker(engine)
session = Session()
# 查


def mysql_get_count_info(**filters):
    rs = session.query(func.count(table_Goodinfo.goodcode)).filter_by(**filters).scalar()
    session.close()
    return rs

def mysql_get_count_goods_info(**filters):
    rs = session.query(func.count(table_Goods.SerialNumber)).filter_by(**filters).scalar()
    session.close()
    return rs
def mysql_get_info_limit(table,limit,offset,**filters):
    rs = session.query(table).filter_by(**filters).limit(limit).offset(offset).all()
    session.close()
    return rs


def mysql_get_info(table,filters):
    try:
        rs = session.query(table).filter_by(**filters).all()
        return rs
    except Exception as e:
        print(e)
    finally:
        session.close()
#改

def mysql_get_mycart_execsql(usr_type,filters):
    if usr_type == 'admin':
        sql = 'SELECT *  FROM ( SELECT a.usr_id,a.goodcode,a.buyamount,b.UnitPrice FROM MyCart a,goodinfo b WHERE a.goodcode = b.goodcode ) d LEFT JOIN ( SELECT usr_id sub_usr_id, sum( buyamount * UnitPrice ) totalmoney FROM MyCart GROUP BY usr_id ) c ON d.usr_id = c.sub_usr_id'
    else:
        sql = 'SELECT *  FROM ( SELECT a.usr_id,a.goodcode,a.buyamount,b.UnitPrice FROM MyCart a,goodinfo b WHERE a.goodcode = b.goodcode and a.usr_id = "{usr_id}") d LEFT JOIN ( SELECT usr_id sub_usr_id, sum( buyamount * UnitPrice ) totalmoney FROM MyCart GROUP BY usr_id ) c ON d.usr_id = c.sub_usr_id'.format(**filters)
    try:
        rs = session.execute(sql)
        return rs
    except Exception as e:
        print(e)
    finally:
        session.close()
def mysql_get_order_overview_execsql(usr_type,filters):
    if usr_type == 'admin':
        sql = 'SELECT * from OrderSummary '
    else:
        sql = 'SELECT * from OrderSummary a WHERE  a.usr_id = "{usr_id}"'.format(
            **filters)
    try:
        rs = session.execute(sql)
        return rs
    except Exception as e:
        print(e)
    finally:
        session.close()
def mysql_get_order_info_execsql(usr_type,filters):
    if usr_type == 'admin':
        sql = 'SELECT *  FROM ( SELECT a.usr_id,a.orderid,a.goodcode,a.UnitPrice,a.amount FROM `Order` a where   a.orderid = "{uid}"  ) d LEFT JOIN ( SELECT orderid sub_orderid, sum( amount * UnitPrice ) totalmoney FROM `Order` GROUP BY orderid ) c ON d.orderid = c.sub_orderid LEFT JOIN (select GoodsType,goodcode res_goodcode from goodinfo ) z on z.res_goodcode = d.goodcode'.format(**filters)
    else:
        sql = 'SELECT *  FROM ( SELECT a.usr_id,a.orderid,a.goodcode,a.UnitPrice,a.amount FROM `Order` a WHERE a.usr_id = "{usr_id}" and a.orderid = "{uid}" ) d LEFT JOIN ( SELECT orderid sub_orderid, sum( amount * UnitPrice ) totalmoney FROM `Order` GROUP BY orderid ) c ON d.orderid = c.sub_orderid LEFT JOIN (select GoodsType,goodcode res_goodcode from goodinfo ) z on z.res_goodcode = d.goodcode '.format(**filters)

    try:
        rs = session.execute(sql)
        return rs
    except Exception as e:
        print(e)
    finally:
        session.close()
def mysql_update_info(rs,key_value_dict):
    try:
        for i in rs:
            for key,value in key_value_dict.items():
                a = 'i.%s = "%s"'%(key,value)
                print(a)
                exec(a)
            session.add(i)
            session.commit()
            return '信息添加成功！'
    except Exception as e:
        session.rollback()
        return str(e)
    finally:        
        session.close()
#增
def mysql_add_info(table,key_value_dict):
    try:
        tb = table(**key_value_dict)
        session.add(tb)
        session.commit()
        return '信息添加成功！'

    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()
def mysql_del_info(table,key_value_dict):
    try:
        rss = session.query(table).filter_by(**key_value_dict).all()
        for rs in rss:
            session.delete(rs)
        session.commit()
        return '删除成功！！'
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()
def MyCart_handel(usr,goodcode,nbr,action = 1):
    filters = {'usr_id':usr,'goodcode':goodcode}
    rs = session.query(table_MyCart).filter_by(**filters).all()
    key_value_dict = {'usr_id': usr, 'goodcode': goodcode, 'buyamount': nbr}
    if action:#默认增加数量
        if not rs:
            key_value_dict = {'usr_id':usr,'goodcode':goodcode,'buyamount':nbr}
            res = mysql_add_info(table_MyCart, key_value_dict)
            if res == '信息添加成功！':
                return {'status':'ok','info':res}
            else:
                return {'status':'nok','info':res}
        else:
            beforenbr = int(rs[0].buyamount)
            afternbr = beforenbr + int(nbr)
            key_value_dict['buyamount'] = afternbr
            res = mysql_update_info(rs, key_value_dict)
            if res == '信息添加成功！':
                return {'status': 1,'info':res}
            else:
                return {'status': 0,'info':res}


def mysql_ordercreate_execsql(username, Turnid,time_str,orderid):

    sql = '''INSERT INTO `Order` select  saler, "{orderid}" as "orderuid",serialnumber, goodcode, UnitPrice, null as "soldprice", "{time_str}" as "timestp",Turnid as "turnid",0 as "issold" from goods WHERE saler = "{username}" and TurnId = "{Turnid}" '''.format(orderid=orderid,time_str=time_str,Turnid=Turnid,username=username)
    print(sql)
    try:
        sql_del = '''DELETE FROM `Order` WHERE usr_id = "{username}" and turnId = "{Turnid}" '''.format(Turnid=Turnid, username=username)
        rs = session.execute(sql_del)  # 删除垃圾数据
        rs = session.execute(sql)#生成订单
        #下面生成订单概览，首先需要删除可能有的垃圾数据
        sql_del = '''DELETE FROM `OrderSummary`  WHERE usr_id = "{username}" and TurnId = "{Turnid}"'''.format(Turnid=Turnid, username=username)

        rs = session.execute(sql_del)  # 删除垃圾数据
        sql = '''INSERT INTO  `OrderSummary` 
(usr_id,turnid,timestp,isclosed,orderuid,goodcost) 
select  usr_id, "{Turnid}" as "turnid" , timestp,0 as "isclosed" ,orderuid,sum(UnitPrice) as goodcost
from `Order` WHERE usr_id = "{username}" and orderuid = "{orderid}" and timestp = "{time_str}"
GROUP BY usr_id ,orderuid,turnid'''.format(orderid=orderid, time_str=time_str, Turnid=Turnid, username=username)
        rs = session.execute(sql)  # 生成订单概览
        return '处理成功！！'
    except Exception as e:
        return str(e)
    finally:
        session.close()


if __name__ == '__main__':
    a = {'SerialNumber':'20051','TurnId' : '2'}
    key_value_dict = {'SerialNumber':'20051','TurnId' : 25,'issold':1}
    a = get(Goods,a)
    update(a,key_value_dict)
    
    
    
