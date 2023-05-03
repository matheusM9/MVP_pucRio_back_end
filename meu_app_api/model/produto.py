from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Carro(Base):
    tablename = 'carro'

id = Column("pk_carro", Integer, primary_key=True)
nome = Column(String(140), unique=True)
ano = Column(Integer)
valor = Column(Float)
data_insercao = Column(DateTime, default=datetime.now())



def __init__(self, nome:str, ano:int, valor:float,
             data_insercao:Union[DateTime, None] = None):
    
    self.nome = nome
    self.ano = ano
    self.valor = valor

   
    if data_insercao:
        self.data_insercao = data_insercao


