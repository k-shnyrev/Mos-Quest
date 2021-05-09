import os.path

from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user

from data import db_session
from forms.answer_form import AnswerForm
from data.answers import Answer
from data.questions import Question
from data.users import User
from forms.login_form import LoginForm
from forms.user import RegisterForm
from maps import save_toponym_map

QUESTIONS = [
    ('Кинология', 'По легенде, волшебный друг человека, который исполнит ваше '
                  'желание, находится где-то здесь.\n'
                  'Сколько кандидатов вы сможете найти?\n'
                  'В ответ запишите число.', '4', 'Площадь Революции'),
    ('Тюлени', 'На месте этого здания какое-то время находился другой объект -'
               ' тоже очень крупный, самый большой такой объект в стране.\n'
               'Запишите в ответ число - диаметр этого объекта в метрах.',
     '130', 'ул. Волхонка, 15'),
    ('Символизм', 'Где-то вблизи этой отметки расположена достаточно '
                  'необычная композиция.\n'
                  'Традиционные религии часто выделяют семь подобных явлений, '
                  'в композиции же их ощутимо больше.\n'
                  'Сколько?', '13', 'Болотная площадь'),
    ('Остров, над которым никогда не заходит солнце',
     'Это единственное в своём роде здание в Москве построено достаточно '
     'давно.\nНазовите год окончания стройки?', '1884',
     'Вознесенский пер., 8/5с3'),
    ('Он жив!', 'Эта известная улица стала такой не сразу.\n'
                'Рядом с ней расположено множество интересных объектов.\n'
                'В каком году возник мемориал, на который намекает название '
                'вопроса?',
     '1990', 'ул. Арбат, 37/2с6')
]

db_session.global_init('db/quest.sqlite')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def get_images():
    db_sess = db_session.create_session()
    db_questions = db_sess.query(Question)
    for question in db_questions:
        file_name = os.path.join('static', 'img', 'questions')
        file_name += '/' + str(question.id) + '.png'
        save_toponym_map(question.map_request, file_name)


def upload_questions():
    db_sess = db_session.create_session()
    db_questions = db_sess.query(Question)
    if not db_questions.first():
        for title, content, answer, map_request in QUESTIONS:
            question = Question(title=title, content=content,
                                true_answer=answer, map_request=map_request)
            db_sess.add(question)
            db_sess.commit()


@app.route('/')
@app.route('/index')
def index():
    upload_questions()
    db_sess = db_session.create_session()
    questions = db_sess.query(Question)
    points = {}
    answers = {}
    tryings = {}
    username = 'Гость'
    db_answers = db_sess.query(Answer)
    if current_user.is_authenticated:
        get_images()
        username = current_user.name
        for answer in db_answers.filter(Answer.user == current_user):
            answers[answer.question_id] = answer.answer
            points[answer.question_id] = answer.score
            tryings[answer.question_id] = answer.trying
    users = []
    rating = []
    db_users = db_sess.query(User)
    for user in db_users:
        score = 0
        for answer in db_answers.filter(Answer.user_id == user.id):
            score += answer.score
        users.append((user.name, score))
    users.sort(key=lambda x: x[1], reverse=True)
    for pos, user in enumerate(users):
        rating.append((pos + 1,) + user)
    param = {
        'username': username,
        'title': 'Домашняя страница',
        'questions': questions,
        'points': points,
        'answers': answers,
        'tryings': tryings,
        'rating': rating
    }
    return render_template('index.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/answer/<int:question_id>',  methods=['GET', 'POST'])
@login_required
def give_answer(question_id):
    form = AnswerForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == question_id).first()
        if not question:
            abort(404)
        answer = db_sess.query(Answer).filter(Answer.user == current_user,
                                              Answer.question_id == question_id).first()
        if answer:
            form.answer.data = answer.answer
        return render_template('answer.html', title='Ответ',
                               form=form, question=question)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        answer = db_sess.query(Answer).filter(Answer.user_id == current_user.id,
                                              Answer.question_id == question_id).first()
        if not answer:
            answer = Answer()
            db_sess.add(answer)
            answer.user_id = current_user.id
            answer.question_id = question_id
            answer.answer = form.answer.data
        elif not answer.score:
            answer.answer = form.answer.data
        question = db_sess.query(Question).filter(Question.id == question_id).first()
        if answer.answer.lower() == question.true_answer.lower():
            answer.score = 10 - answer.trying if answer.trying < 10 else 1
        if not answer.score:
            answer.trying += 1
        db_sess.commit()
        return redirect('/')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="run WEB server")
    parser.add_argument('host', default='127.0.0.1', metavar='host', nargs='?',
                        type=str, help='the hostname to listen on')
    parser.add_argument('port', default=5000, type=int,
                        help='the port of the webserver')
    args = parser.parse_args()
    app.run(args.host, args.port)
