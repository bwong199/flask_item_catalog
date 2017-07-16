from flask_catalog import app
from flask import render_template, redirect, flash, url_for, session, abort
from catalog.form import SetupForm
from flask_catalog import db
from author.models import Author
from catalog.models import Catalog
from author.decorators import login_required
import bcrypt

@app.route('/')
@app.route('/index')
def index():
	catalogs  = Catalog.query.count()
	if catalogs == 0:
		return redirect(url_for('setup'))
	return 'Hello World!'

@app.route('/admin')
@login_required
def admin():
	if session.get('is_author'):
		return render_template('catalog/admin.html')
	else:
		abort(403)

@app.route('/setup', methods=('GET', 'POST'))
def setup():
	form = SetupForm()
	error = ""
	if form.validate_on_submit():
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(form.password.data, salt)
		author = Author(
			form.fullname.data, 
			form.email.data, 
			form.username.data, 
			hashed_password,
			True
		)
		db.session.add(author)
		db.session.flush()
		if author.id:
			catalog = Catalog(
				form.title.data, 
				author.id
			)
			db.session.add(catalog)
			db.session.flush()
		else:
			db.session.rollback()
			error = "Error creating user"
		if author.id and catalog.id:
			db.session.commit()
			flash('Catalog created')
			return redirect(url_for('admin'))
		else:
			db.session.rollback()
			error = "Error creating catalog"
	return render_template('catalog/setup.html', form=form)

@app.route('/item')
@login_required
def post():
	return 'CATALOG POST'