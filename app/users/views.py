from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import users
from ..auth.forms import RegistrationForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User

@users.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        #flash('You can now login.')
        return redirect(url_for('.index'))
    return render_template('users/create.html', form=form, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@users.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@users.route('/show/<id>')
@login_required
def show(id):
    user = User.query.get_or_404(id)
    if user is None:
        abort(404)
    return render_template('users/show.html', user=user, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())


@users.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = RegistrationForm()
    if form.validate_on_submit():
        user.username=form.username.data
        return redirect(url_for('.show', id=user.id))

    form.username.data = user.username
    form.email.data = user.email
    return render_template('users/edit.html', form=form, user=user)


@users.route('/delete/', methods=['POST'])
@login_required
def delete():
    id = request.form['user_id']
    user = User.query.get_or_404(id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')
    return redirect(url_for('.index'))
