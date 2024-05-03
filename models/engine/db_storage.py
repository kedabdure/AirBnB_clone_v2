from sqlalchemy import create_engine
from os import getenv
from base_model import Base


class DBStorage:
    """new engine for database"""
    __engine = None
    __session = None
    
    def __init__(self):
        """inistancialion"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                    pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
            
        def all(self, cls=None)
            """query on the current db session"""
            if cls is None:
                session.query(cls)
            