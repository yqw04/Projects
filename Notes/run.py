from datetime import datetime
from flask import Flask, redirect, render_template, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Length, input_required

app = Flask(__name__)  # tells app where python module is
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  # connects to database
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#A many-to-many table for linking notes and their tags.
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('notes.note_id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
)

# Notes table with its attributes and relationships
class Notes(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_name = db.Column(db.String(40))
    note_text = db.Column(db.String(1000))
    note_color = db.Column(db.String(20))
    session_id = db.Column(db.String(50)) 
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    tags = db.relationship('Tag', secondary=note_tags, backref=db.backref('notes', lazy='joined'))

# Tags that users add to notes
class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Form to allow users to add new note to database
class NotesForm(FlaskForm):
    note_text = TextAreaField('Note text', validators=[input_required(), Length(1, 2000)])
    note_name = StringField('Note name', validators=[input_required(), Length(1, 100)])
    note_color = SelectField('Note Color', choices=[('blue', 'Blue'), ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('grey', 'Grey')], validators=[input_required()])
    tags = StringField('Tags (comma-separated)')    
    submit = SubmitField('Submit')

# Ensures its different 
@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = ""

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    session_id = session['session_id']
    all_note = Notes.query.filter_by(session_id=session_id, is_deleted=False).all()
    new_note_form = NotesForm()
    tags = Tag.query.join(note_tags).join(Notes).filter(Notes.session_id == session_id).distinct().all()

    # Adds new note to database
    if new_note_form.validate_on_submit():
        # Seperates multiple tags
        tags_list = [tag.strip() for tag in new_note_form.tags.data.split(',')]

        note = Notes (
            note_name=new_note_form.note_name.data,
            note_text=new_note_form.note_text.data,
            note_color=new_note_form.note_color.data,
            session_id=session_id
        )
        # Adds new tags to database
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)
        db.session.add(note)
        db.session.commit()
        update_tags()
        return redirect(url_for('home'))
    
    return render_template('home.html', note=all_note, form=new_note_form, tags=tags)

# Route to display tags
@app.route('/tag/<string:tag_name>', methods=['GET'])
def filter_by_tag(tag_name):
    session_id = session['session_id']
    tag = Tag.query.filter_by(name=tag_name,).first()
    if tag:
        filtered_notes = Notes.query.filter(Notes.tags.any(name=tag_name), Notes.is_deleted == False).all()
    else:
        filtered_notes = []
    tags = Tag.query.join(note_tags).join(Notes).filter(Notes.session_id == session_id).distinct().all()
    new_note_form = NotesForm()
    return render_template('home.html', note=filtered_notes, form=new_note_form, tags=tags, tag_name=tag_name)

# Route to move note to delete page
@app.route('/move_to_delete/<int:note_id>', methods=['POST'])
def move_to_delete(note_id):
    note = Notes.query.get(note_id)
    if note:
        note.is_deleted = True
        db.session.commit()
    return redirect(url_for('home'))

# Route for the delete page
@app.route('/delete')
def delete_page():
    session_id = session['session_id']
    deleted_notes = Notes.query.filter_by(session_id=session_id, is_deleted=True).all()
    tags = Tag.query.join(note_tags).join(Notes).filter(Notes.session_id == session_id).distinct().all()
    return render_template('delete.html', note=deleted_notes, tags=tags)

# Route to permanently delete note from database
@app.route('/delete/perm_delete/<int:note_id>', methods=['POST'])
def perm_delete(note_id):
    delete_note = Notes.query.get(note_id)

    if delete_note:
        db.session.delete(delete_note)
        db.session.commit()
    update_tags()
    return redirect(url_for('delete_page'))

# Route to move the deleted note back to home page
@app.route('/delete/restore/<int:note_id>', methods=['POST'])
def restore(note_id):
    restored_note = Notes.query.get(note_id)
    if restored_note:
        restored_note.is_deleted = False
        db.session.commit()

        for tag in restored_note.tags:
            existing_tag = Tag.query.filter_by(name=tag.name).first()
            if not existing_tag:
                new_tag = Tag(name=tag.name)
                db.session.add(new_tag)
        db.session.commit()
    return redirect(url_for('delete_page'))

# Delete tags that are not associated to any notes
def update_tags():
    all_tags = Tag.query.all()
    for tag in all_tags:
        notes_with_tag = Notes.query.filter(Notes.tags.any(name=tag.name)).all()
        if not notes_with_tag:
            db.session.delete(tag)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables before running the app
    app.run(debug=True)
