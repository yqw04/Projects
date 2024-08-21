from flask import Flask, redirect, render_template, request, url_for
from flask import session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #tells app where python module is
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3' #connects to database
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.app_context().push()

#class - like a blueprint, template for creating objects
class Item(db.Model): #shows logical structure of database
    id = db.Column(db.Integer(), primary_key = True) #primary key - uniquely identifies each item in database table 
    name = db.Column(db.String(length = 30), nullable = False, unique = True) #nullable - dont want it to be null/empty
    price = db.Column(db.Integer(), nullable = False)
    env_impact = db.Column(db.String(), nullable = False)
    description = db.Column(db.String(length = 1000), nullable = False, unique = True)
    image = db.Column(db.String(length = 1000), nullable = False)
    quantity = db.Column(db.Integer(), nullable = False)

    def __repr__(self): #string representation of object
        return f'Item {self.name}' #returns the name rather than the variable
    
class Sort(FlaskForm): #create web forms
    order = SelectField('Sort', choices = [('name', 'Name'), ('price', 'Price'), ('environmental impact', 'Environmental impact')])
    submit = SubmitField('Select', name='sort_submit')

class AddBasket(FlaskForm):
    submit = SubmitField('Add to Basket')

class Checkout(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    card_no = StringField("Card Number", validators=[Length(16, 16), DataRequired()]) #validators - checks
    cvc = StringField("CVC", validators=[Length(3, 3), DataRequired()]) #2 no. in Length as it is min and max
    exp_date = DateField("Expire on", validators=[DataRequired()])
    submit = SubmitField("Submit")

#app.route - used to map the specific URL with the associated function intended to perform some task
@app.route('/', methods=['GET', 'POST']) #get data | send data to server
def Home():
    form = AddBasket()
    new_arrivals = Item.query.filter(Item.id.in_([7, 8, 9])).all()  # Specific IDs for the homepage sections
    popular = Item.query.filter(Item.id.in_([10, 11, 12])).all()  # Specific IDs for the homepage sections

    if request.method == 'POST':  # Check if the form was submitted
        item_id = request.form.get('item_id')
        if item_id:
            return add_to_basket(item_id)  # Call the function to add to the basket
    return render_template('Home.html', new_arrivals=new_arrivals, popular=popular, form=form) #look for templates in the templates folder.

#app.route - used to map the specific URL with the associated function intended to perform some task
@app.route('/All', methods=['GET', 'POST']) #get data | send data to server
def All():
    form = Sort() #for sorting
    order = Item.name #automatically in name order
    if form.validate_on_submit(): #checks if request is post, and data is accepted by all validators
        if form.order.data == 'price':
            order = Item.price
        elif form.order.data == 'environmental impact':
            order = Item.env_impact
    products = Item.query.order_by(order).all() #ordering all items in order
    return render_template('All.html', form = form, products = products) #look for templates in the templates folder.

@app.route('/Product/<item_id>', methods = ['GET', 'POST']) #routing to id page
def Product(item_id):
    form = AddBasket() #flaskform
    Product = Item.query.filter_by(id = item_id).first() #filtering database to only show items with same id
    Basketitem = Basket() 
    if form.validate_on_submit(): 
        item_dict = {
            'id': Product.id,
            'name': Product.name,
            'price': Product.price,
            'env_impact': Product.env_impact,
            'description': Product.description,
            'image': Product.image,
            'quantity': Product.quantity
        }
        Basketitem.append(item_dict) #adding item to basket 
        session.modified = True #saves session when it changes
        return redirect('/cart') #returns a response object and redirects the user to another target location
    return render_template('Single_product.html', Product = Product, form = form)

def price(Basketitem):
    total_price = 0
    for item in Basketitem: #looping over all items, adding the price
        total_price += item['price'] * item['quantity']
    return round(total_price, 2)

def add_to_basket(item_id):
    product = Item.query.get(item_id)  # Get the item by ID
    basket = Basket()
    item_dict = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'env_impact': product.env_impact,
        'description': product.description,
        'image': product.image,
        'quantity': product.quantity
    }
    basket.append(item_dict)  # Add item to the basket
    session.modified = True  # Save session
    return redirect('/cart')  # Redirect to the cart

def Basket(): #create new basket if nothing in basket 
    if 'Basket' not in session: #data that is required to be saved in the session is stored in a temporary directory on the server
        session['Basket'] = [] #empty basket
    return session['Basket']

@app.route('/cart')
def cart():
    basket = Basket() #items in basket
    total = price(basket)
    amount = quantity(basket)
    return render_template('cart.html', basket = basket, total = total, amount = amount, len = len) 

def quantity(Basketitem):
    amount = 0
    for item in Basketitem: #looping over all items, adding the quantity
        amount = amount + item['quantity']
    return amount  

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    basket = Basket()
    for i in range(len(basket)):
        quantity = int(request.form.get(f'quantity_{i}'))
        basket[i]['quantity'] = quantity
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/delete/<int:item>')
def delete(item):
    del session['Basket'][item] #removes the item
    session.modified = True
    return redirect('/cart')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = Checkout()
    basket = Basket()
    total = price(basket)
    card_number = form.card_no.data #data from chechout form
    cvc = form.cvc.data
    error = ''
    if form.validate_on_submit():
        if not card_number.isdigit() or not cvc.isdigit(): 
            error = "remove letters"
        elif len(card_number) != 16 or len(cvc) != 3:
            error = "please add required amount"
        else:
            return redirect(url_for('success'))
    return render_template('checkout.html', total = total, form = form, error = error, basket = basket, len = len)

@app.route('/success')
def success():
    basket = Basket()
    total = price(basket)
    return render_template('success.html', basket = basket, total = total, len = len)

if __name__ == '__main__':  
    app.run(debug=True)

