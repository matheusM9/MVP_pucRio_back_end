from pydantic import BaseModel
from typing import Optional, List
from model.produto import Carro

from schemas import ComentarioSchema

class CarroSchema(BaseModel):

 nome: str = "Fiat Uno"
 ano: Optional[int] = 2010
 valor: float = 15000.00

class CarroBuscaSchema(BaseModel):

 nome: str = "modelo"

class ListagemCarrosSchema(BaseModel):
 
 carros:List[CarroSchema]

def apresenta_carros(carros: List[Carro]):

 result = []
 for carro in carros:

  result.append({
   "nome": carro.nome,
   "ano": carro.ano,
   "valor": carro.valor,
})

 return {"carros": result}
class CarroViewSchema(BaseModel):
 
 id: int = 1
 nome: str = "Fiat Uno"
 ano: Optional[int] = 2010
 valor: float = 15000.00
 total_cometarios: int = 1
 comentarios:List[ComentarioSchema]

class CarroDelSchema(BaseModel):

  mesage: str
  nome: str

def apresenta_carro(carro: Carro):

 return {
"id": carro.id,
"nome": carro.nome,
"ano": carro.ano,
"valor": carro.valor,
"total_cometarios": len(carro.comentarios),
"comentarios": [{"texto": c.texto} for c in carro.comentarios]
}
class CarroViewSchema(BaseModel):

 id: int = 1
 nome: str = "Fiat Uno"
 ano: Optional[int] = 2010
 valor: float = 15000.00
 total_cometarios: int = 1
 comentarios:List[ComentarioSchema]

class CarroDelSchema(BaseModel):

 mesage: str
 nome: str

def apresenta_carro(carro: Carro):

 return {
"id": carro.id,
"nome": carro.nome,
"ano": carro.ano,
"valor": carro.valor,
"total_cometarios": len(carro.comentarios),
"comentarios": [{"texto": c.texto} for c in carro.comentarios]
}