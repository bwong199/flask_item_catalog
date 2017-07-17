from flask_catalog import db
from datetime import datetime

class Catalog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	admin = db.Column(db.Integer, db.ForeignKey('author.id'))
	items = db.relationship('Item', backref='catalog', lazy='dynamic')

	def __init__(self, title, admin):
		self.title = title
		self.admin = admin

	def __repr__(self):
		return '<Catalog %r>' % self.title

class Item(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
	title = db.Column(db.String(80))
	description = db.Column(db.String(80))
	slug = db.Column(db.String(256), unique=True)
	publish_date = db.Column(db.DateTime)
	live = db.Column(db.Boolean)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category= db.relationship('Category', backref=db.backref('items', lazy='dynamic'))

	def __init__(self, catalog, author, title, description, category, slug=None, publish_date=None, live=True):
		self.catalog_id = catalog.id
		self.author_id = author.id
		self.title = title
		self.description = description
		self.category_id = category.id
		self.slug = slug
		if publish_date is None:
			self.publish_date = datetime.utcnow()
		else:
			self.publish_date = publish_date
		self.live = live

	def __repr__(self):
		return '<Item %r>' % self.title

class Category(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))

	def __init__(self, title):
		self.title = title

	def __repr__(self):
		return self.title
