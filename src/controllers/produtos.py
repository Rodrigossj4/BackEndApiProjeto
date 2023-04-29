from typing import Optional
from flask import request, make_response,jsonify
from src.server.instance import server
from flask_pydantic_spec import Response, Request
from pydantic import BaseModel
import psycopg2   
 
conn = psycopg2.connect(database="ecommerce", 
                        user="postgres",
                        password="123456", 
                        host="localhost", port="5432")
    
    
class Produto(BaseModel):
    id: Optional[int]
    nome: str
    idSecao: str
    preco: str  
    
class Produtos(BaseModel): 
    Produtos:list[Produto] 

class Erro(BaseModel):
    status:int
    msg:str 
    
@server.app.get('/Produtos')
@server.api.validate(resp=Response(HTTP_200=Produtos),tags=['Produtos'])
def getProdutos():
    """
    Retorna todos os produtos da base de dados

    """ 
    cursor =  conn.cursor()
    cursor.execute('SELECT id, nome, preco, idSecao FROM PRODUTOS Where ativa = true')
    produtos =  cursor.fetchall()
        
    cursor.close()
       
    produtosVO = list()
    for pd in produtos:
        produtosVO.append({
            'id':pd[0],
            'nome':pd[1],
            'preco':pd[2] ,
            'idSecao':pd[3]
        })
        
    return make_response(
    jsonify(Produtos(Produtos=produtosVO).dict()))   

@server.app.post('/Produtos')
@server.api.validate(body=Request(Produto), resp=Response(HTTP_200=Produto, HTTP_400=Erro,  HTTP_500=Erro),tags=['Produtos'])
def postProduto():
    """
    Insere um produto da base de dados

    """ 
    try:
        
        body = request.context.body.dict()
        produto = request.json
        
        if produto['nome'] == "":
            return make_response(
            jsonify(Erro(status=400, msg="O nome do pruduto não pode ser vazio").dict())), 400
       
        if len(produto['nome']) < 3:
            return make_response(
                jsonify(Erro(status=400, msg="Nome do produto deve ter mais de 2 caracteres. Verifique os parêmetros enviados").dict())), 400
        
        if produto['idSecao'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
        
        if produto['idSecao'] == "0":
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
                               
        if type(int(produto['idSecao'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
        
        if produto['preco'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Preço do produto não especificado. Verifique os parêmetros enviados").dict())), 400
            
        cursor =  conn.cursor()
        sql = f"INSERT INTO PRODUTOS(NOME,PRECO, IDSECAO) VALUES('{produto['nome']}', {produto['preco']}, {produto['idSecao']})"
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return  body
    
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Houve um erro ao cadastrar o produto").dict())), 500

@server.app.put('/Produtos')
@server.api.validate(body=Request(Produto), resp=Response(HTTP_200=Produto, HTTP_400=Erro,  HTTP_500=Erro),tags=['Produtos'])
def putProduto():
    """
    Atualiza um produto da base de dados

    """
    try:     
        body = request.context.body.dict()
        produto = request.json
        
        if produto['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto não especificado. Verifique os parêmetros enviados").dict())), 400
        
        if produto['id'] == 0:
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto não especificado. Verifique os parêmetros enviados").dict())), 400
                               
        if type(int(produto['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto inválido. Verifique os parêmetros enviados").dict())), 400
       
        if produto['nome'] == "":
                return make_response(
                jsonify(Erro(status=400, msg="O nome do pruduto não pode ser vazio").dict())), 400
        
        if len(produto['nome']) < 3:
            return make_response(
                jsonify(Erro(status=400, msg="Nome do produto deve ter mais de 2 caracteres. Verifique os parêmetros enviados").dict())), 400
            
        if produto['idSecao'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
            
        if produto['idSecao'] == "0":
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
                                
        if type(int(produto['idSecao'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Seção não especificada. Verifique os parêmetros enviados").dict())), 400
            
        if produto['preco'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Preço do produto não especificado. Verifique os parêmetros enviados").dict())), 400
            
        cursor =  conn.cursor()
        sql = f"UPDATE PRODUTOS SET NOME = '{produto['nome']}', PRECO = {produto['preco']} , IDSECAO = {produto['idSecao']} WHERE ID = {produto['id']}"
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return make_response(
            jsonify(body))
        
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Houve um erro ao atualizar o produto").dict())), 500

@server.app.delete('/Produtos')
@server.api.validate(body=Request(Produto), resp=Response(HTTP_200=Produto, HTTP_400=Erro,  HTTP_500=Erro),tags=['Produtos'] )
def deleteProduto():
    """
    Deleta um produto da base de dados

    """
    try:    
        body = request.context.body.dict()
        produto = request.json
        
        if produto['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto não especificado. Verifique os parêmetros enviados").dict())), 400
        
        if produto['id'] == 0:
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto não especificado. Verifique os parêmetros enviados").dict())), 400
                               
        if type(int(produto['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id do produto inválido. Verifique os parêmetros enviados").dict())), 400
       
        cursor =  conn.cursor()
        sql = f"DELETE FROM PRODUTOS WHERE ID = {produto['id']}"
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return make_response(
            jsonify(body)) 
    
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Houve um erro ao excluir o produto").dict())), 500    
