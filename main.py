from flask import Flask, render_template
from data import db_session, jobs, users

app = Flask(__name__, template_folder='./template')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(host='127.0.0.1', port=5000)


@app.route('/')
def work_log():
    db_session.global_init('db/blogs.sqlite')
    session = db_session.create_session()
    peoples = session.query(users.User)
    return render_template('prof.html', peoples=session.query(users.User), jobs=session.query(jobs.Jobs))


if __name__ == '__main__':
    main()
