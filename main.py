from flask import Flask, request, redirect, session, flash, send_from_directory, url_for, render_template
import pandas as pd


app = Flask(__name__, template_folder='.')
app.secret_key = "senha"

@app.route('/')
def bla():
	return render_template('index.html')

#Faz todos os htmls funcionarem
@app.route('/<path:path>')
def send_path(path):
	return send_from_directory('.', path)


@app.route("/autenticar", methods=["POST",])
def autenticar():
	if request.form["username"] == "admin" and request.form["password"] == "admin":
		session["usuario_logado"] = request.form["username"]
		#flash(request.form["username"] + " logou com sucesso")
		return redirect("/dashboard.html")
	
	elif (request.form["username"] == "aurea" or request.form["username"] == "Aurea") and request.form["password"] == "071029":
		session["usuario_logado"] = request.form["username"]
		return redirect("/dashboard.html")
	
	elif (request.form["username"] == "marcio" or request.form["username"] == "Márcio" or request.form["username"] == "Marcio") and request.form["password"] == "071029":
		session["usuario_logado"] = request.form["username"]
		return redirect("/dashboard.html")
	
	else:
		flash("Usuário ou senha não existem")
		return redirect("/")
