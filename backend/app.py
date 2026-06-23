from flask import Flask, jsonify
from flask_cors import CORS

from routes.notes import notes_bp
from routes.chart import chart_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Yerel geliştirme için frontend (Vite) origin'ine izin ver
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

app.register_blueprint(notes_bp)
app.register_blueprint(chart_bp)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
