import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_HEIGHT = 500
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'mono-blue'

"""
    it's best practice to save the information outside of our application (Environments variable)
"""