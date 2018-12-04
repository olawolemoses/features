from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from . import admin
from ..auth.forms import RegistrationForm
from .forms import RoleForm, UserAssignForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User, Role

@admin.route('/users/index')
@login_required
def users_index():
    """
    List all users
    """
    check_admin()
    users = User.query.all()
    roles = Role.query.all()

    return render_template('admin/users/index.html', users=users, roles=roles,
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@admin.route('/users/assign/', methods=['GET', 'POST'])
@login_required
def users_assign():
    """
    Assign a role to a user
    """
    check_admin()

    id = request.form['user_id']

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role

    form = UserAssignForm(obj=user)

    if form.validate_on_submit():
        user.role = form.role.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have successfully assigned a role.')
        except:
            flash('Error: failed to assign a role.')
        # redirect to the roles page
        return redirect(url_for('admin.users_index'))

    return render_template('admin/users/assign.html',
                           user=user, form=form,
                           title='Assign User')


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/index.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/create.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully edited the role.')
        except:
            flash('Error: there is a problem assigning this role')
        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/create.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    try:
        db.session.delete(role)
        db.session.commit()
        flash('You have successfully deleted the role.')
    except:
        flash('An error occured while trying to delete the role.')
    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.context_processor
def inject_logs():
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)
