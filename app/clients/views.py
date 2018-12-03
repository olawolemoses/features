#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, \
    flash
from flask_login import login_required, current_user
from . import clients
from forms import ClientForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User

@clients.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(client_name=form.client_name.data)
        db.session.add(client)
        return redirect(url_for('.index'))
    return render_template('clients/create.html', form=form)

@clients.route('/index')
@login_required
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)


@clients.route('/show/<id>')
@login_required
def show(id):
    client = Client.query.get_or_404(id)
    if client is None:
        abort(404)
    return render_template('clients/show.html', client=client)


@clients.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    form = ClientForm()
    if form.validate_on_submit():
        client.client_name = form.client_name.data
        return redirect(url_for('.show', id=client.id))

    form.client_name.data = client.client_name
    return render_template('clients/edit.html', form=form,
                           client=client)


@clients.route('/delete/', methods=['POST'])
@login_required
def delete():
    id = request.form['client_id']
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('You have successfully deleted the Client.')
    return redirect(url_for('.index'))


@clients.context_processor
def inject_logs():
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)
