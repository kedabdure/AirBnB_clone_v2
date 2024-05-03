#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

class DBStorage:
    """new engine for database"""
    __engine = None
    __session = None
    
    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls=None):
        """query on the current db session"""
        self.__session = sessionmaker(bind=self.__engine)
        if cls is None:
            obj = self.__session.query(State).all()
            obj.extend(self.__session.query(User).all())
            obj.extend(self.__session.query(Place).all())
            obj.extend(self.__session.query(City).all())
            obj.extend(self.__session.query(Amenity).all())
            obj.extend(self.__session.query(Review).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = cls.__session.query(cls).all()
            
        return {"{}.{}".format(type(obj), obj.id): obj for obj in objs}

    def new(self, obj):
        """add the obj to the current database"""
        self._session.add(obj)

    def save(self, obj):
        """commit the change to the database"""
        self.__session.commit(obj)

    def delete(self, obj=None):
        """delete from database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working sqlalchemy session"""
        self.__session.close()
