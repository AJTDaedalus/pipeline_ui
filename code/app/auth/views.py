from flask import render_template, redirect, url_for, flash, request
from app.models import db
from app.auth.forms import RegistrationForm
from app.models import User
from app.auth import auth

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.lower()).first():
            flash('User already exists.', category='error')
            return redirect(url_for('home.index'))
        else:
            user = User(username=form.username.data.lower(),
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!',
                  category='success')
            return redirect(url_for('home.index'))
    return render_template('registration.html', title='Register', form=form)
