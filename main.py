from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from data import db_session, jobs, users
from werkzeug.security import *

app = Flask(__name__, template_folder='./template')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run(host='127.0.0.1', port=5000)


@app.route('/')
def work_log():
    db_session.global_init('db/blogs.sqlite')
    session = db_session.create_session()
    peoples = session.query(users.User)
    return render_template('prof.html', peoples=session.query(users.User), jobs=session.query(jobs.Jobs))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
# http://127.0.0.1:5000/register
