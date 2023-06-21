from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipes_model import Recipe
from flask_app.models.users_model import User


@app.route('/recipes/new')
def show_form():
    return render_template('new_recipe.html')


@app.route('/recipes/create', methods=['POST'])
def submit_new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    recipe_data = {
        ** request.form,
        'user_id' : session['user_id']
    }

    Recipe.create_recipe(recipe_data)

    return redirect('/dashboard')

# Show one Recipe

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):

    one_recipe = Recipe.get_one_recipe({'recipe_id' : recipe_id})
    one_user = User.getUserById({'user_id' : session['user_id']})

    return render_template('single_recipe.html', one_recipe=one_recipe, one_user=one_user)


#show edit form
@app.route('/recipes/edit/<int:recipe_id>')
def show_edit_form(recipe_id):

    one_recipe = Recipe.get_one_recipe({'recipe_id' : recipe_id})

    return render_template('edit_recipe.html', one_recipe=one_recipe)

# submission route
@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def submit_edit_form(recipe_id):

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')

    Recipe.update_recipe({
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'minutes' : int(request.form['minutes']),
        'date' : request.form['date'],
        'recipe_id' : recipe_id
    })

    return redirect('/dashboard')

# delete route

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):

    Recipe.delete_recipe({'recipe_id' : recipe_id})
    return redirect('/dashboard')
