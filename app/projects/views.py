from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import projects
from .forms import ProjectForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User, Project

@projects.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(project_name=form.project_name.data)
        db.session.add(project)
        return redirect(url_for('.index'))
    return render_template('projects/create.html', form=form, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@projects.route('/index')
@login_required
def index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())


@projects.route('/show/<id>')
@login_required
def show(id):
    project = Project.query.get_or_404(id)
    if project is None:
        abort(404)
    return render_template('projects/show.html', project=project, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())


@projects.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.project_name=form.project_name.data
        return redirect(url_for('.show', id=project.id))

    form.project_name.data = project.project_name
    return render_template('projects/edit.html', form=form, project=project)


@projects.route('/delete/', methods=['POST'])
@login_required
def delete():
    id = request.form['project_id']
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')
    return redirect(url_for('.index'))

@projects.context_processor
def inject_logs():
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)
