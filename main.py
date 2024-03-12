from flask import Flask, render_template, request, redirect
from flask import Blueprint
from database import db, lm
from flask_migrate import Migrate
from controllers.usuarios import bp_usuarios
from controllers.assunto import bp_assunto
from controllers.ciclo import bp_ciclo
from controllers.ciclo_assunto import bp_c_assunto
from flask_login import current_user
from models import Usuario, Assunto, CicloAssunto, CicloEstudo
from sqlalchemy import select


app = Flask(__name__)
app.config['SECRET_KEY'] = 'palavra-secreta'
conexao = "sqlite:///meubanco.db"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
app.register_blueprint(bp_assunto, url_prefix='/assunto')
app.register_blueprint(bp_ciclo, url_prefix='/ciclo')
app.register_blueprint(bp_c_assunto, url_prefix='/c_assunto')
db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect('/c_assunto/calculo')
  else:
    return render_template('landingpage.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/cadastro')
def cadastro():
  return render_template('cadastro.html')

@app.route('/assunto')
def assunto():
  assunto = Assunto.query.filter_by(id_usuario=current_user.id).all()
  return render_template('materia2.html', assunto=assunto)

  
@app.route('/sugestoes')
def sugestoes():
  return render_template('sugestões.html')

@app.route('/sugestoes2')
def sugestoes2():
  return render_template('sugestoes2.html')
  
@app.route('/recebe_sugestoes', methods=['GET'])
def dados():
  nome = request.args.get("nome")
  email = request.args.get("email")
  sugestao = request.args.get("sugestao")
  enviar = request.args.get("enviar")
  return render_template('recebe_sugestao.html', nome=nome, email=email, sugestao=sugestao, enviar=enviar)

@app.route('/sobre_nos')
def sobre():
  return render_template('sobre.html')
  
app.run(host='0.0.0.0', port=81)