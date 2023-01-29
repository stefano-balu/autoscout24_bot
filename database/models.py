from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Extra simple table, used just to handle data persistence, not correctly mapped data types.
class AutoScout24(Base):
    __tablename__ = 'auto_scout24'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=True)
    year = Column(String, nullable=True)
    kilometers = Column(String, nullable=True)
    horsepower = Column(String, nullable=True)
    shift = Column(String, nullable=True)
    fuel = Column(String, nullable=True)
    fuel_consumption = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    owners = Column(String, nullable=True)
    co2 = Column(String, nullable=True)
    seller_type = Column(String, nullable=True)
    seller_location = Column(String, nullable=True)
    price_euro = Column(String, nullable=True)
    url = Column(String, nullable=True)
    classification = Column(String, nullable=True)
