from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth

def create_app():
    app = Flask(__name__)
    app.secret_key = 'myscretkey'
    oauth = OAuth(app)
    github = oauth.register(
      name='github',
      client_id='c7d6c9e2e39cab20c080',
      client_secret='7177f59a4ee4f28de1b0fcf0c1c4f3c9b4d9aa14',
      access_token_url='https://github.com/login/oauth/access_token',
      access_token_params=None,
      authorize_url='https://github.com/login/oauth/authorize',
      authorize_params=None,
      api_base_url='https://api.github.com/',
      client_kwargs={'scope': 'user:email'},
    )
    @app.route('/')
    def index():
      return "Hello"
    
    @app.route('/login')
    def login():
      return render_template('login.html')

    @app.route('/github/login')
    def githublogin():
      github = oauth.create_client('github')
      redirect_uri = url_for('authorize', _external=True)
      return github.authorize_redirect(redirect_uri)
    @app.route('/authorize')
    def authorize():
      github = oauth.create_client('github')
      token = github.authorize_access_token()
      resp = github.get('user', token=token)
      profile = resp.json()
      print(profile, token)
      return redirect('/')
    return app