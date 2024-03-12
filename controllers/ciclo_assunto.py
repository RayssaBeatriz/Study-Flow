from flask import render_template, request, flash, redirect
from models import CicloAssunto, CicloEstudo, Assunto
from database import db, lm
from flask import Blueprint, url_for
from flask_login import current_user
from sqlalchemy.sql import func
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select
import json

bp_c_assunto = Blueprint("c_assunto", __name__, template_folder='templates')


@bp_c_assunto.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        assunto = Assunto.query.filter_by(id_usuario=current_user.id).all()
        return render_template('c_assunto_create.html', assunto=assunto)
    if request.method == 'POST':
        id_ciclo = CicloEstudo.query.filter_by().order_by(
            CicloEstudo.id.desc()).first().id
        ids_assuntos = request.form.getlist('checkbox')
        for id_assunto in ids_assuntos:
            ciclo_assunto = CicloAssunto(id_ciclo, id_assunto)
            db.session.add(ciclo_assunto)
            db.session.commit()

        return redirect('/c_assunto/calculo')


@bp_c_assunto.route('/calculo', methods=['GET', 'POST'])
def calculo():
    last_ciclo = CicloEstudo.query.filter_by().order_by(
    CicloEstudo.id.desc()).first().id
    q_tempo = CicloEstudo.query.filter_by(id=last_ciclo).first().duracao_ciclo
    q_min = int(datetime.datetime.strftime(q_tempo, '%H')) * 60 + int(
      datetime.datetime.strftime(q_tempo, '%M'))
    dados = db.session.query(CicloAssunto, Assunto).join(CicloAssunto).filter_by(id_ciclo=last_ciclo).all()

    soma = 0
    lista_a = []
    lista_d = []
    lista_h = []
    for cicloassunto, assunto in dados:
      soma = int(assunto.nf) + soma

    for cicloassunto, assunto in dados:
        calculo = q_min*float(assunto.nf)/soma
        calculo_d = float(calculo/60)
        if calculo_d == calculo_d:
          quebrado = str(calculo_d)[0]
          horas_r = float(calculo_d) - float(quebrado)
          horas_g = int(calculo_d)
          horas_h = (horas_r)*60
          horas_c = float(horas_h/100)
          horas_int = "{}h e {}m".format(horas_g, horas_c)
          horas_float = float(horas_g + horas_c)
          print('Tempo de estudo para {} é {}'.format(assunto.nome, horas_int))
          lista_a.append(assunto.nome)
          lista_d.append(calculo)
          lista_h.append(horas_float)
          print ('Lista: {}'.format(lista_d))
          print ('Lista: {}'.format(lista_h))
    return render_template("grafico.html",
                           ctx = json.dumps(lista_d),
                           ctxv = json.dumps(lista_a),
                           ctxh = json.dumps(lista_h))
