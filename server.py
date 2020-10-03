import flask
import flask_login


app = flask.Flask(__name__)
app.secret_key = 'your-super-secret-key'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'test@test.test': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    user.us_authenticated = request.form['password'] == users[email]['password']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect('admin')

    return 'Bad login'


@app.route('/admin')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect('login')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
