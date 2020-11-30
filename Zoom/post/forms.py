from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    snippet = StringField('Post Snippet', validators=[DataRequired()])
    content = CKEditorField('Post Content', validators=[DataRequired()])
    picture = FileField('Upload post cover', validators=[FileAllowed(['jpg', 'png', 'jpeg']), FileRequired()])
    submit = SubmitField('Publish')

class UpdatePostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    snippet = StringField('Post Snippet', validators=[DataRequired()])
    content = CKEditorField('Post Content', validators=[DataRequired()])
    picture = FileField('Upload post cover', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

class CommentForm(FlaskForm):
    body = StringField('Comment Content', validators=[DataRequired()])
    submit = SubmitField('Publish')