from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class NewNoteForm(FlaskForm):
    body = CKEditorField('body', validators=[DataRequired()])
    # body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')


class DeleteNoteForm(FlaskForm):
    delete = SubmitField('Delete')
