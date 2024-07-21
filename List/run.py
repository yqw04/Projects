from flask import Flask, redirect, render_template, url_for, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Length, input_required

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

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

# Home page - show lists
@app.route('/', methods=['GET', 'POST'])
def home():
    new_list_form = ListForm()
    order_form = OrderSort()
    search_form = SearchForm()
    layout_form = LayoutForm()

    # Handle new list creation
    if new_list_form.validate_on_submit() and 'submit' in request.form:
        new_list = List(name=new_list_form.new_list.data)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('home'))

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

    return render_template('home.html', new_list_form=new_list_form, search_form=search_form, order_form=order_form, lists=lists, layout_form=layout_form, layout=layout)


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
    return redirect(url_for('home'))

# Allows user to delete items from lists
@app.route('/delete_single_list_item/<int:list_id>/<int:id>', methods=['POST'])
def delete_single_list_item(list_id, id):
    delete_item = Item.query.get(id)

    if delete_item:
        db.session.delete(delete_item)
        db.session.commit()
    return redirect(url_for('Single_List', list_id=list_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)