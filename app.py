from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==============================
# 🔴 EDIT THIS SECTION FOR NEW PRODUCT
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
       
    },

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
