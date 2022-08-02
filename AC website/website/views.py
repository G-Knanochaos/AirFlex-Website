from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

views = Blueprint('views',__name__)

@views.route('')
def default():
    return render_template("home.html",user=current_user)

@views.route('home')
def home():
    return redirect(url_for("views.default"))
    #redirects to default page for people who search url/home

@views.route('webflow')
@login_required
def webflow():
    return render_template("webflow_base.html")
