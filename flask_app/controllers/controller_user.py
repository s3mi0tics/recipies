from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import model_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/user/process_login', methods = ["POST"])
def process_login():
    is_valid = model_user.User.validate_login(request.form)
    if not is_valid:
        return redirect('/')
    
    potential_user= model_user.User.get_one_by_email({"email" : request.form['email']})

    if not potential_user:
        flash('Invalid credentials', "err_user_password1")
        return redirect('/')
    
    password_match = bcrypt.check_password_hash(potential_user.password, request.form['password'])
    
    if not password_match:
        flash('Invalid credentials', "err_user_password1")
        return redirect('/')


    session ['uuid'] = potential_user.id

    return redirect('/dashboard')

@app.route('/user/create', methods = ['POST'])
def user_create():
    is_valid = model_user.User.validate_registration(request.form)
    if not is_valid:
        return redirect ('/')
    
    hash_password = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': hash_password
    }
    
    id = model_user.User.create(data)
    session ['uuid'] = id
    return redirect ('/')

@app.route('/user/<int:id>')
def user_show(id):
    return render_template('user_show.html')

@app.route('/user/<int:id>/edit')
def user_edit(id):
    return render_template('user_edit.html')

@app.route('/user/<int:id>/update', methods = ['POST'])
def user_update(id):
    return redirect('/')

@app.route('/user/<int:id>/delete')
def user_delete(id):
    return redirect('/')

#/user/new ->display
#/user/create ->action
#/user/<int:id> ->display
#/user/<int:id>/edit ->display
#/user/<int:id>/update ->action
#/user/<int:id>/delete ->action