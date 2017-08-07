from flask_catalog import app
from flask import render_template, redirect, flash, url_for, session, abort, jsonify
from catalog.form import SetupForm, ItemForm
from flask_catalog import db
from author.models import Author
from catalog.models import Catalog, Item, Category
from author.decorators import login_required, author_required
import json
import bcrypt
from slugify import slugify

POSTS_PER_PAGE = 5

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
	catalog  = Catalog.query.first()
	if not catalog:
		return redirect(url_for('setup'))
	items = Item.query.filter_by(live=True).order_by(Item.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('catalog/index.html', catalog = catalog, items = items)

@app.route('/admin')
@app.route('/admin/<int:page>')
@author_required
def admin(page=1):
	if session.get('is_author'):
		items = Item.query.order_by(Item.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
		return render_template('catalog/admin.html', items = items)
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

# returns all the items in the first catalog in json
@app.route('/catalog.json', methods=['GET'])
def catalog():
	catalog  = Catalog.query.first()
	if not catalog:
		return redirect(url_for('setup'))
	items = Item.query.filter_by(live=True).order_by(Item.publish_date.desc())
	return json.dumps({'items': [i.title for i in items]})

@app.route('/items', methods=('GET', 'POST'))
@author_required
def items():
	form = ItemForm()
	if form.validate_on_submit():
		if form.new_category.data:
			new_category = Category(form.new_category.data)
			db.session.add(new_category)
			db.session.flush()
			category = new_category
		elif form.category.data:
			category_id = form.category.get_pk(form.category.data)
			category = Category.query.filter_by(id=category_id).first()
		else:
			category = None
		catalog = Catalog.query.first()
		author = Author.query.filter_by(username=session['username']).first()
		title = form.title.data
		description = form.description.data
		slug = slugify(title)
		item = Item(catalog, author, title, description, category, slug)
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('article', slug=slug))
	return render_template('catalog/items.html', form=form, action="new")

@app.route('/article/<slug>')
def article(slug):
	item = Item.query.filter_by(slug=slug).first_or_404()
	return render_template('catalog/article.html', item = item)

@app.route('/edit/<int:item_id>', methods=('GET', 'POST'))
@author_required
def edit(item_id):
	item = Item.query.filter_by(id=item_id).first_or_404()
	form = ItemForm(obj=item)
	print(form)
	if form.validate_on_submit():
		form.populate_obj(item)
		print(form.validate_on_submit())
		if form.new_category.data:
			new_category = Category(form.new_category.data)
			db.session.add(new_category)
			db.session.flush()
			post.category = new_category
		db.session.commit()
		return redirect(url_for('article', slug=item.slug))
	return render_template('catalog/items.html', form=form, item=item, action="edit")

@app.route('/delete/<int:item_id>')
@author_required
def delete(item_id):
	item = Item.query.filter_by(id=item_id).first_or_404()
	item.live = False
	db.session.commit()
	flash('Item deleted')
	return redirect('/admin')



