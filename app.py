from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==============================
# 🔴 EDIT THIS SECTION FOR NEW PRODUCTS
# ==============================
products = [
    {
        "id": 1,
        "name": "Astronaut Pencil Sharpener",   # 🔴 CHANGE NAME
        "price": 149,                           # 🔴 CHANGE PRICE
        "description": "Cute astronaut-themed sharpener for kids.",
        "features": [
            "Smooth sharpening",
            "Durable material",
            "Portable design",
            "Best for school & gifting"
        ],
        "img": "https://drive.google.com/uc?export=view&id=1n7A_0FlFbWeacd4V-iXo_OpQ5wob-NC_",  # 🔴 CHANGE IMAGE
        "stock": 50                             # 🔴 CHANGE STOCK
    }
]
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
        "description": f"{name} is a stylish and durable product designed for daily use. Perfect for students and gifting."
    })


@app.route("/order/<name>")
def order(name):
    return jsonify({"message": f"✅ Order placed for {name}!"})


if __name__ == "__main__":
    app.run(debug=True)