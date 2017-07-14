from catalog import db

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	admin = db.Column(db.Integer, db.ForeignKey('author.id'))

	def __init__(self, title, admin):
		self.title = title
		self.admin = admin

	def __repr__(self):
		return '<Blog %r>' % self.name