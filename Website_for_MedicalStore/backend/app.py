import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes.customers import customers_bp
from routes.medicines import medicines_bp


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "medical_store.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    app.register_blueprint(customers_bp)
    app.register_blueprint(medicines_bp)

    with app.app_context():
        db.create_all()

    @app.route("/api/health", methods=["GET"])
    def health():
        return {"status": "ok", "message": "Sri Gajana Generic Medical Store API is running"}

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)