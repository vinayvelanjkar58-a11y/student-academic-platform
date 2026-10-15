from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify({
        "message": "Student Academic Management Platform is running",
        "status": "success"
    })


@main.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200
