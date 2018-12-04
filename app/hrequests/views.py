#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, \
    flash, current_app, abort
from flask_login import login_required, current_user
from . import hrequests
from forms import FeatureForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User, Log

import app


@hrequests.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    """
    create a feature request
    """
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
        try:
            db.session.add(feature)
            db.session.commit()
            log = Log(
                    user_id=current_user._get_current_object().id,
                    feature_id=feature.id,
                    action="created",
                    timestamp=datetime.utcnow()
                )
            db.session.add(log)
            db.session.commit()
            flash('You have successfully created the Feature Request.')
        except:
            flash('Error: failed to create the Feature Request.')

        return redirect(url_for('.index'))

    return render_template('hrequests/create.html', form=form)


@hrequests.route('/index')
@login_required
def index():
    """
    list all feature requests
    """
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
    """
    edit a feature request
    """
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
        try:
            db.session.add(feature)
            db.session.commit()
            log = Log(
                    user_id=current_user._get_current_object().id,
                    feature_id=feature.id,
                    action="updated",
                    timestamp=datetime.utcnow()
            )

            db.session.add(log)
            flash('You have successfully updated the Feature Request.')
        except:
            flash('An error occured while trying to update the Feature Request.')

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
    """
    delete a feature request
    """
    id = request.form['request_id']
    feature = Feature.query.get_or_404(id)
    try:
        db.session.delete(feature)
        db.session.commit()

        log = Log(
                user_id=current_user._get_current_object().id,
                feature_id=feature.id,
                action="deleted",
                timestamp=datetime.utcnow()
            )

        db.session.add(log)
        db.session.commit()
        flash('You have successfully deleted the Feature Request.')
    except:
        flash('An error occured while deleting a Feature Request.')

    return redirect(url_for('.index'))

@hrequests.context_processor
def inject_logs():
    """
    inject logs into all templates in hrequests
    """
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)


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
