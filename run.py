import logging
from app import app
from config import HOST, PORT

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host=HOST, port=PORT)
