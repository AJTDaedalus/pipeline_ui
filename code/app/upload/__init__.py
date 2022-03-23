
from flask import Blueprint

upload = Blueprint('upload', __name__)

from app.upload import views
