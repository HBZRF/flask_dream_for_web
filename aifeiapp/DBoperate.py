# --------------连接数据库----------###2222
from sqlalchemy import create_engine,update,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func



HOSTNAME = '111.229.253.42'
PORT = '3306'
DATABASE = 'dreamapp'
USERNAME = 'dreamapp'
PASSWORD = 'Aifei12345!'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD, HOSTNAME, PORT, DATABASE)
engine = create_engine(DB_URI)
# ------------声明映像-----------------
# 表名 ，字段名，类型，约束
# 类 属性
Base = declarative_base(engine)
# ----------创建数据表对应的类-----------
class table_User(Base):
    __tablename__ = 'user'
    UserUid = Column(String(255),primary_key = True)
    PassWord = Column(String(255),nullable=False)
    PhoneNumber = Column(String(255))
    Email = Column(String(255))
    RegistrationTime = Column(DateTime)
    children = relationship("table_Post", back_populates="parent")
    # def to_dict(self):
    #     model_dict = dict(self.__dict__)
    #     del model_dict['_sa_instance_state']
    #     return model_dict
    # Base.to_dict = to_dict # 若是使用的flask_sqlalchemy,则改写成: db.to_dict = to_dict
class table_Post(Base):
    __tablename__ = 'post'
    PostUid = Column(String(50),primary_key = True)
    AuthorUid = Column(String(255), ForeignKey('user.UserUid'))
    parent = relationship("table_User", back_populates="children")
    CreateTime = Column(DateTime)
    LastModifyTime = Column(DateTime)
    PostTitle = Column(String(150),nullable=False)
    PostContent = Column(String(150), nullable=False)

class table_ThumbsUp(Base):
    __tablename__ = 'thumbsup'
    RowId = Column(String(255),primary_key = True)
    AuthorUid = Column(String(255),nullable=False)
    PostUid = Column(String(50),nullable=False)
    Attitude = Integer()

#Base.metadata.create_all()
mysql_Session = sessionmaker(engine)
mysql_Session = mysql_Session()



if __name__ == '__main__':
    pass

    
    
