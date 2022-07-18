from flask import Flask, render_template, flash, request
from form import Form, UserForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask Instance
app = Flask(__name__)

# Add Database SQLITE DB
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
# Add Database MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:16966@localhost/users"
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db=db)
# Secret Key
app.config["SECRET_KEY"] = "16966"


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_add = db.Column(db.DateTime, default=datetime.utcnow)
    # Do password hashing
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password,)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create String

    def __repr__(self):
        return "<Name %r>" % self.name


# Create a Route Decorator
@app.route("/")
def index():
    flash("Welcome To Our Website!")
    my_name = "Omar"
    stuff = "This is <strong>bold</strong> text"
    text = "This is TEXT For Test  "
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", my_name=my_name, stuff=stuff, text=text, favorite_pizza=favorite_pizza)


# http://localhost:5000/user/name
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_password = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_add)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


# Create Form Page
@app.route("/form", methods=["GET", "POST"])
def form():
    name = None
    form = Form()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully!")
    return render_template("form.html", name=name, form=form)


# Update Database Record
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update_record(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except print(0):
            flash("Update Unsuccessfull, Try Again!")
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)


@app.route('/delete/<int:id>')
def delete_record(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfuly!")
        our_users = Users.query.order_by(Users.date_add)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Ther is an Erorr, Try Again!")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)


# Create Custom Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
