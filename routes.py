from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.models import Exercise
from models.database import db
from __main__ import app
