from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# ✅ DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
db = SQLAlchemy(app)

# ==============================
# ✅ CART DATABASE MODEL (ADD HERE)
# ==============================
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

# ==============================
# PRODUCTS
# ==============================
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

# ==============================
# ❌ REMOVE OLD cart = []
# ==============================


# ==============================
# ✅ ADD TO CART (DATABASE)
# ==============================
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json

    item = Cart(name=data["name"], price=data["price"])
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Item added to database cart"})

# ==============================
# ✅ VIEW CART
# ==============================
@app.route("/cart")
def view_cart():
    items = Cart.query.all()

    result = []
    for i in items:
        result.append({
            "name": i.name,
            "price": i.price
        })

    return jsonify(result)

# ==============================
# ✅ CLEAR CART
# ==============================
@app.route("/clear-cart")
def clear_cart():
    Cart.query.delete()
    db.session.commit()

    return jsonify({"message": "Cart cleared"})

# ==============================
# OTHER ROUTES
# ==============================
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
    return jsonify({"message": f"✅ Order placed for {name}!"})

# ==============================
# RUN APP + CREATE DB
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # ✅ creates cart.db

    app.run(debug=True)
