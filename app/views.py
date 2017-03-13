"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from forms import CreateUser
from models import UserProfile
from werkzeug import secure_filename

import random
from datetime import date, datetime
from time import strftime 

UPLOAD_FOLDER = '.app/static/uploads'
app.config ['UPLOAD FOLDER']=UPLOAD_FOLDER


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/profile', methods=["GET", "POST"])
def profile():
    form = CreateUser()
    if request.method == "post" and form.validate_on_submit():
        
        userid  = random.randint(1, 1000)
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        age = form.age.data
        gender = form.gender.data
        bio = form.bio.data
        pwd = form.password.data
        file = request.files['image']
        img = secure_filename(file.filename)
        date_added = datetime.now().strftime("%a, %d, %b, %Y")  
        file.save(os.path.join("app/static/uploads", img))
        
        new_user= UserProfile(userid, firstname, lastname, username, age. gender, bio, pwd, img, date_added)
        db.session.add(new_user)
        db.session.commit()
        
        flash ("Sign up successful", "success")
        return redirect(url_for('profile'))
    flash_errors(form)
    return render_template('profile.html', form=form)

#handle form errors
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("There is an error in %field - %s" % (getattr(form, field).label.text,error), "danger") 


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        username = form.username.data
        password = form.username.data
        
        user = UserProfile.query.filter_by(username=username, password=password).first()
        
        if user is not None:
            login_user(user)
            return redirect(url_for('securepage'))
        else:
            return redirect(url_for('home'))
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
