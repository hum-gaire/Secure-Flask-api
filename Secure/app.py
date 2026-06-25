from flask import Flask, request, jsonify
from models import get_db, init_db
from auth import generate_token, token_required, admin_required
from validators import validate_username, validate_password, validate_order_data
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-fallback-change-me")

@app.before_first_request
def setup():
    init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    
    if not validate_username(username) or not validate_password(password):
        return jsonify({"error": "Invalid username or password"}), 400
    
    password_hash = generate_password_hash(password)
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, "user")
        )
        conn.commit()
    except Exception:
        return jsonify({"error": "Username already exists"}), 409
    
    return jsonify({"message": "User created"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    
    if user and check_password_hash(user["password_hash"], password):
        token = generate_token(user["id"], user["role"])
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/products", methods=["GET"])
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/order", methods=["POST"])
@token_required
def order():
    data = request.get_json()
    valid, error = validate_order_data(data)
    if not valid:
        return jsonify({"error": error}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (request.user_id, data["product_id"], data["quantity"])
    )
    conn.commit()
    
    return jsonify({"message": "Order placed"}), 201

@app.route("/admin/users", methods=["GET"])
@token_required
@admin_required
def admin_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=False)
