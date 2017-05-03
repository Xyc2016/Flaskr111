from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User ' + self.username + '>'


tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref(
            'posts',
            lazy='dynamic'
        )
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Post ' + self.title + '>'


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Comment ' + self.title + '>'


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag ' + self.title + '>'


def sidebar_data():
    recent = Post.query.order_by(
        Post.date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    posts = Post.query.order_by(
        Post.date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('index.html',
                           posts=posts, recent=recent, top_tags=top_tags)


@app.route('/post/<int:post_id>')
def post(post_id):
    the_post = Post.query.get_or_404(post_id)
    tags = the_post.tags
    comments = the_post.comments.order_by(
        Comment.date.desc()
    ).all()
    recent, top_tags = sidebar_data()
    return render_template('post.html', post=the_post, recent=recent,
                           top_tags=top_tags, tags=tags, comments=comments)


@app.route('/tag/<string:tag_title>')  # use tag_id instead tag_title
def tag(tag_title):
    tag = Tag.query.filter_by(title=tag_title).first_or_404()
    posts = tag.posts.order_by(Post.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('tag.html', tag=tag, posts=posts,
                           recent=recent, top_tags=top_tags)


@app.route('/user/username')  # use user_id instead username
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    recent, top_tags = sidebar_data()
    return render_template('user.html', user=user,
                           recent=recent, top_tags=top_tags)



if __name__ == '__main__':
    app.run()
