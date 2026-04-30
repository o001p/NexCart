from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
db = SQLAlchemy(app)

# ---------------- USER ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

# ---------------- CART ----------------
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

# ---------------- PRODUCTS ----------------
products = [
    {
        "id": 1,
        "name": "Astronaut Pencil Sharpener",
        "price": 149,
        "img": "https://res.cloudinary.com/dhhmstxp2/image/upload/q_auto/f_auto/v1777572636/uc_fkvhws.png"
    },
    {
        "id": 2,
        "name": "Cute Eraser Set",
        "price": 99,
        "img": "https://res.cloudinary.com/dhhmstxp2/image/upload/q_auto/f_auto/v1777573602/WhatsApp_Image_2026-04-30_at_23.55.29_jvct4k.jpg"
    }
]

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"], password=data["password"]).first()

    if user:
        return jsonify({"message": "Login success", "user_id": user.id})
    else:
        return jsonify({"message": "Invalid login"})

# ---------------- ADD TO CART ----------------
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json

    item = Cart(
        name=data["name"],
        price=data["price"],
        user_id=data["user_id"]
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added to cart"})

# ---------------- VIEW CART ----------------
@app.route("/cart/<int:user_id>")
def view_cart(user_id):
    items = Cart.query.filter_by(user_id=user_id).all()

    result = []
    for i in items:
        result.append({
            "name": i.name,
            "price": i.price
        })

    return jsonify(result)

# ---------------- CLEAR CART ----------------
@app.route("/clear-cart/<int:user_id>")
def clear_cart(user_id):
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "Cart cleared"})

# ---------------- OTHER ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products")
def get_products():
    return jsonify(products)

@app.route("/ai-description/<name>")
def ai_description(name):
    return jsonify({
        "description": f"{name} is a stylish and durable product designed for daily use."
    })

@app.route("/order/<name>")
def order(name):
    return jsonify({"message": f"Order placed for {name}!"})

# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
