from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
import jwt
import json
import os
from datetime import datetime, timedelta

def login():
    username = request.form['username']
    password = request.form['password']