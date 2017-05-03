from flask import Blueprint, render_template, flash, redirect, url_for
from models import db, User
from forms import LoginForm, RegisterForm

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logged in', category='success')
        return redirect(url_for('blog.index'))
    return render_template('main/login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    flash('Logged out', category='success')
    return redirect(url_for('blog.index'))


@main_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Please log in')
        return redirect(url_for('main.login'))
    return render_template('main/register.html',form=form)


