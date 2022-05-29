from sqlalchemy import table,MetaData, create_engine
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.sql.sqltypes import TIMESTAMP

engine = create_engine("postgresql://postgres:6755@localhost/postgres")
sessionLocal = sessionmaker(autocommit=False, autoflush = False, bind = engine)
Base = declarative_base()

USER_ID_SEQ = Sequence('user_id_seq')


class User(Base):
    __tablename__ = "myuser"

    uid = Column(Integer, USER_ID_SEQ, primary_key = True, server_default = USER_ID_SEQ.next_value())
    email = Column(String, nullable = False)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    time_created = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    
