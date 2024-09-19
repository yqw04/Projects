from flask import Flask, redirect, render_template, request, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, input_required, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) #tells app where python module is
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3' #connects to database
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.app_context().push()
lm = LoginManager(app)
lm.login_view = 'login'

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

class CategoryForm(FlaskForm):
    category = SelectField('Category', choices = [('all', 'All'), ('pillow', 'Pillow'), ('more', 'More'),  ('blanket', 'Blanket'),  
        ('sets', 'Sets'),  ('extra', 'Extra'),  ('new', 'New'),  ('popular', 'Popular')])
    
class AddBasket(FlaskForm):
    submit = SubmitField('Add to Basket')

class Checkout(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    card_no = StringField("Card Number", validators = [Length(16, 16), DataRequired()]) #validators - checks
    cvc = StringField("CVC", validators = [Length(3, 3), DataRequired()]) #2 no. in Length as it is min and max
    exp_date = DateField("Expire on", validators = [DataRequired()])
    submit = SubmitField("Submit")

# creates the signup form to be used by routes
class SignupForm(FlaskForm):
    username = StringField('Username', validators = [input_required(), Length(1, 20)])
    password = PasswordField('Password', validators = [input_required()])
    verify_password = PasswordField('Verify password', validators = [input_required(), EqualTo('password', message = 'Passwords must match')])
    student = BooleanField('Student')
    submit = SubmitField('Submit')

# creates the login form to be used by routes
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [input_required(), Length(1, 20)])
    password = PasswordField('Password', validators = [input_required()])
    submit = SubmitField('Submit')

# Table to link users and jobs directly which is used for managing job assignments.
class UserBasketLink(db.Model):
    __tablename__ = 'user_basket_link'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key = True)
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key = True)
    quantity = db.Column(db.Integer, nullable=False, default = 1)  # Add this line

# A user Table defining attributes for user information and relationships with the other models.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(16), index = True, unique = True)
    password_hash = db.Column(db.String(64))
    student = db.Column(db.Boolean)
    basket = db.relationship('Item', secondary = 'user_basket_link', backref = db.backref('assigned_users', lazy = 'dynamic'))
    
    # gets the current users id
    def get_id(self):
        return str(self.user_id)

    # sets passwords hashes and sets the current password to the hash creatde
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # checks that the password inputted is correct
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_student(self, student):
        self.student = student
    
    # registeres a new user
    @staticmethod
    def register(username, password, student):
        user = User(username = username)
        user.set_password(password)
        user.set_student(student)
        db.session.add(user)
        db.session.commit()
        return user
    
    # needed for getting users
    def __repr__(self):
        return '<User {0}>'.format(self.username)

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    subject = SelectField('Subject', choices = [('order placement', 'Order Placement'), ('shipment related', 'Shipment Related'), ('product related', 'Product Related'), 
    ('payment related', 'Payment Related'), ('account related', 'Account Related'),('general enquiry', 'General Enquiry'), ('other', 'Other')])
    other = StringField('Other', validators=[])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')



# route for the login page
# the login page is the first page and so its URL is just blank
@app.route('/', methods = ['GET', 'POST'])
def login():
    # form is the variable for the logins form
    login_form = LoginForm()

    # if the form is submitted the checks if user is in database and checks password
    # if user is verified takes to home page and log ins the current user as the current user
    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()

        if user is None:
            return render_template('login.html', form = login_form, error = 'invalid username')

        if not user.verify_password(login_form.password.data):
            return render_template('login.html', form = login_form, error = 'invalid password')

        login_user(user)

        return redirect(url_for('Home'))
    return render_template('login.html', form = login_form)

# route for the signup page which takes you to the home page and the URL of the base URL/signup
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    # signup_form is the variable for the logins form
    signup_form = SignupForm()

    # if form is submitted then creates a new user adding the submitted details to the database and takes user to login
    if signup_form.validate_on_submit():

        password_in = str(signup_form.password.data)
        username_in = str(signup_form.username.data)
        student_in = bool(signup_form.student.data)

        if User.query.filter_by(username=username_in).first() is None:
            
            User.register(username_in, password_in, student_in)
            return redirect(url_for('login'))

        else:
            return render_template('signup.html', form = signup_form, exists = True)


    return render_template('signup.html', form = signup_form)

# routing for the logout which takes you to the login page and logs our the current user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# is needed when working with users
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.route - used to map the specific URL with the associated function intended to perform some task
@app.route('/home', methods = ['GET', 'POST']) # get data | send data to server
def Home():
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()

    form = AddBasket()
    new_arrivals = Item.query.filter(Item.id.in_([7, 8, 9])).all()  # Specific IDs for the homepage sections
    popular = Item.query.filter(Item.id.in_([10, 11, 12])).all()  # Specific IDs for the homepage sections

    if form.validate_on_submit():
        item_id = request.form.get('item_id')
        if item_id:
            return add_to_basket(item_id)  # Call the function to add to the basket
    return render_template('Home.html', new_arrivals = new_arrivals, popular = popular, form = form, user = user) # look for templates in the templates folder.

@app.route('/All', methods=['GET', 'POST']) # get data | send data to server
def All():
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()
    category = request.args.get('category', 'all')
    sort_order = request.args.get('order', 'name') 

    category_form = CategoryForm()
    form = Sort() # for sorting
    category_form.process(category=category)
    form.process(order=sort_order)
    if sort_order == 'price':
        order = Item.price
    elif sort_order == 'environmental impact':
        order = Item.env_impact
    else:
        order = Item.name  # default in name order

    if category == 'more' :
        products = Item.query.filter(Item.id.in_([13, 14, 15, 16, 17, 18, 19, 20, 21])).order_by(order).all()
    elif category == 'pillow':
        products = Item.query.filter(Item.id.in_([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])).order_by(order).all()
    elif category == 'blanket':
        products = Item.query.filter(Item.id.in_([13, 14, 15])).order_by(order).all()
    elif category == 'sets':
        products = Item.query.filter(Item.id.in_([16, 17, 18])).order_by(order).all()
    elif category == 'extra':
        products = Item.query.filter(Item.id.in_([19, 20, 21])).order_by(order).all()
    elif category == 'new':
        products = Item.query.filter(Item.id.in_([7, 8, 9])).order_by(order).all()
    elif category == 'popular':
        products = Item.query.filter(Item.id.in_([10, 11, 12])).order_by(order).all()
    else:
        products = Item.query.order_by(order).all() 

    return render_template('All.html', form=form, products=products, category_form=category_form, category = category, user=user)


# Update the Product route to correctly handle adding items to the basket.
@app.route('/Product/<item_id>', methods = ['GET', 'POST'])
def Product(item_id):
    form = AddBasket()
    product = Item.query.filter_by(id = item_id).first()

    if form.validate_on_submit():
        item_id = request.form.get('item_id')
        if item_id:
            return add_to_basket(item_id)  # Call the function to add to the basket

    return render_template('Single_product.html', Product = product, form = form)

@app.route('/add_to_basket/<int:item_id>', methods = ['POST'])
@login_required
def add_to_basket(item_id):
    user_id = current_user.get_id()
    
    # Check if the item already exists in the basket
    existing_item = UserBasketLink.query.filter_by(user_id = user_id, id = item_id).first()

    if existing_item:
        # If the item exists, increase the quantity
        existing_item.quantity += 1
    else:
        # If the item does not exist, create a new entry
        new_item = UserBasketLink(user_id = user_id, id = item_id, quantity = 1)
        db.session.add(new_item)

    # Commit the changes
    db.session.commit()

    return redirect(url_for('cart'))

def Basket():
    current_user_id = current_user.get_id()
    
    # Check what items and links are present in the database
    basket_items = db.session.query(Item, UserBasketLink).join(UserBasketLink).filter(UserBasketLink.user_id == current_user_id).all()

    basket = []
    for item, link in basket_items:
        basket_item = {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'env_impact': item.env_impact,
            'description': item.description,
            'image': item.image,
            'quantity': link.quantity 
        }
        basket.append(basket_item)

    return basket

@app.route('/cart')
def cart():
    basket = Basket() # items in basket
    total = price(basket)
    amount = quantity(basket)
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()
    return render_template('cart.html', basket = basket, total = total, amount = amount, len = len, user = user) 

def price(Basketitem):
    total_price = 0
    for item in Basketitem: # looping over all items, adding the price
        total_price += item['price'] * item['quantity']
    return round(total_price, 2)

def quantity(Basketitem): # total amount
    amount = 0
    for item in Basketitem: # looping over all items, adding the quantity
        amount = amount + item['quantity']
    return amount  

@app.route('/update_quantity/<int:item>', methods=['POST'])
def update_quantity(item):
    link = UserBasketLink.query.filter_by(user_id = current_user.get_id(), id = item).first()
    if link:
        # Get the new quantity from the form
        quantity = int(request.form.get('quantity'))
        if quantity > 0:  # Ensure the quantity is positive
            link.quantity = quantity
            db.session.commit()
        else:
            # Handle the case where quantity is 0 or less, maybe remove the item?
            db.session.delete(link)
            db.session.commit()
    return redirect(url_for('cart'))

@app.route('/delete/<int:item>')
def delete(item):
    link = UserBasketLink.query.filter_by(user_id = current_user.get_id(), id = item).first()
    if link:
        db.session.delete(link)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()
    form = Checkout()
    basket = Basket()
    total = price(basket)
    card_number = form.card_no.data # data from chechout form
    cvc = form.cvc.data
    error = ''
    if form.validate_on_submit():
        if not card_number.isdigit() or not cvc.isdigit(): 
            error = "remove letters"
        elif len(card_number) != 16 or len(cvc) != 3:
            error = "please add required amount"
        else:
            return redirect(url_for('success'))
    return render_template('checkout.html', total = total, form = form, error = error, basket = basket, len = len, user=user)

@app.route('/success')
def success():
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()
    basket = Basket()
    total = price(basket)
    return render_template('success.html', basket = basket, total = total, len = len, user=user)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    user = db.session.query(User).filter_by(user_id = current_user.get_id()).first()
    form = ContactForm()
    if form.validate_on_submit():
        # Handle the form submission
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        # Add logic to handle or store the contact form data
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))  # Redirect after successful submission

    return render_template('contact.html', form=form, user=user)

def insert_items():
    # Check if the database already contains items
    if Item.query.count() == 0:
        items_to_insert = [
            Item(
                name = 'Luxury Bamboo Pillow',
                price = 45.75,
                env_impact = '6.4kg(CO2e)',
                description = 'This pillow is perfect for anyone who wants to upgrade their sleep experience because it was made with comfort in mind. \
                    This luxuriously soft and elegant pillow offers exceptional support, comfort, and cosiness to your head and neck, making it the perfect \
                        choice for anybody who experiences neck, shoulder, or back problems. This means you''ll be able to breathe more easily and stay healthier \
                            while you sleep. Treat yourself to the finest sleep of your life with the help of this eco-friendly and luxurious bamboo pillow, which \
                                is guaranteed to offer the perfect amount of comfort.',
                image = 'images/pillow1.png',
                quantity = 1
            ),
            Item(
                name = 'Synthetic Memory Foam',
                price = 40.22,
                env_impact = '8.3kg(CO2e)',
                description = 'Made with cozy materials, it''s bound to make you fall asleep instantly. Super fluffy and silky, it will offer individualised \
                    comfort and support, so you will, without a doubt, wake up feeling refreshed and rejuvenated. Made with high-quality materials that are \
                        soft, long-lasting, and durable. This product is hypoallergenic and dust mites resistant, making this pillow perfect for anyone with \
                            allergies or sensitivities. Whether you sleep on your back, side, or stomach, this synthetic memory foam pillow is sure to provide \
                                you with a great night''s sleep. This pillow is a great investment in your sleep health and overall well-being and is sure to \
                                    provide you with years of comfortable and restful sleep.',
                image = 'images/pillow2.png',
                quantity = 1
            ),
            Item(
                name = 'Cushion Square Pillow',
                price = 15.94,
                env_impact = '5.9kg(CO2e)',
                description = 'This gorgeous, cozy pillow can give you a sense of luxury and elegance. This pillow is perfect for relaxing and lying down after a \
                    long day at work as it was made to conform to your head and neck for customised support and pressure relief. Made from a soft and durable \
                        fabric that is easy to care for. This pillow will make you feel instant comfort when you lie on it. Perfect for using as a headrest whether \
                            reading a book or watching television on the couch. Therefore, a cushion squared pillow is unquestionably something to think about if \
                                you''re seeking a superb pillow that will provide you both comfort and style.',
                image = 'images/pillow3.png',
                quantity = 1
            ),
            Item(
                name = 'Puzzle Shaped Pillow',
                price = 21.59,
                env_impact = '9.9kg(CO2e)',
                description = 'These extraordinary but amazing pillows are wonderful presents for your friends, family, or even yourself! Adding a bit of personality \
                    to your sofa, bed, or any other place. Display these pillows to brighten up the room and make it aesthetically pleasing. Easily adjustable and \
                        portable to find the perfect position in your room. To make your space stand out, it can be displayed alone, in a pair, or grouped with \
                            various colours and sizes, choose the one that best matches your personal style and decor. Whether you''re looking for a functional \
                                pillow or a decorative touch for your home, this puzzle shaped pillow is the perfect choice!',
                image = 'images/pillow4.png',
                quantity = 1
            ),
            Item(
                name = 'Fleece V Shape Pillow',
                price = 14.32,
                env_impact = '7.9kg(CO2e)',
                description = 'The V-shaped pillow is perfect for those who love to relax in bed or on the sofa. This unique shape was designed to provide the perfect \
                    amount of support for your neck and back, making it comfortable to sit up or lay down. The soft, fleece materials makes this pillow feel great \
                        against your skin. Give it a try and you will see why it is the perfect accessory for a cozy night in.',
                image = 'images/pillow5.png',
                quantity = 1
            ),
            Item(
                name = 'Round Pillow',
                price = 9.30,
                env_impact = '2.4kg(CO2e)',
                description = 'The round pillow is not only comfortable, but it''s also stylish, making this a must-have item. The pillow is perfect for adding a hint \
                    of colour to any room in your house. With a variety of colours and patterns you are sure to find the one that best matches your style. The Plus, \
                        it is a compact size and lightweight making it easy to store and move around, so you can use it wherever you go. Don''t settle for an \
                            uncomfortable pillow, upgrade to the round pillow today!',
                image = 'images/pillow6.png',
                quantity = 1
            ),
            Item(
                name = '2x Blue Melted Smiley Faces Pillow',
                price = 18.99,
                env_impact = '5.25kg(CO2e)',
                description = 'Bring a touch of playful whimsy to your space with our unique square pillow, featuring a quirky design of white smiling melting faces \
                    on a vibrant blue background. This eye-catching pillow is perfect for adding a pop of color and personality to any room. Whether placed on a \
                        couch, bed, or chair, it''s sure to spark conversation and brighten up your decor with its fun, artistic flair. Perfect for anyone looking \
                            to add a dash of creativity and comfort to their living space.',
                image = 'images/pillow7.png',
                quantity = 1
            ),
            Item(
                name = 'Rectangle Boho Pillow',
                price = 15.00,
                env_impact = '3.4kg(CO2e)',
                description = 'Elevate your space with this chic textured tufted fringe tassel pillow, a perfect blend of modern design and boho charm. Crafted from \
                    a soft, woven cotton blend, this pillow adds a cozy, tactile element to any room, featuring intricate decorative accents and fringed edges for \
                        a stylish twist. Whether it''s your living room, bedroom, or favorite reading nook, this versatile pillow is ideal for enhancing sofas, beds, \
                            benches, or even your office.',
                image = 'images/pillow8.png',
                quantity = 1
            ),
            Item(
                name = 'Floral Pattern Pillow',
                price = 7.99,
                env_impact = '2.1kg(CO2e)',
                description = 'Add a touch of charm to your home with this delightful cushion, featuring a delicate small flower pattern. Perfect for bringing a romantic \
                    and cozy vibe to your bed, armchair, or sofa, this versatile cover blends seamlessly with both solid-colored and patterned textiles. Its timeless \
                        design makes it a wonderful addition to any space, enhancing your décor with a subtle yet elegant flair.',
                image = 'images/pillow9.png',
                quantity = 1
            ),
            Item(
                name = 'Luxury Bounce Back Pillow Pair',
                price = 20.99,
                env_impact = '12.9kg(CO2e)',
                description = 'Crafted to maintain its shape night after night, these pillows offer the perfect blend of softness and support. The innovative bounce-back \
                    design ensures that your pillows retain their loft, providing consistent comfort. Encased in a breathable, hypoallergenic cotton cover, they are \
                        ideal for allergy sufferers and those seeking a restful night''s sleep. Whether you prefer to sleep on your back, side, or stomach, these pillows \
                            adapt to your needs, offering a luxurious sleep experience.',
                image = 'images/pillow10.png',
                quantity = 1
            ),
            Item(
                name = 'Checkerboard Fur Pillow',
                price = 9.99,
                env_impact = '4.8kg(CO2e)',
                description = 'Add a touch of timeless elegance to your living space with the Checkerboard Fur Pillow. This exquisite pillow features a checkerboard pattern,\
                      meticulously crafted with soft, plush faux fur that offers a luxurious feel and a stylish edge. Perfect for both contemporary and classic interiors, \
                        it provides exceptional comfort and a cosy atmosphere. Whether used as a statement piece on your sofa or a chic accent on your bed, this pillow \
                            effortlessly enhances your decor with its versatile charm. The neutral colour palette and distinctive texture make it a versatile addition \
                                to any room.',
                image = 'images/pillow11.png',
                quantity = 1
            ),
            Item(
                name = 'Soft Cherry Blossom',
                price = 5.50,
                env_impact = '2.3kg(CO2e)',
                description = 'Embrace the delicate beauty of spring all year round. Inspired by the gentle allure of blooming cherry blossoms, this pillow features a \
                    lush, pastel floral pattern that brings a touch of nature''s elegance into your home. The ultra-soft fabric offers a luxurious feel against your \
                        skin, whether you''re decorating a cozy bedroom or brightening up your living space, this pillow is perfect for lounging, napping, or adding a \
                            stylish accent to your decor. The zippered cover is removable and washable, ensuring easy care and lasting freshness.',
                image = 'images/pillow12.png',
                quantity = 1
            ),
            Item(
                name = 'Ultra Soft Fleece Blanket',
                price = 18.99,
                env_impact = '11kg(CO2e)',
                description = 'Wrap yourself in unparalleled comfort with this Ultra Soft Fleece Blanket. Crafted from premium microfleece, this blanket offers the perfect \
                    blend of warmth and softness, making it ideal for cozy nights in. Its lightweight design is perfect for year-round use, providing a gentle layer of \
                        warmth without feeling heavy. Whether you''re curling up on the couch with a good book or adding an extra layer to your bed, the Ultra Soft Fleece\
                              Blanket is your go-to for ultimate comfort.',
                image = 'images/blanket1.png',
                quantity = 1
            ),
            Item(
                name = 'Sherpa Lamb Blanket',
                price = 25.50,
                env_impact = '8.25kg(CO2e)',
                description = 'This luxurious blanket features a unique double-sided reversible design, offering you two distinct textures for a perfect night''s sleep. One \
                    side is crafted from soft Sherpa lamb material that provides a cozy, warm embrace, while the other side boasts ultra-soft cashmere, delivering an even \
                        gentler touch to your skin. This ensures every moment is wrapped in soothing softness and warmth. Indulge in this exquisite piece and elevate your \
                            comfort to new heights.', 
                image = 'images/blanket2.png',
                quantity = 1
            ),
            Item(
                name = 'Soft Fleece Blanket Queen',
                price = 24.99,
                env_impact = '16.25kg(CO2e)',
                description = 'Experience ultimate comfort with the Soft Fleece Blanket Queen, now upgraded with premium microfiber for even greater softness and warmth. \
                    Perfect for chilly nights or as an extra layer on your bed, this thicker and fluffier flannel fleece blanket offers cozy comfort all year round. Its \
                        lightweight yet warm design makes it ideal for snuggling up, while its versatility allows it to serve as a stylish home decor piece, a cozy addition \
                            to your child''s room, or the perfect blanket for your pet. Embrace warmth and luxury with this essential, ultra-soft blanket.',
                image = 'images/blanket3.png',
                quantity = 1
            ),
            Item(
                name = '100% Cotton Duvet Cover and Pillowcase Set',
                price = 65.50,
                env_impact = '5.9kg(CO2e)',
                description = 'The Flora and Funa Duvet Cover and Pillowcase Set combines elegance and comfort with its soft polycotton fabric and striking Flora and Funa \
                    Jacquard print. This set includes Oxford-style pillowcases and a duvet cover, all finished with a secure zip closure for a snug fit. The exquisite \
                        design not only enhances the beauty of your bedroom but also promises a restful night''s sleep with its luxurious feel and attention to detail.',
                image = 'images/set1.png',
                quantity = 1
            ),
            Item(
                name = 'Gypsophila Blooms Duvet Cover and Pillowcase Set',
                price = 59.99,
                env_impact = '6.7kg(CO2e)',
                description = 'Transform your bedroom into a sanctuary of elegance with our Gypsophila Blooms Duvet Cover and Pillowcase Set. Crafted from 100% premium cotton,\
                      this set offers unparalleled softness and a luxurious feel. The duvet cover features a stunning pattern of ethereal gypsophila blooms, gracefully \
                        cascading across a smooth luxury cotton sateen fabric. The matching pillowcases complete the look, creating a cohesive and serene atmosphere in \
                            your space. Experience the perfect blend of style and comfort, and indulge in restful nights and sophisticated design with our exquisite bedding \
                                collection.',
                image = 'images/set2.png',
                quantity = 1
            ),
            Item(
                name = 'Micro Corduroy Duvet Cover and Pillowcase Set',
                price = 49.99,
                env_impact = '12kg(CO2e)',
                description = 'Transform your bedroom into a serene sanctuary with this luxurious duvet cover and pillowcase set, expertly crafted from 100% cotton. The fresh,\
                      crisp white fabric is not only beautifully soft but also features an elegant micro corduroy texture, adding subtle sophistication to your bedding. \
                        The small Oxford edge enhances the set''s refined look, making it the perfect choice for those who appreciate attention to detail. The secure zipper \
                            fastening ensures your duvet stays in place, while the coordinating Oxford pillowcases complete the ensemble for a polished and cohesive finish. \
                                Indulge in comfort and style with this timeless bedding set.',
                image = 'images/set3.png',
                quantity = 1
            ),
            Item(
                name = 'Luxury Satin Eye Mask',
                price = 8.99,
                env_impact = '0.5kg(CO2e)',
                description = 'Elevate your sleep experience with our Luxury Satin Eye Mask, designed to offer unparalleled comfort and relaxation. Made from ultra-soft, \
                    breathable satin, this hypoallergenic mask gently caresses your skin while effectively blocking out light for deeper, more restful sleep. The adjustable \
                        elastic band ensures a perfect fit, making it ideal for meditation, travel, or simply unwinding after a long day. Embrace luxury and wake up refreshed \
                            with the ultimate in sleep accessories.',
                image = 'images/extra1.png',
                quantity = 1
            ),
            Item(
                name = 'Deep Sleep Essentials Kit',
                price = 15.50,
                env_impact = '0.85kg(CO2e)',
                description = 'Designed to guide you into a blissful slumber. This thoughtfully curated kit includes soothing herbal teas, calming essential oils, and a soft eye \
                    mask, all working together to ease a busy mind and promote restful sleep. Ideal for overcoming stressful periods or as a comforting gift, it''s your perfect\
                          companion for a serene escape, whether at home or on the go. Rediscover the joy of a restful night''s sleep with this essential collection.',
                image = 'images/extra2.png',
                quantity = 1
            ),
            Item(
                name = 'Silk Scrunchies 3 Pack',
                price = 9.99,
                env_impact = '17.00kg(CO2e)',
                description = 'Elevate your hair care routine with our Silk Scrunchies 3 Pack, designed to blend style and functionality. Crafted from 100% pure silk, these \
                    scrunchies effortlessly reduce frizz, prevent tangling, and retain moisture, promoting healthier, smoother hair. Say goodbye to split ends and rough \
                        textures as you enjoy a luxurious hold that keeps your hairstyle chic and your locks in pristine condition. Treat yourself to the elegance and\
                              benefits of silk with every use.',
                image = 'images/extra3.png',
                quantity = 1
            )
        ]
        db.session.bulk_save_objects(items_to_insert)
        db.session.commit()

if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
        insert_items() #Automatically adds the items into the database
    app.run(debug=True)