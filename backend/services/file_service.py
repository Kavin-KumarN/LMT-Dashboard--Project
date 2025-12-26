from flask import Blueprint, request, jsonify
from services.file_service import save_file, list_files

data_bp = Blueprint("data", __name__)

@data_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    result = save_file(file)
    return jsonify(result), 201


@data_bp.route("/files", methods=["GET"])
def get_files():
    files = list_files()
    return jsonify(files)
