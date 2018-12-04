from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from . import productareas
from .forms import ProductAreaForm
from .. import db
from ..models import User, Client, ProductArea, Feature, User

@productareas.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductAreaForm()
    if form.validate_on_submit():
        product_area = ProductArea(product_area=form.product_area.data)
        try:
            db.session.add(product_area)
            db.session.commit()
            flash('You have successfully add the Product Area.')
        except:
            flash('An error occured while trying to add the Product Area.')
        return redirect(url_for('.index'))

    return render_template('productareas/create.html', form=form, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@productareas.route('/index')
@login_required
def index():
    product_areas = ProductArea.query.all()
    return render_template('productareas/index.html', product_areas=product_areas, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())


@productareas.route('/show/<id>')
@login_required
def show(id):
    product_area = ProductArea.query.get_or_404(id)
    if product_area is None:
        abort(404)
    return render_template('productareas/show.html', product_area=product_area, name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())


@productareas.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product_area = ProductArea.query.get_or_404(id)
    form = ProductAreaForm()
    if form.validate_on_submit():
        product_area.product_area=form.product_area.data
        try:
            db.session.add(product_area)
            db.session.commit()
            flash('You have successfully updated the Product Area.')
        except:
            flash('An error occured while trying to update the Product Area.')
        return redirect(url_for('.show', id=product_area.id))

    form.product_area.data = product_area.product_area
    return render_template('productareas/edit.html', form=form, product_area=product_area)


@productareas.route('/delete/', methods=['POST'])
@login_required
def delete():
    id = request.form['product_area_id']
    product_area = ProductArea.query.get_or_404(id)
    try:
        db.session.delete(product_area)
        db.session.commit()
        flash('You have successfully deleted the Product Area.')
    except:
        flash('An error occured while trying to delete the Product Area.')
    return redirect(url_for('.index'))

@productareas.context_processor
def inject_logs():
    """
    inject logs into all templates in product areas
    """
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)
