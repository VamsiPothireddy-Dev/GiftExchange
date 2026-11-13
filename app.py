import csv
import os

import openpyxl
from flask import Flask, jsonify, request

from read_employees import assign_gifts

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_names(path):
    """Load employee names from a .csv, .txt, or .xlsx file."""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        with open(path, newline="") as f:
            return [row["name"].strip() for row in csv.DictReader(f)]

    if ext == ".txt":
        with open(path) as f:
            return [line.strip() for line in f if line.strip()]

    if ext in (".xlsx", ".xlsm"):
        wb = openpyxl.load_workbook(path, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        wb.close()
        if not rows:
            return []
        # Skip header row if the first cell looks like a column name
        start = 1 if str(rows[0][0]).strip().lower() == "name" else 0
        return [str(r[0]).strip() for r in rows[start:] if r and r[0]]

    raise ValueError(f"unsupported file type: {ext}")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


def extract_names(data):
    """Pull a list of names out of a JSON body in any supported shape."""
    if isinstance(data, dict):
        data = data.get("employees") or data.get("names")
    if not isinstance(data, list):
        raise ValueError("body must be a list of names or objects with 'name'")
    names = []
    for item in data:
        if isinstance(item, dict):
            item = item.get("name")
        names.append(str(item).strip())
    return names


def build_response(names):
    try:
        pairs = assign_gifts(names)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    return jsonify([{"name": g, "giftedTo": r} for g, r in pairs])


@app.post("/employees")
def post_employees():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "request body must be valid JSON"}), 400
    try:
        names = extract_names(data)
    except (ValueError, AttributeError) as e:
        return jsonify({"error": str(e)}), 400
    return build_response(names)


@app.get("/employees")
def get_employees():
    path = request.args.get("path")
    if not path:
        return jsonify({"error": "missing 'path' query parameter"}), 400

    full_path = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
    if not os.path.isfile(full_path):
        return jsonify({"error": f"file not found: {path}"}), 404

    try:
        names = load_names(full_path)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    return build_response(names)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5001)
