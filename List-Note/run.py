from flask import Flask, redirect, render_template, url_for, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Length, input_required
from datetime import datetime

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# List Section
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', backref=db.backref('items', lazy=True))

# Ability to add new list, starts of empty - Home page
class ListForm(FlaskForm):
    new_list = TextAreaField('Add new List', validators=[input_required(), Length(1, 2000)])
    submit = SubmitField('Submit')

# Ability to add item to list - Single List page
class ItemForm(FlaskForm):
    new_item = StringField('Add to List:', validators=[input_required(), Length(1, 2000)])
    submit = SubmitField('Add Item')

# Allow sorting the items - Both pages
class OrderSort(FlaskForm): 
    order = SelectField('Sort', choices=[('---', '---'), ('a-z', 'A-Z')])
    submit = SubmitField('Sort', name='sort_submit')

# Allows user to search for lists and items - Both pages
class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[Length(min=1, max=200)], render_kw={"placeholder": "Search..."})
    submit = SubmitField('Search', name='search_submit')

# Ability to change the layout - Home page
class LayoutForm(FlaskForm):
    layout = SelectField('Layout', choices=[('boxes', 'Boxes'), ('lines', 'Lines')])
    submit = SubmitField('Change Layout',  name='layout_submit')

# Ability to change the layout - Single List page
class SingleListLayoutForm(FlaskForm):
    layout = SelectField('Layout', choices=[('single-column', 'Single Column'), ('two-column', 'Two Columns')])
    submit = SubmitField('Change Layout', name='single_list_layout_submit')

# Allows user to change the style of bullet points - Single List page
class ListStyleForm(FlaskForm):
    list_style = SelectField('List Style', choices=[('default', 'Default'), ('decimal', 'Numbers')]) 
    submit = SubmitField('Apply Style', name='apply_style')

# Notes Section
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

# Home page - show lists
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/list', methods=['GET', 'POST'])
def list_page():
    new_list_form = ListForm()
    order_form = OrderSort()
    search_form = SearchForm()
    layout_form = LayoutForm()

    # Handle new list creation
    if new_list_form.validate_on_submit() and 'submit' in request.form:
        new_list = List(name=new_list_form.new_list.data)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('list_page'))

    lists = List.query.all()

    # Handle search functionality
    if 'search_submit' in request.form and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        if search_query:
            lists = List.query.filter(List.name.contains(search_query)).all()

    # Handle layout selection
    if 'layout_submit' in request.form and layout_form.validate_on_submit():
        session['layout'] = layout_form.layout.data

    # Retrieve the layout from the session
    layout = session.get('layout', 'boxes')
    layout_form.layout.data = layout
    
    # Handle sorting functionality
    if 'sort_submit' in request.form and order_form.validate_on_submit():
        order = List.id
        if order_form.order.data == 'a-z':
            order = List.name
        lists = List.query.order_by(order).all()

    return render_template('list.html', new_list_form=new_list_form, search_form=search_form, order_form=order_form, lists=lists, layout_form=layout_form, layout=layout)

# Single list page - Show items within list
@app.route('/Single_List/<list_id>', methods = ['GET', 'POST']) 
def Single_List(list_id):
    lists = List.query.filter_by(id = list_id).first() 
    new_item_form = ItemForm()
    order_form = OrderSort()
    search_form = SearchForm()
    single_list_layout_form = SingleListLayoutForm()
    list_style_form = ListStyleForm()

    # Handle new list creation
    if new_item_form.validate_on_submit():
            new_item = Item(name=new_item_form.new_item.data, list_id = list_id)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('Single_List', list_id=list_id))

    # Handle layout selection
    if single_list_layout_form.validate_on_submit() and 'single_list_layout_submit' in request.form:
        session['single_list_layout'] = single_list_layout_form.layout.data

    # Handle bullet point style selection
    if list_style_form.validate_on_submit() and 'apply_style' in request.form:
        session['list_style'] = list_style_form.list_style.data

    layout = session.get('single_list_layout', 'single-column')
    list_style = session.get('list_style', 'decimal')
    single_list_layout_form.layout.data = layout
    list_style_form.list_style.data = list_style

    items = lists.items
    if 'search_submit' in request.form and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        if search_query:
            items = Item.query.filter(Item.name.contains(search_query)).all()

    # Handle sorting functionality
    if 'sort_submit' in request.form and order_form.validate_on_submit():
        order = Item.id
        if order_form.order.data == 'a-z':
            order = Item.name
        items = Item.query.filter_by(list_id=list_id).order_by(order).all()

    return render_template('single_list.html', lists=lists, new_item_form=new_item_form, single_list_layout_form=single_list_layout_form, list_style_form=list_style_form, 
                           layout=layout, order_form=order_form, items=items, search_form=search_form, list_style=list_style)

# Allows user to delete lists
@app.route('/delete_list_item/<int:id>', methods=['POST'])
def delete_list_item(id):
    delete_job = List.query.get(id)

    if delete_job:
        db.session.delete(delete_job)
        db.session.commit()
    return redirect(url_for('list_page'))

# Allows user to delete items from lists
@app.route('/delete_single_list_item/<int:list_id>/<int:id>', methods=['POST'])
def delete_single_list_item(list_id, id):
    delete_item = Item.query.get(id)

    if delete_item:
        db.session.delete(delete_item)
        db.session.commit()
    return redirect(url_for('Single_List', list_id=list_id))

# Notes 
@app.route('/note', methods=['GET', 'POST'])
def note_page():
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
        return redirect(url_for('note_page'))
    
    return render_template('note.html', note=all_note, form=new_note_form, tags=tags)

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
    return render_template('note.html', note=filtered_notes, form=new_note_form, tags=tags, tag_name=tag_name)

# Route to move note to delete page
@app.route('/move_to_delete/<int:note_id>', methods=['POST'])
def move_to_delete(note_id):
    note = Notes.query.get(note_id)
    if note:
        note.is_deleted = True
        db.session.commit()
    return redirect(url_for('note_page'))

# Route for the delete page
@app.route('/delete')
def note_delete():
    session_id = session['session_id']
    deleted_notes = Notes.query.filter_by(session_id=session_id, is_deleted=True).all()
    tags = Tag.query.join(note_tags).join(Notes).filter(Notes.session_id == session_id).distinct().all()
    return render_template('notedelete.html', note=deleted_notes, tags=tags)

# Route to permanently delete note from database
@app.route('/delete/perm_delete/<int:note_id>', methods=['POST'])
def perm_delete(note_id):
    delete_note = Notes.query.get(note_id)

    if delete_note:
        db.session.delete(delete_note)
        db.session.commit()
    update_tags()
    return redirect(url_for('note_delete'))

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
    return redirect(url_for('note_delete'))

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
        db.create_all()  
    app.run(debug=True)