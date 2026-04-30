from flask import Flask, jsonify, render_template, request, session, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.secret_key = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(15))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    pincode = db.Column(db.String(10))
    user_id = db.Column(db.Integer)

# ---------------- PRODUCTS ----------------
products = [
    {"id":1,"name":"Astronaut Pencil Sharpener","price":149,"category":"Stationery",
     "img":"https://res.cloudinary.com/dhhmstxp2/image/upload/q_auto/f_auto/v1777572636/uc_fkvhws.png"},
    {"id":2,"name":"Cute Eraser Set","price":99,"category":"Stationery",
     "img":"https://res.cloudinary.com/dhhmstxp2/image/upload/q_auto/f_auto/v1777573602/WhatsApp_Image_2026-04-30_at_23.55.29_jvct4k.jpg"},
    {"id":3,"name":"Toy Car","price":299,"category":"Toys",
     "img":"https://via.placeholder.com/200"}
]

# ---------------- AUTH ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message":"User exists"})

    user = User(username=data["username"],
                password=generate_password_hash(data["password"]))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"Registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password,data["password"]):
        session["user_id"] = user.id
        return jsonify({"message":"Login success"})
    return jsonify({"message":"Invalid login"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/user-info")
def user_info():
    if "user_id" not in session:
        return jsonify({})
    user = User.query.get(session["user_id"])
    return jsonify({"username": user.username})

# ---------------- PRODUCTS ----------------
@app.route("/products")
def get_products():
    return jsonify(products)

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CART ----------------
@app.route("/add-to-cart", methods=["POST"])
def add_cart():
    if "user_id" not in session:
        return jsonify({"message":"Login required"})

    d = request.json
    db.session.add(Cart(name=d["name"],price=d["price"],user_id=session["user_id"]))
    db.session.commit()
    return jsonify({"message":"Added to cart"})

@app.route("/cart")
def cart():
    if "user_id" not in session: return jsonify([])
    items = Cart.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([{"id":i.id,"name":i.name,"price":i.price} for i in items])

# ---------------- WISHLIST ----------------
@app.route("/add-wishlist", methods=["POST"])
def add_wish():
    if "user_id" not in session:
        return jsonify({"message":"Login required"})

    d = request.json
    db.session.add(Wishlist(name=d["name"],price=d["price"],user_id=session["user_id"]))
    db.session.commit()
    return jsonify({"message":"Added to wishlist"})

@app.route("/wishlist")
def wishlist():
    if "user_id" not in session: return jsonify([])
    items = Wishlist.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([{"name":i.name,"price":i.price} for i in items])

# ---------------- ADDRESS ----------------
@app.route("/save-address", methods=["POST"])
def save_addr():
    if "user_id" not in session:
        return jsonify({"message":"Login required"})

    d = request.json
    db.session.add(Address(**d,user_id=session["user_id"]))
    db.session.commit()
    return jsonify({"message":"Address saved"})

# ---------------- ORDER ----------------
@app.route("/place-order")
def order():
    if "user_id" not in session:
        return jsonify({"message":"Login required"})

    items = Cart.query.filter_by(user_id=session["user_id"]).all()

    for i in items:
        db.session.add(Order(name=i.name,price=i.price,user_id=session["user_id"]))

    Cart.query.filter_by(user_id=session["user_id"]).delete()
    db.session.commit()

    return jsonify({"message":"Order placed successfully 🎉"})

@app.route("/orders")
def orders():
    if "user_id" not in session: return jsonify([])
    items = Order.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([{"name":i.name,"price":i.price} for i in items])

# ---------------- PAGES ----------------
@app.route("/cart-page")
def cart_page(): return render_template("cart.html")

@app.route("/checkout")
def checkout(): return render_template("checkout.html")

@app.route("/orders-page")
def orders_page(): return render_template("orders.html")

@app.route("/wishlist-page")
def wishlist_page(): return render_template("wishlist.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/")
    return render_template("profile.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
