# -*- coding: utf-8 -*-
import datetime
import os

from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from form import NewNoteForm, EditNoteForm, DeleteNoteForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# , merge, delete
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    body = db.Column(db.Text)
    comments = db.relationship('Comment', back_populates='post')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)


@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Comment=Comment, Draft=Draft)















# edit = CKEditor(app)
#
#
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     timestemp = db.Column(db.DateTime)
#
#     @property
#     def time(self):
#         return self.timestemp.strftime('%Y-%m-%d')
#
#     def __repr__(self):
#         return '<Note %r>' % self.body
#
#
# @app.route('/new', methods=['GET', 'POST'])
# def new_note():
#     form = NewNoteForm()
#     if form.validate_on_submit():
#         note = Note(body=form.body.data)
#         note.timestemp = datetime.datetime.now()
#         db.session.add(note)
#         db.session.commit()
#         flash('Your note is saved!')
#         return redirect(url_for('index'))
#     elif form.csrf_token.errors:
#         for error in form.csrf_token.errors:
#             flash(error)
#     return render_template('new_note.html', form=form)
#
#
# @app.route('/')
# def index():
#     form = DeleteNoteForm()
#     note_list = Note.query.all()
#     return render_template('index.html', note_list=note_list, form=form)
#
#
# @app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
# def edit_note(note_id):
#     form = EditNoteForm()
#     note = Note.query.get(note_id)
#     if form.validate_on_submit():
#         note.body = form.body.data
#         note.timestemp = datetime.datetime.now()
#         db.session.commit()
#         flash('Your note is update!')
#         return redirect(url_for('index'))
#     elif form.csrf_token.errors:
#         for error in form.csrf_token.errors:
#             flash(error)
#     form.body.data = note.body
#     return render_template('edit_note.html', form=form)
#
#
# @app.route('/delete/<int:note_id>', methods=['POST'])
# def delete(note_id):
#     form = DeleteNoteForm()
#     if form.validate_on_submit():
#         note = Note.query.get(note_id)
#         db.session.delete(note)
#         db.session.commit()
#         flash('Your Note is deleted!')
#     else:
#         abort(400)
#     return redirect(url_for('index'))
