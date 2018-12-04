#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm

from app import db

# login user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticate a User
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None \
            and user.verify_password(form.password.data):
            try:
                login_user(user, form.remember_me.data)
            except:
                flash('Something wrong happened while trying to log you in')
            return redirect(request.args.get('next')
                            or url_for('hrequests.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

# logout user

from flask_login import logout_user, login_required
@auth.route('/logout')
@login_required
def logout():
    """
    Logout a User
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a User
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            flash('You can now login.')
        except:
            flash('An error occured while trying to register')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
