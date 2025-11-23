from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class amazonProductSchema(Base):
    __tablename__ = 'amazon_product_data'
    
    id = Column(Integer, primary_key=True, index=True)
    product_link = Column(String)
    title = Column(String)
    brand = Column(String)
    discount = Column(Float)
    avg_rating = Column(Float)
    total_ratings = Column(Integer)
    availability = Column(String)
    category = Column(String)
    price = Column(Float)