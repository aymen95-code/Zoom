from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from Zoom import db
from Zoom.models import User, Post
from Zoom.utils import save_pic
from Zoom.user.forms import UpdateAccountForm
user = Blueprint('user', __name__)

@user.route('/user/<string:username>')
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    # a path to the current user profile pic
    image_file = url_for('static', filename='profile_pics/' + user.profile_file)    
    return render_template('profile.html', title=user.username, user=user, posts=posts, image_file=image_file)

@user.route('/user/<string:username>/update', methods=['GET', 'POST'])
@login_required
def update_account(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user != user:
        abort(403)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            folder_path = 'static/profile_pics'
            profile_pic = save_pic(form.picture.data, folder_path)
            user.profile_file = profile_pic
        user.username = form.username.data
        user.email = form.email.data
        user.gender = form.gender.data
        db.session.commit()
        return redirect(url_for('user.account', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.gender.data = user.gender
    return render_template('editProfile.html', title="Edit Profile", form=form)
    
@user.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.username} Has been deleted', 'success')
    return redirect(url_for('auth.logout'))
    