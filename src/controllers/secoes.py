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

class Secao(BaseModel):
    id: Optional[int]
    nome: str
    
class Secoes(BaseModel):    
    Secoes:list[Secao] 
    
class Erro(BaseModel):
    status:int
    msg:str  

@server.app.get('/Secoes')
@server.api.validate(resp=Response(HTTP_200=Secoes),tags=['Secoes'])
def get():
    """
    Retorna todas as seções da base de dados

    """  
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM SECAO Where ativa = true')
    secoes =  cursor.fetchall()
    cursor.close()
     
    secoesVO = list()
    for sc in secoes:
        secoesVO.append({
            'id':sc[0],
            'nome':sc[1]    
        })
        
    return make_response(
        jsonify(Secoes(Secoes=secoesVO).dict()))


def retorna_produtos(id):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM PRODUTOS WHERE idSecao = ' + id )
    produtos=  cursor.fetchall()
    cursor.close()
    
    return len(produtos)    
    

@server.app.post('/Secoes')
@server.api.validate(body=Request(Secao), resp=Response(HTTP_200=Secao, HTTP_400=Erro,  HTTP_500=Erro),tags=['Secoes'])
def post():
    """
    Insere uma seção da base de dados

    """  
    try:
        body = request.context.body.dict()
        secao = request.json
    
        if secao['nome'] != "":
            cursor =  conn.cursor()
            sql = f"INSERT INTO SECAO(NOME) VALUES('{secao['nome']}')"
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return  body        
      
        return make_response(
        jsonify(Erro(status=400, msg="Não foi possível incluir a Seção. Verifique os parêmetros enviados").dict())), 400
       
    
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Houve um erro grave com a aplicação").dict())), 500
    

@server.app.put('/Secoes')
@server.api.validate(body=Request(Secao), resp=Response(HTTP_200=Secao, HTTP_400=Erro,  HTTP_500=Erro), tags=['Secoes'])
def put(): 
    """
    Atualiza a seção da base de dados

    """     
    try:
       
        body = request.context.body.dict()
        secao = request.json
        
        if secao['nome'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Não é possível atualizar o nome da Seção. Verifique os parêmetros enviados").dict())), 400
       
        if len(secao['nome']) < 3:
            return make_response(
                jsonify(Erro(status=400, msg="Nome da Seção deve ter mais de 2 caracteres. Verifique os parêmetros enviados").dict())), 400
       
        if secao['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção não especificado. Verifique os parêmetros enviados").dict())), 400
        
        if secao['id'] == 0:
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção não especificado. Verifique os parêmetros enviados").dict())), 400
                               
        if type(int(secao['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção inválido. Verifique os parêmetros enviados").dict())), 400
       
        
        cursor =  conn.cursor()
        sql = f"UPDATE SECAO SET NOME = '{secao['nome']}' WHERE ID = {secao['id']}"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
            
        return make_response(
            jsonify(body))
        
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Houve um erro durante a atualização").dict())), 500    


@server.app.delete('/Secoes')
@server.api.validate(body=Request(Secao), resp=Response(HTTP_200=Secao, HTTP_400=Erro,  HTTP_500=Erro),tags=['Secoes'])
def delete():
    """
    Deleta a seção da base de dados

    """     
    try:
        body = request.context.body.dict()
        secao = request.json
        secoes = retorna_produtos(secao['id'])
       
        if secao['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção não especificado. Verifique os parêmetros enviados").dict())), 400
        
        if secao['id'] == "0":
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção não especificado. Verifique os parêmetros enviados").dict())), 400
                               
        if type(int(secao['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção inválido. Verifique os parêmetros enviados").dict())), 400
       
       
        if  secoes > 0:
            return make_response(
                jsonify(Erro(status=400, msg="Não é possível excluir pois existem produtos vinculados").dict())), 400
       
        cursor =  conn.cursor()
        sql = f"DELETE FROM SECAO WHERE ID = {secao['id']}"
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return make_response(
            jsonify(body))
        
    except Exception as e:
        return make_response(
        jsonify(Erro(status=500, msg="Existem produtos vinculados a essa seção. Não é possível excluir.").dict())), 500 
        
