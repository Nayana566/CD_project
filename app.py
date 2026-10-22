from flask import Flask, render_template, request, jsonify
from compiler import compile_source

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.get_json(silent=True) or {}
    source = data.get("code", "")

    if not isinstance(source, str):
        return jsonify({"error": "Source code must be text."}), 400

    if not source.strip():
        return jsonify({
            "output": "Please enter source code.",
            "lexical": "Not run",
            "syntax": "Not run",
            "semantic": "Not run",
            "ast": ""
        })

    return jsonify(compile_source(source))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
