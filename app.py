from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()

from Virtual_avatar import virtual_avatar_bp
from contact_mailer import contact_mailer_bp
from spotify_embed_proxy import spotify_embed_proxy_bp
from twitter_proxy import twitter_proxy_bp

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

# Register blueprints
app.register_blueprint(virtual_avatar_bp)
app.register_blueprint(contact_mailer_bp)
app.register_blueprint(spotify_embed_proxy_bp)
app.register_blueprint(twitter_proxy_bp)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    try:
        return send_from_directory('.', path)
    except Exception:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5000)