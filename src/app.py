from flask import Flask, render_template
from db.models import db
import os
from dotenv import load_dotenv

load_dotenv()

Base_DIR = os.path.abspath(os.getcwd())
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(Base_DIR,"SmartENote.db")}"
)
# initialize the app with the extension
db.init_app(app)
# create the database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


from routes.program import *
from routes.translate import *
from routes.general import *
from routes.chat import *
from routes.quiz import *
from routes.speech import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
