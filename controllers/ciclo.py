from flask import render_template, request, flash, redirect
from models import CicloEstudo
from database import db, lm
from flask import Blueprint, url_for
from flask_login import current_user
import datetime

bp_ciclo = Blueprint("ciclo", __name__, template_folder='templates')

@bp_ciclo.route('/create', methods= ['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('ciclo_create.html')
  if request.method == 'POST':
    id_usuario = current_user.id
    nome_ciclo = request.form.get('nome')
    duracao_cicl = request.form.get('duracao')
    duracao_ciclo = datetime.datetime.strptime(duracao_cicl, '%H:%M')
    cicloestudo = CicloEstudo(id_usuario, nome_ciclo, duracao_ciclo)
    db.session.add(cicloestudo)
    ciclo = db.session.flush()
    db.session.commit()
    #usar url_for
    return redirect('/c_assunto/create')

@bp_ciclo.route('/recovery' )
def recovery():
    ciclo = CicloEstudo.query.filter_by(id_usuario=current_user.id).all()
    return render_template('ciclo_recovery.html', ciclo=ciclo)

@bp_ciclo.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cicloEstudo = CicloEstudo.query.get(id)
    
    if request.method== 'GET':
      return render_template('ciclo_update',  cicloEstudo = cicloEstudo)
    if request.method=='POST':
      CicloEstudo.nome = request.form.get('nome')
      CicloEstudo.duracao_ciclo = request.form.get('duracao')
  
      db.session.add(cicloEstudo) 
      db.session.commit()
      flash('Ciclo atualizado com sucesso!')
      return redirect('/recovery')

@bp_ciclo.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
  if request.method == 'GET':
    ciclo = CicloEstudo.query.get(id)
    return render_template('ciclo_delete.html', ciclo = ciclo)

  if request.method == 'POST':
    ciclo = CicloEstudo.query.get(id)
    db.session.delete(ciclo)
    db.session.commit()
    flash('Ciclo excluído com sucesso')
    return redirect('/recovery')
