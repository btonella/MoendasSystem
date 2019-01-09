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
	return render_template('dashboard.html')

@app.route('/cardapio.html')
def cardapio():
	return render_template('cardapio.html')

@app.route('/mesas.html')
def mesas():
	return render_template('mesas.html')


@app.route('/notifications.html')
def notifications():
	return render_template('notifications.html')

@app.route('/typography.html')
def typography():
	return render_template('typography.html')

@app.route('/users.html')
def users():
	return render_template('users.html')


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
