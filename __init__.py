from flask import Flask, redirect, url_for ,render_template

from config import DevConfig
from controllers.blog import blog_blueprint
from controllers.main import main_blueprint
from extensions import bcrypt
from models import db

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
bcrypt.init_app(app)


@app.route('/')
def index1():
    return redirect(url_for('blog.index'))


@app.route('/f1')
def f1():
    return render_template('blog/base.html')

app.register_blueprint(blog_blueprint)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run()
