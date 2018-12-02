#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, \
    flash, current_app
from flask_login import login_required, current_user
from . import hrequests
from forms import FeatureForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User

import app


@hrequests.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = FeatureForm()
    if form.validate_on_submit():

        feature = Feature(
            title=form.title.data,
            description=form.description.data,
            client_priority=form.client_priority.data,
            target_date=form.target_date.data,
            product_area_id=form.product_area.data,
            client_id=form.client.data,
            project_id=form.project.data,
            user_id=current_user._get_current_object().id,
            )

        # reorder

        arr = \
            Feature.query.filter_by(client_id=form.client.data).order_by(Feature.client_priority).all()
        reorder(arr, form.client_priority.data)
        db.session.add(feature)
        flash('You have successfully created the Feature Request.')
        return redirect(url_for('.index'))

    return render_template('hrequests/create.html', form=form)


@hrequests.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)

    pagination = \
        Feature.query.order_by(Feature.timestamp.desc()).paginate(page,
            current_app.config['POSTS_PER_PAGE'], False)

    features = pagination.items

    return render_template('hrequests/index.html', features=features,
                           pagination=pagination)


@hrequests.route('/show/<id>')
@login_required
def show(id):

    feature = Feature.query.get_or_404(id)
    if feature is None:
        abort(404)
    return render_template('hrequests/show.html', feature=feature,
                           name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())


@hrequests.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    feature = Feature.query.get_or_404(id)

    form = FeatureForm()

    if form.validate_on_submit():

        feature.title = form.title.data
        feature.description = form.description.data
        feature.client_priority = form.client_priority.data
        feature.target_date = datetime.utcnow()
        feature.product_area_id = form.product_area.data
        feature.client_id = form.client.data
        feature.project_id = form.project.data
        feature.user_id = current_user._get_current_object().id
        arr = Feature.query.filter(Feature.client_id
                                   == form.client.data).filter(Feature.id
                != feature.id).order_by(Feature.client_priority).all()
        reorder(arr, form.client_priority.data)
        db.session.add(feature)
        flash('You have successfully updated the Feature Request.')
        return redirect(url_for('.show', id=feature.id))

    form.title.data = feature.title
    form.description.data = feature.description
    form.client_priority.data = feature.client_priority
    form.target_date.data = feature.target_date
    form.product_area.data = feature.product_area_id
    form.client.data = feature.client_id
    form.project.data = feature.project_id
    form.user.data = current_user._get_current_object().id

    return render_template('hrequests/edit.html', form=form,
                           feature=feature)


@hrequests.route('/delete/', methods=['POST'])
@login_required
def delete():
    id = request.form['request_id']
    feature = Feature.query.get_or_404(id)
    print feature
    db.session.delete(feature)
    db.session.commit()
    flash('You have successfully deleted the Feature Request.')
    return redirect(url_for('.index'))


def reorder(arr, index):

    i = len(arr)

    while i >= index:
        arr[i - 1].client_priority = i + 1
        db.session.add(arr[i - 1])
        i = i - 1

    while i > 0:
        arr[i - 1].client_priority = i
        db.session.add(arr[i - 1])
        i = i - 1
    db.session.commit()
