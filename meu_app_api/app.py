from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": CarroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: CarroSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    produto = Produto(
        nome=form.nome,
        ano=form.ano,
        valor=form.valor)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
       
        session = Session()
       
        session.add(produto)
        
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_carros(produto), 200

    except IntegrityError as e:
      
        error_msg = "carro de mesmo nome na base :/"
        logger.warning(f"Erro ao adicionar carro '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        
        error_msg = "Não foi possível salvar novo carro :/"
        logger.warning(f"Erro ao adicionar carro '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemCarrosSchema, "404": ErrorSchema})
def get_produtos():
    
    logger.debug(f"Coletando produtos ")
  
    session = Session()
    
    produtos = session.query(Produto).all()

    if not produtos:
       
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        
        print(produtos)
        return apresenta_carros(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_produto(query: CarroBuscaSchema):
    
    produto_id = query.id
    logger.debug(f"Coletando dados sobre Automóvel #{produto_id}")
    
    session = Session()
    
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
      
        error_msg = "Automóvel não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Automóvel encontrado: '{produto.nome}'")
        
        return apresenta_carros(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": CarroDelSchema, "404": ErrorSchema})
def del_produto(query: CarroBuscaSchema):
    
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre Automóvel #{produto_nome}")
    
    session = Session()
  
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Automóvel removido", "id": produto_nome}
    else:
        
        error_msg = "Automóvel não encontrado na base :/"
        logger.warning(f"Erro ao deletar Automóvel #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


