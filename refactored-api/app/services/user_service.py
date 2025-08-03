from app.db.database import get_db_connection
from app.utils.security import hash_password, verify_password
from flask import jsonify

def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return dict(user)
    return {"error": "User not found"}, 404

def create_user(data):
    if not all(k in data for k in ("name", "email", "password")):
        return {"error": "Missing fields"}, 400
    hashed_pw = hash_password(data["password"])
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                 (data["name"], data["email"], hashed_pw))
    conn.commit()
    conn.close()
    return {"message": "User created"}, 201

def update_user(user_id, data):
    if "name" not in data or "email" not in data:
        return {"error": "Missing fields"}, 400
    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                 (data["name"], data["email"], user_id))
    conn.commit()
    conn.close()
    return {"message": "User updated"}

def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted"}

def search_users_by_name(name):
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    conn.close()
    return [dict(user) for user in users]

def authenticate_user(data):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (data["email"],)).fetchone()
    conn.close()
    if user and verify_password(data["password"], user["password"]):
        return jsonify({"status": "success", "user_id": user["id"]})
    return jsonify({"status": "failed"}), 401
