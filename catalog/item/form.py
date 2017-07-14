from flask_wtf import Form
from wtforms import validators,StringField
from author.form import RegisterForm

class SetupForm(RegisterForm):
	title = StringField('Item name', [
		validators.Required(),
		validators.Length(max=80)
	])
