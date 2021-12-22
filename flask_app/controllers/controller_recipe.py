from typing import ContextManager
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import model_user, model_recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/recipe/new')
def recipe_new():
    if 'uuid' not in session:
        return redirect('/')
    return render_template('recipe_new.html')

@app.route('/recipe/create', methods = ['POST'])
def recipe_create():
    is_valid = model_recipe.Recipe.validate_recipe(request.form);
    
    if not is_valid:
        return redirect ('/recipe/new')

    data = {

        **request.form,
        'user_id':session['uuid'], 
        'under_30_min':request.form['under_30_min']

    }

    model_recipe.Recipe.create(data)
    return redirect ('/dashboard')

@app.route('/recipe/<int:id>')
def recipe_show(id):
    context = {
        'user': model_user.User.get_one({'id':session['uuid']}),
        'recipe' : model_recipe.Recipe.get_user({"id":id}) 
    }
    return render_template('recipe_show.html', **context)

@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    if 'uuid' not in session:
        return redirect('/')
        
    context = {
        'user': model_user.User.get_one({'id':session['uuid']}),
        'recipe': model_recipe.Recipe.get_one({'id':id})
    }
    return render_template('recipe_edit.html', **context)

@app.route('/recipe/<int:id>/update', methods = ['POST'])
def recipe_update(id):
    is_valid = model_recipe.Recipe.validate_recipe(request.form)

    if not is_valid:
        return redirect(f'/recipe/{id}/edit')

    model_recipe.Recipe.update_one(request.form)
    return redirect('/')

@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    model_recipe.Recipe.delete_one({'id': id})
    return redirect('/')

#/recipe/new ->display
#/recipe/create ->action
#/recipe/<int:id> ->display
#/recipe/<int:id>/edit ->display
#/recipe/<int:id>/update ->action
#/recipe/<int:id>/delete ->action