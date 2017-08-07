from flask_catalog import app
from flask import render_template, redirect, url_for, session, request
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
from flask_catalog import db
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
import bcrypt

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for("index"))
    request_token = get_request_token()
    session['request_token'] = request_token
    return redirect(get_oauth_verifier_url(request_token))

@app.route('/auth/twitter') 
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)
    print(access_token['screen_name'])
    user = Author.query.filter_by(username = access_token['screen_name'],).first() 
    if user:
    	session['username'] = user.username
    	session['is_author'] = user.is_author
    	session['user_id'] = user.id
    	if 'next' in session:
    		next = session.get('next')
    		session.pop('next')
    		return redirect(next)
    	else:			
    		return redirect(url_for('index'))

    if not user:
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw("password", salt)
		author = Author(
			access_token['screen_name'], 
			access_token['screen_name'] + "@defaultemail.com", 
			access_token['screen_name'], 
			hashed_password,
			True
		)
		db.session.add(author)
		db.session.flush()
		db.session.commit()
		return redirect(url_for('success'))
    abort(403)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	error = None

	if request.method == 'GET' and request.args.get('next'):
		session['next'] = request.args.get('next', None)
	if form.validate_on_submit():
		author = Author.query.filter_by(
			username = form.username.data,
		).first() 
		if author:
			if bcrypt.hashpw(form.password.data, author.password) == author.password:
				session['username'] = form.username.data
				session['is_author'] = author.is_author
				session['user_id'] = author.id

				if 'next' in session:
					next = session.get('next')
					session.pop('next')
					return redirect(next)
				else:			
					return redirect(url_for('index'))
			else:
				error = "Incorrect username and password"
		else:
			error = "Incorrect username and password"
	return render_template('author/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
	form = RegisterForm()
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
		db.session.commit()
		return redirect(url_for('success'))
	return render_template('author/register.html', form=form)

@app.route('/success')
def success():
	return "User created"

@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('is_author')
	return redirect(url_for('index'))