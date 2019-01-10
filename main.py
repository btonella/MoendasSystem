from flask import Flask, request, redirect, session, flash, send_from_directory, url_for, render_template
import pandas as pd

app = Flask(__name__, template_folder='.')
app.secret_key = "senha"

nomeUsuario = ""

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
	pedidosCSV = pd.read_csv("dataBase/pedidos.csv")
	pedidosCSV.VALOR = pedidosCSV.VALOR.astype(float)
	return render_template('pedidos.html', CSV=pedidosCSV, titulo="Pedidos", titulo_pagina="Pedidos")

@app.route('/mesas.html')
def mesas():
	mesasCSV = pd.read_csv("dataBase/mesas.csv")
	mesasCSV.TOTAL = mesasCSV.TOTAL.astype(float)
	pedidosCSV = pd.read_csv("dataBase/pedidos.csv")
	pedidosCSV.VALOR = pedidosCSV.VALOR.astype(float)
	pedidosCSV.MESA = pedidosCSV.MESA.astype(int)
	#pedidosCSV = pedidosCSV.groupby("MESA").VALOR.sum().reset_index()
	return render_template('mesas.html', CSVmesas=mesasCSV, CSVpedidos=pedidosCSV, titulo="Mesas", titulo_pagina="Mesas")


@app.route("/save.html")
def save():
	import time

	dia = str(time.time())
	pedidos = pd.read_csv("dataBase/pedidos.csv")
	pedidos.to_csv("dataBase/"+dia+".csv")
	return render_template("save.html", titulo="", titulo_pagina="Salvar")


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

