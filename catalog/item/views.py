from catalog import app
from flask import render_template, redirect, flash, url_for
from item.form import SetupForm
from catalog import db
from author.models import Author
from item.models import Item

@app.route('/')
@app.route('/index')
def index():
	return "Hello dfdfWordfdfld!"

@app.route('/admin')
def admin():
	items = Item.query.count()
	if items == 0:
		return redirect(url_for('setup'))
	return render_template('item/admin.html')

@app.route('/setup', methods=('GET', 'POST'))
def setup():
	form = SetupForm()
	error = ""
	if form.validate_on_submit():
		author = Author(
			form.fullname.data, 
			form.email.data, 
			form.username.data, 
			form.password.data, 
			True
		)
		db.session.add(author)
		db.session.flush()
		if author.id:
			item = Item(
				form.title.data, 
				author.id
			)
			db.session.add(item)
			db.session.flush()
		else:
			db.session.rollback()
			error = "Error creating user"
		if author.id and item.id:
			db.session.commit()
			flash('Item created')
			return redirect(url_for('admin'))
		else:
			db.session.rollback()
			error = "Error creating item"
	return render_template('item/setup.html', form=form)