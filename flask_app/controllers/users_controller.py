from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipes_model import Recipe


# this is a show page of the home page
@app.route('/')
def home():
    return render_template('register.html')


@app.route('/loginuser', methods=['POST'])
def loginuser():

    login_data = {'email' : request.form['email']}
    user_in_db = User.getUserByEmail(login_data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect(f'/dashboard')


@app.route('/register_user', methods=['POST'])
def successful_register():

    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    newUser_data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password': pw_hash
    }
    user_id = User.createUser(newUser_data)

    session['user_id'] = user_id

    return redirect(f'/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/')

    one_user = User.getUserById({'user_id' : session['user_id']})

    all_recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', one_user=one_user, all_recipes=all_recipes)
