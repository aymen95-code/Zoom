from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from Zoom import db
from Zoom.post.forms import PostForm, UpdatePostForm, CommentForm
from Zoom.models import Post, Comment
from Zoom.utils import save_pic
post = Blueprint('post', __name__)

@post.route('/post/new', methods=['GET', 'POST'])
@login_required
def add_post():
   form = PostForm()
   if form.validate_on_submit():
      folder_path = 'static/post_pics'
      cover_pic = save_pic(form.picture.data, folder_path)
      cover_pic_file = cover_pic
      post = Post(title=form.title.data, snippet=form.snippet.data, post_content=form.content.data, cover_pic_file=cover_pic_file, author=current_user)
      db.session.add(post)
      db.session.commit()
      flash('Your post has been posted', 'success')
      return redirect(url_for('main.home'))
   return render_template('addpost.html', title="add Post", form=form)

@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def get_post(post_id):
   post = Post.query.get_or_404(post_id)
   form = CommentForm()
   if form.validate_on_submit():
      # Creating a new Comment object
      comment = Comment(comment_content=form.body.data, author=current_user, post=post)
      db.session.add(comment)
      db.session.commit()
      return redirect(url_for('post.get_post', post_id=post.id))
   # getting comments for the current post
   comments = Comment.query.filter_by(post_id=post_id).all()
   return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@post.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
   post = Post.query.get_or_404(post_id)
   if post.author != current_user:
      abort(403)
   form = UpdatePostForm()
   if form.validate_on_submit():
      post.title = form.title.data
      post.snippet = form.snippet.data
      post.post_content = form.content.data
      if form.picture.data:
         folder_path = 'static/post_pics'
         post.cover_pic_file = save_pic(form.picture.data, folder_path)
      db.session.commit()
      flash('Your post has been updated', 'success')
      return redirect(url_for('post.get_post', post_id=post.id))
   form.title.data = post.title
   form.snippet.data = post.snippet
   form.content.data = post.post_content
   return render_template('editPost.html', title="add Post", form=form)

@post.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
   post = Post.query.get_or_404(post_id)
   if post.author != current_user:
      abort(403)
   db.session.delete(post)
   db.session.commit()
   flash('Post Has been deleted!!', 'success')
   return redirect(url_for('main.home'))

@post.route('/post/<int:post_id>/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id, post_id):
   comment = Comment.query.get_or_404(comment_id)
   post = Post.query.get_or_404(post_id)
   if comment.author != current_user:
      abort(403)
   db.session.delete(comment)
   db.session.commit()
   return redirect(url_for('post.get_post', post_id=post.id))

      