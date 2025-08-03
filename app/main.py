from flask import Flask, Blueprint, request, jsonify, redirect
from .models import db, URLMap
from .utils import generate_short_code, is_valid_url, normalize_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

url_shortener_blueprint = Blueprint('url_shortener', __name__)


@url_shortener_blueprint.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@url_shortener_blueprint.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@url_shortener_blueprint.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    long_url = normalize_url(data["url"])

    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400


    while True:
        short_code = generate_short_code()
        if not URLMap.query.filter_by(short_code=short_code).first():
            break

    url_entry = URLMap(original_url=long_url, short_code=short_code)
    db.session.add(url_entry)
    db.session.commit()

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    })

@url_shortener_blueprint.route("/<short_code>")
def redirect_to_url(short_code):
    url_entry = URLMap.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.click_count += 1
        db.session.commit()
        return redirect(url_entry.original_url)
    return jsonify({"error": "Short code not found"}), 404

@url_shortener_blueprint.route("/api/stats/<short_code>")
def get_stats(short_code):
    url_entry = URLMap.query.filter_by(short_code=short_code).first()
    if url_entry:
        return jsonify({
            "url": url_entry.original_url,
            "clicks": url_entry.click_count,
            "created_at": url_entry.created_at.isoformat()
        })
    return jsonify({"error": "Short code not found"}), 404


app.register_blueprint(url_shortener_blueprint)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
