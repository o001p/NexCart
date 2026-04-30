import os
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_123")

# DATABASE CONFIG: Uses Render persistent disk if available, else local folder
if os.path.exists('/data'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/cart.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

# ---------------- AUTH ROUTES ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"message": "User already exists"}), 400
    
    hashed_pw = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and check_password_hash(user.password, data.get("password")):
        session["user_id"] = user.id
        # FIXED: Sending user_id so frontend JS can save it
        return jsonify({"message": "Login success", "user_id": user.id})
    return jsonify({"message": "Invalid username or password"}), 401

# ---------------- PRODUCT DATA ----------------
products = [
    {"id":1, "name":"Astronaut Pencil Sharpener", "price":149, "img":"https://cloudinary.com"},
    {"id":2, "name":"Unicorn Junior Set", "price":199, "img":"https://cloudinary.com"}
]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/products")
def get_products(): return jsonify(products)

@app.route("/add-to-cart", methods=["POST"])
def add_cart():
    if "user_id" not in session: return jsonify({"message": "Login required"}), 401
    d = request.json
    db.session.add(Cart(name=d["name"], price=d["price"], user_id=session["user_id"]))
    db.session.commit()
    return jsonify({"message": "Added to cart"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
