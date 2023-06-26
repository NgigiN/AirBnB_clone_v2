#!/usr/bin/python3
"""This module defines the City class"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of a city"""
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if models.storage_type == 'db':
        places = relationship("Place", backref="cities", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """Initializes a new City instance"""
        super().__init__(*args, **kwargs)

    if models.storage_type != 'db':
        @property
        def places(self):
            """Returns the list of Place instances with city_id equals to the
            current City.id"""
            return [place for place in models.storage.all("Place").values()
                    if place.city_id == self.id]
