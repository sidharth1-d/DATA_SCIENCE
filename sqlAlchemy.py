from sqlalchemy import Column, create_engine,Integer,String,Float
from sqlalchemy.orm  import declarative_base,sessionmaker
engine = create_engine('sqlite:///sqlalchemy_test.db',echo = True)

Base = declarative_base()

class player(Base):

    __tablename__ = 'players'

    jerNo = Column(Integer,primary_key = True)
    playerName = Column(String(100))
    avg = Column(Float)

Base.metadata.create_all(engine)
print("step 4 complete : table 'players' created using an  ORM model !")