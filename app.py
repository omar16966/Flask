from flask import Flask, render_template, request

# Create a Flask Instance
app = Flask(__name__)

# Create a Route Decorator


@app.route("/")
def index():
    my_name = "Omar"
    stuff = "This is <strong>bold</strong> text"
    text = "This is TEXT For Test  "
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", my_name=my_name, stuff=stuff, text=text, favorite_pizza=favorite_pizza)

# http://localhost:5000/user/name
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

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
