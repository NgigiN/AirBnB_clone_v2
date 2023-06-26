#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'

        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", cascade='all, delete, delete-orphan', backref="state")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """ Initializes a new State instance """
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """ Getter attribute that returns City instances """
            city_instances = models.storage.all("City").values()
            return [
                city for city in city_instances if city.state_id == self.id]
