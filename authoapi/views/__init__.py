#!/usr/bin/python3
"""task 8"""
from flask import Blueprint



app_views = Blueprint('app_views', __name__, url_prefix="/authoapi/")

from authoapi.views.index import *
from authoapi.views.register import *