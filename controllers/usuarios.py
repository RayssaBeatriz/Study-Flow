from flask import render_template, request, redirect, flash
from models import Usuario
from database import db, lm
from flask import Blueprint, url_for
from flask_login import login_user, logout_user, login_required, current_user

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

@bp_usuarios.route('/recovery')
@login_required
def recovery():
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
  if request.method=='GET':
    usuarios = Usuario.query.all()
    return render_template('usuarios_recovery.html', usuarios=usuarios)

@bp_usuarios.route('/create', methods= ['GET', 'POST'])
def create():
  if request.method== 'GET':
    return render_template('cadastro.html')
  else:
    nome = request.form.get('nome')
    email= request.form.get('email')
    senha= request.form.get('senha')
    csenha= request.form.get('senha2')
    admin= 0
    usuario= Usuario(nome, email, senha, admin)
    db.session.add(usuario)
    db.session.commit()

    if senha==csenha:
      flash('Dados registrados com sucesso')
      usuario = Usuario.query.filter_by(email = email).first()
      login_user(usuario)
      return redirect('/')
    elif senha != csenha:
      flash('Senhas não conferem')
      return redirect(url_for('.create'))

@bp_usuarios.route('/update', defaults={'id':0}, methods= ['GET', 'POST'])
@bp_usuarios.route('/update/<int:id>', methods= ['GET', 'POST'])
@login_required
def update(id):
  if id==0 or not current_user.admin:
    id = current_user.id
    if request.method== 'GET':
      usuario= Usuario.query.get(id)
      return render_template('usuario_update.html', usuario = usuario)
    if request.method=='POST':
      usuario = Usuario.query.get(id)
      usuario.nome = request.form.get('nome')
      usuario.email = request.form.get('email')
  
    if (request.form.get('senha') and request.form.get('senha2') == request.form.get('senha')):
        usuario.senha = request.form.get('senha')
      
    else:
        flash('Senhas não conferem')
        return redirect(url_for('.update', id=id))
  else:
    if request.method== 'GET':
      usuario= Usuario.query.get(id)
      return render_template('admin_update.html', usuario=usuario)
    if request.method=='POST':
      usuario = Usuario.query.get(id)
      usuario.nome = request.form.get('nome')
      usuario.email = request.form.get('email')
      usuario.admin = bool(request.form.get('admin'))

  db.session.add(usuario) 
  db.session.commit()
  flash('Dados atualizados com sucesso!')
  return redirect(url_for('.recovery'))

@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
    
  if request.method == 'GET':
    usuario = Usuario.query.get(id)
    return render_template('usuarios_delete.html', usuario = usuario)

  if request.method == 'POST':
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso')
    return redirect(url_for('.recovery'))

@lm.user_loader
def load_user(id):
  usuario = Usuario.query.filter_by(id=id).first()
  return usuario

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
  email = request.form.get('email')
  senha = request.form.get('senha')
  usuario = Usuario.query.filter_by(email = email).first()
  if usuario and senha == usuario.senha:
    login_user(usuario)
    return redirect('/')
  else:
    flash('Dados incorretos', 'danger')
    return redirect('/login')

@bp_usuarios.route('/logoff')
def logoff():
  logout_user()
  return redirect('/')