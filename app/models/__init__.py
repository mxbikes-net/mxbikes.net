from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .product import Product
from .user import User
from .download import Download
from .guid import GUID
