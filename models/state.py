#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")


if getenv("HBNB_TYPE_STORAGE") != "db":

    @property
    def cities(self):
        """cities def property"""
        from models import storage

        twin_cities = []  # just linked cities lol
        city_list = storage.all(City)
        for city in city_list.values():
            if city.state_id == self.id:
                twin_cities.append(city)
        return twin_cities
