from database import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
  __tablename__ = "usuario"
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(100))
  email =  db.Column(db.String(100))
  senha = db.Column(db.String(100))
  admin = db.Column(db.Boolean)

  def __init__(self, nome, email, senha, admin):
    self.nome= nome
    self.email= email
    self.senha= senha
    self.admin = admin

  def __repr__(self):
    return '<Usuário{}>'.format(self.nome, self.id)

class Assunto(db.Model):
  __tablename__ = "assunto"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  nome = db.Column(db.String(100))
  descricao = db.Column(db.String(100))
  nf = db.Column(db.String(100))
  usuario = db.relationship('Usuario', foreign_keys=id_usuario)
  
  def __init__(self, id_usuario, nome, descricao, nf):
    self.id_usuario = id_usuario
    self.nome = nome
    self.descricao = descricao
    self.nf = nf

  def __repr__(self):
    return '<Assunto: {} - {} - {} >'.format(self.id, self.usuario.nome, self.usuario.email)

class CicloAssunto(db.Model):
  __tablename__ = "cicloassunto"
  id = db.Column(db.Integer, primary_key = True)
  id_ciclo = db.Column(db.Integer, db.ForeignKey('cicloestudo.id'))
  id_assunto  = db.Column(db.Integer, db.ForeignKey('assunto.id'))
  assunto = db.relationship('Assunto', foreign_keys=id_assunto)

  def __init__(self, id_ciclo, id_assunto):
    self.id_ciclo = id_ciclo
    self.id_assunto = id_assunto

class CicloEstudo(db.Model):
  __tablename__ = "cicloestudo"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  nome_ciclo = db.Column(db.String(100))
  duracao_ciclo = db.Column(db.DateTime)

  def __init__(self, id_usuario, nome_ciclo, duracao_ciclo):
    self.id_usuario = id_usuario
    self.nome_ciclo = nome_ciclo
    self.duracao_ciclo = duracao_ciclo

  def __repr__(self):
    return '<Ciclo Estudo{}>'.format(self.nome_ciclo, self.id)

class HorasEstudadas (db.Model):
  __tablename__ = "horasestudadas"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  id_assunto = db.Column(db.Integer, db.ForeignKey('assunto.id'))
  inicio_estudo = db.Column(db.DateTime)
  fim_estudo = db.Column(db.DateTime)

  def __init__(self, id_usuario, id_assunto, inicio_estudo, fim_estudo):
    self.id_usuario = id_usuario
    self.id_assunto = id_assunto
    self.inicio_estudo = inicio_estudo
    self.fim_estudo = fim_estudo

  def __repr__(self):
    return '<Perfil do horas estudadas{}>'.format(self.id_usuario, self.id)
''''
class CicloAssunto(db.Model):
  __tablename__ = "cicloassunto"
  id = db.Column(db.Integer, primary_key = True)
  id_assunto= db.Column(db.Integer, db.ForeignKey('assunto.id'))
  id_estudo= db.Column(db.Integer, db.ForeignKey('cicloestudo.id'))
  id_horasestudo = db.Column(db.Integer, db.ForeignKey('horasestudadas.id'))

  def __init__(self, id_assunto, id_estudo):
    self.id_assunto = id_assunto
    self.id_ciclo = id_estudo

  def __repr__(self):
    return '<Perfil do ciclo de assuntos{}>'.format(self.id_usuario, self.id_horasestudo, self.estudo)
  '''