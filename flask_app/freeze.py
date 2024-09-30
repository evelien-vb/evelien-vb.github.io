from flask_frozen import Freezer
from flask_app import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()