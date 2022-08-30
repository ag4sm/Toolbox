from . import bp as auth
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, request, flash, redirect, url_for, session
from .forms import LoginForm, SignupForm, EditProfileForm
from ...models import User

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        # check if user exists and if entered password matches hashed password
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash("You have now successfully logged in.", 'success')
            return redirect(url_for('main.user'))
        flash("Incorrect Email/Password Combo!", 'danger')
        return render_template('login.html.j2', form=form)
    # Below render handles the GET (or the "else" part of the if statement)
    return render_template('login.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out.', 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name" : form.first_name.data.title(),
                "last_name" : form.last_name.data.title(),
                "email" : form.email.data.lower(),
                "password" : form.password.data
            }
            # create new empty user
            new_user_object = User()
            # build user with form data
            new_user_object.user_from_dict(new_user_data)
            # save to database
            new_user_object.save()
        except:
            flash("There was an unexpected error.", 'warning')
            return render_template('signup.html.j2', form=form)

        flash("You have registered successfully", 'success')
        return redirect(url_for('auth.login'))
    
    # This statement handles the GET method (what happens when someone just comes to the site)
    return render_template('signup.html.j2', form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
                "first_name" : form.first_name.data.title(),
                "last_name" : form.last_name.data.title(),
                "email" : form.email.data.lower(),
                "password" : form.password.data
        }
        user = User.query.filter_by(email=new_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash('Email is already in use.', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.user_from_dict(new_user_data)
            current_user.save()
            flash('Profile successfully updated.', 'success')
        except:
            flash('There was an unexpected error trying to update your profile. Please try again.', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.user'))
    return render_template('signup.html.j2', form=form)
