
from flask import Flask, request, jsonify, redirect
from app.utils import generate_short_code, is_valid_url
from app.storage import URLStore

app = Flask(__name__)
store = URLStore()

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while store.get(short_code):
        short_code = generate_short_code()

    store.add(short_code, long_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url_data = store.get(short_code)
    if not url_data:
        return jsonify({"error": "Not found"}), 404

    store.increment_clicks(short_code)
    return redirect(url_data["original_url"])

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    url_data = store.get(short_code)
    if not url_data:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "url": url_data["original_url"],
        "clicks": url_data["clicks"],
        "created_at": url_data["created_at"].isoformat()
    })
