#!/usr/bin/python3
""" Database storage engine """

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """ Database storage engine """

    __engine = None
    __session = None

    def __init__(self):
        """ Initializes a new DBStorage instance """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, database),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Queries all objects depending on the class name """
        from models.base_model import BaseModel
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        objects = {}
        classes = [BaseModel, Amenity, City, Place, Review, State, User]

        if cls is None:
            classes = [cls for cls in classes if cls is not None]
        else:
            classes = [cls]

        for cls in classes:
            query = self.__session.query(cls)
            for obj in query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """ Adds the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes obj from the current database session """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and creates a new session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Closes the current session """
        self.__session.close()
