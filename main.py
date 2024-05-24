from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

### Classes ###

class novoAnuncioObjeto:
    def __init__(self, nome, valor, descricao):
        self.nome = nome
        self.valor = valor
        self.descricao = descricao

### Listas ###

listaDeProdutos = []
listaDeNovosAnuncios = []

### Rotas e Funções Gerais ###

@app.route("/")
def base():
    return render_template("templatebase.html")

@app.route("/signIn")
def signIn():    
    return render_template('signIn.html')

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/minhaConta")
def minhaConta():

    # Aqui deverá haver uma função que verifica que o usuário esta logado, sendo que caso não esteja logado o usuário deve ser redirecionado para a tela de login signIn. Caso logado, o usuário deve ser redirecionado a sua conta pessoal instanciada.
    
    return render_template("minhaconta.html")

@app.route("/sobreOProjeto")
def sobreOProjeto():
    return render_template("sobreOProjeto.html")
    
@app.route("/vender", methods=['GET', 'POST'])
def vender():
    if request.method == 'POST':
        nome = request.form.get('nomeDoProduto')
        valor = request.form.get('valorDoProduto')
        descricao = request.form.get('descricaoDoProduto')
        novoProduto = novoAnuncio(nome, valor, descricao)       
        listaDeProdutos.append(novoProduto)
        return render_template('templatebase.html')
    return render_template('vender.html')

@app.route("/meusAnuncios")
def meusAnuncios():
    return render_template("meusAnuncios.html", listaDeProdutos=listaDeProdutos)

### Funções Para Conexão Com o Bando de Dados MySQL WorkBench ###

@app.route("/novoUsuario", methods=['POST'])
def novoUsuario():
    
    user = request.form.get("user")
    password = request.form.get("password")
    confirmaPassword = request.form.get("confirmaPassword")

    if (password != confirmaPassword):
        return render_template("signUp.html")
    else:    
        try:
            conexao = mysql.connector.connect (
            host='localhost', 
            database='usuariosCadastrados', 
            user='root', 
            password='123456'
        )
    
            inserirNovoUsuario = f'INSERT INTO usuariosCadastrados (user, password) VALUES ("{user}", "{password}")'
    
    
            cursor = conexao.cursor()
            cursor.execute(inserirNovoUsuario)
            conexao.commit()
            print(cursor.rowcount, "Registros inseridos na tabela!")
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conexao.is_connected()):
                conexao.close()
                print("Conexão ao MySQL finalizada")
    
        return render_template("signIn.html")

@app.route("/novoAnuncio", methods=['POST'])
def novoAnuncio():

    nome = request.form.get("nomeDoProduto")
    valor = request.form.get("valorDoProduto")
    descricao = request.form.get("descricaoDoProduto")
   
    try:
        conexao = mysql.connector.connect (
        host='localhost', 
        database='produtosCadastrados', 
        user='root', 
        password='123456'
    )

        inserirNovoProduto = f'INSERT INTO produtosCadastrados (nomeDoProduto, valorDoProduto, descricaoDoProduto) VALUES ("{nome}", "{valor}", "{descricao}")'


        cursor = conexao.cursor()
        cursor.execute(inserirNovoProduto)
        conexao.commit()
        print(cursor.rowcount, "Registros inseridos na tabela!")
        cursor.close()
    except Error as erro:
        print("Falha ao inserir dados no MySQL: {}".format(erro))
    finally:
        if (conexao.is_connected()):
            conexao.close()
            print("Conexão ao MySQL finalizada")

    return render_template("templatebase.html")

if __name__ == '__main__':
  app.run()
