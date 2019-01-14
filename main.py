from flask import Flask, request, redirect, session, flash, send_from_directory, url_for, render_template
import pandas as pd
import sqlite3


app = Flask(__name__, template_folder='.')
app.secret_key = "senha"

nomeUsuario = ""


#Banco de dados
conn = sqlite3.connect("dataBase/database.db")
cursor = conn.cursor()

@app.route('/')
def initial():
	return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
	return render_template('dashboard.html', titulo="Dashboard", titulo_pagina="Dashboard")

@app.route('/cardapioComidas.html')
def cardapio1():
	cardapioComidas = pd.read_csv("dataBase/cardapioComidas.csv")
	cardapioComidas.PREÇO = cardapioComidas.PREÇO.astype(float)
	return render_template('cardapioComidas.html', cardapioCSV=cardapioComidas, titulo="", titulo_pagina="Cardapio Comidas")

@app.route('/cardapioBebidas.html')
def cardapio2():
	cardapioBebidas = pd.read_csv("dataBase/cardapioBebidas.csv")
	cardapioBebidas.PREÇO = cardapioBebidas.PREÇO.astype(float)
	return render_template('cardapioBebidas.html', cardapioCSV=cardapioBebidas, titulo="", titulo_pagina="Cardapio Bebidas")

@app.route('/cardapioCachacas.html')
def cardapio3():
	cardapioCachacas = pd.read_csv("dataBase/cardapioCachacas.csv")
	cardapioCachacas.PREÇO = cardapioCachacas.PREÇO.astype(float)
	return render_template('cardapioCachacas.html', cardapioCSV=cardapioCachacas, titulo="" , titulo_pagina="Cardapio Cachaças")

@app.route('/pedidos.html')
def pedidos():

	cursor.execute(""" SELECT * FROM pedidos """)
	linhas = cursor.fetchall()
	cursor.close()
	nomes = {"id": 0,
		"mesa": 1,
		"comanda": 2,
		"pedido": 3,
		"quantidade": 4,
		"valor": 5}

	mesas_ativas = []
	for linha in linhas:
		mesas_ativas.append(linha[nome["mesa"]])
	mesas_ativas = sorted(set(mesas_ativas))
	#pedidosCSV = pd.read_csv("dataBase/pedidos.csv")
	#pedidosCSV.VALOR = pedidosCSV.VALOR.astype(float)
	return render_template('pedidos.html', dados=linhas, nomes=nomes, mesas_ativas=mesas_ativas, titulo="Pedidos", titulo_pagina="Pedidos")

@app.route('/mesas.html')
def mesas():

	#mesasCSV = pd.read_csv("dataBase/mesas.csv")
	#mesasCSV.TOTAL = mesasCSV.TOTAL.astype(float)
	#pedidosCSV = pd.read_csv("dataBase/pedidos.csv")
	#pedidosCSV.VALOR = pedidosCSV.VALOR.astype(float)
	#pedidosCSV.MESA = pedidosCSV.MESA.astype(int)
	#pedidosCSV = pedidosCSV.groupby("MESA").VALOR.sum().reset_index()
	return render_template('mesas.html', dados=linhas, database=database, titulo="Mesas", titulo_pagina="Mesas")


@app.route("/save.html")
def save():
	import time

	dia = str(time.time())
	pedidos = pd.read_csv("dataBase/pedidos.csv")
	pedidos.to_csv("dataBase/"+dia+".csv")
	return render_template("save.html", titulo="", titulo_pagina="Salvar")


@app.route("/nova_venda.html")
def novaVenda():
	#IMPORT DOS CARDAPIOS
	cardapioComidas = pd.read_csv("dataBase/cardapioComidas.csv")
	cardapioComidas.PREÇO = cardapioComidas.PREÇO.astype(float)
	cardapioCachacas = pd.read_csv("dataBase/cardapioCachacas.csv")
	cardapioCachacas.PREÇO = cardapioCachacas.PREÇO.astype(float)
	cardapioBebidas = pd.read_csv("dataBase/cardapioBebidas.csv")
	cardapioBebidas.PREÇO = cardapioBebidas.PREÇO.astype(float)
	
	#IMPORT DAS COMANDAS ABERTAS
	cursor.execute(""" SELECT * FROM pedidos """)
	linhas = cursor.fetchall()
	cursor.close()
	nomes = {"id": 0,
		"mesa": 1,
		"comanda": 2,
		"pedido": 3,
		"quantidade": 4,
		"valor": 5}

	comandas_ativas = []
	for linha in linhas:
		comandas_ativas.append(linha[nome["comanda"]])
	comandas_ativas = sorted(set(comandas_ativas))

	return render_template("nova_venda.html", titulo="Nova Venda", titulo_pagina="Nova Venda", comidas=cardapioComidas, bebidas=cardapioBebidas, cachacas=cardapioCachacas, comandas_ativas=comandas_ativas)


@app.route("/salvar_venda_nova", methods=["POST",])
def salvar_venda_nova():
	mesaEscolhida = request.form["mesas"]
	
	if request.form["comandaNova"] == None and request.form["comandaAberta"] == None:
		flash("Erro, falta de informações")
		return redirect ("/nova_venda.html")

	elif request.form["comandaNova"] == None:
		comandaEscolhida = request.form["comandaAberta"]
	else:
		comandaEscolhida = request.form["comandaNova"]

	if request.form["bebidas"] == None and request.form["comidas"] == None and request.form["cachacas"] == None:
		flash("Erro, falta de informações")
		return redirect ("/nova_venda.html")

	elif request.form["bebidas"] == None and request.form["comidas"] == None:
		pedidoEscolhido = request.form["cachacas"]

	elif request.form["bebidas"] == None and request.form["cachacas"] == None:
		pedidoEscolhido = request.form["comidas"]

	elif request.form["comidas"] == None and request.form["comidas"] == None:
		pedidoEscolhido = request.form["bebidas"]

	quantidadeEscolhida = request.form["quantidade"]

	cursor.execute("""
		INSERT INTO pedidos (mesa, comanda, pedido, quantidade, valor)
		VALUES (mesaEscolhida, comandaEscolhida, pedidoEscolhido, quantidadeEscolhida, 0)
		""")
	return redirect("/pedidos.html")


#Faz todos os htmls funcionarem
@app.route('/<path:path>')
def send_path(path):
	return send_from_directory('.', path)


@app.route("/autenticar", methods=["POST",])
def autenticar():
	if request.form["username"] == "admin" and request.form["password"] == "admin":
		session["usuario_logado"] = request.form["username"]
		nomeUsuario = "admin"
		#flash(request.form["username"] + " logou com sucesso")
		return redirect("/dashboard.html")
	
	elif (request.form["username"] == "aurea" or request.form["username"] == "Aurea") and request.form["password"] == "071029":
		session["usuario_logado"] = request.form["username"]
		nomeUsuario = "Aurea"
		return redirect("/dashboard.html")
	
	elif (request.form["username"] == "marcio" or request.form["username"] == "Márcio" or request.form["username"] == "Marcio") and request.form["password"] == "071029":
		session["usuario_logado"] = request.form["username"]
		nomeUsuario = "Márcio"
		return redirect("/dashboard.html")
	
	else:
		flash("Usuário ou senha não existem")
		return redirect("/")

