#!/usr/bin/python3
""" State Module for HBNB project """
import shlex
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
# from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    # if getenv('HBNB_TYPE_STORAGE') == 'db':
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", cascade='all, delete, delete-orphan', backref="state")

    @property
    def cities(self):
        """ Getter attribute that returns City instances """
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                lista.append(var[key])
        for elem in lista:
            if (elem.state_id == self.id):
                result.append(elem)
        return (result)
