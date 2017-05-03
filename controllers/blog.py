from flask import Blueprint, render_template
from models import User, Post, Comment, db, sidebar_data, Tag
from forms import CommentForm
from datetime import datetime

blog_blueprint = Blueprint('blog', __name__,  url_prefix='/blog')


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def index(page=1):
    posts = Post.query.order_by(
        Post.date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template('blog/index.html',
                           posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(form.title.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()
    the_post = Post.query.get_or_404(post_id)
    tags = the_post.tags
    comments = the_post.comments.order_by(
        Comment.date.desc()
    ).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/post.html', post=the_post, recent=recent,
                           top_tags=top_tags, tags=tags, comments=comments, form=form)


@blog_blueprint.route('/tag/<tag_id>')
def tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    posts = tag.posts.order_by(Post.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('blog/tag.html', tag=tag, posts=posts,
                           recent=recent, top_tags=top_tags)


@blog_blueprint.route('/user/username')  # use user_id instead username
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    recent, top_tags = sidebar_data()
    return render_template('blog/user.html', user=user,
                           recent=recent, top_tags=top_tags, posts=posts)
