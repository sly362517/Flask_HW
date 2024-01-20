from flask import Flask, render_template, request, flash, redirect, url_for
import os
from config import Config
from models import db, User
from random import choice
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)

@app.route('/registration/', methods=['GET', 'POST'])
def registration3():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        name = form.name.data.lower()
        surname = form.surname.data.lower()
        email = form.email.data
        user = User(name=name, surname=surname, email=email)
        if User.query.filter(User.email == email).first():
            flash(f'Пользователь с e-mail {email} уже существует')
            return redirect(url_for('registration'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('registration3'))
    return render_template('registration3.html', form=form)


if __name__ == '__main__':
    app.run()
