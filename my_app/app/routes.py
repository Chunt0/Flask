from flask import render_template, url_for
from app import db
from app.models import User
from app.forms import LoginForm
from app.auth import login_required
from flask import Flask, render_template, redirect, request

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Add other routes for your apps here
