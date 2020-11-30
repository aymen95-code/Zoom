from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from Zoom.models import Post, Comment

main = Blueprint('main', __name__)

@main.route('/')
def home():
   if current_user.is_authenticated:
      posts = Post.query.order_by(Post.date_posted.desc()).all()
      profile_file_source = url_for('static', filename='profile_pics/' + current_user.profile_file)
      return render_template('home_auth.html', title="Home", posts=posts, profile_file_source=profile_file_source)
   return render_template('home.html', title="Home")