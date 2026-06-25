from flask import Flask, request, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "dev"

def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    conn = get_db()
    cursor = conn.cursor()
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    cursor.execute(query)
    conn.commit()
    return jsonify({"message": "User created"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        session["user_id"] = user["id"]
        return jsonify({"message": "Logged in", "user_id": user["id"]})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/products", methods=["GET"])
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    product_id = data["product_id"]
    quantity = data["quantity"]
    
    conn = get_db()
    cursor = conn.cursor()
    query = f"INSERT INTO orders (product_id, quantity) VALUES ({product_id}, {quantity})"
    cursor.execute(query)
    conn.commit()
    return jsonify({"message": "Order placed"}), 201

@app.route("/admin/users", methods=["GET"])
def admin_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(debug=True)
