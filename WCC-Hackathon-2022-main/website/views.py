from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import ACdatum #FanData
from . import db

views = Blueprint('views',__name__)

@views.route('')
def default():
    return render_template("home.html",user=current_user)

@views.route('home')
def home():
    return redirect(url_for("views.default"))
    #redirects to default page for people who search url/home

@views.route('base')
@login_required
def webflow():
    return render_template("base2.html",user=current_user)

@views.route('aircalculator', methods = ['GET','POST'])
@login_required
def aircalculator():
    if request.method == 'POST': #this checks the request type
        '''
        #example of how to make new ACdata instance
        hours, temp, bill = some_backend_function(request.form)
        new_ACdatum = ACdatum(hours=hours,temp=temp,estimated_bill=bill)
        db.session.add(new_ACdatum)
        db.session.commit()
        '''
        #return request.form
        if request.form.get("save"):
            
            new_ACdatum = ACdatum(hours=request.form.get("BTU_rating"),\
                                  temp=request.form.get("EER"),\
                                  estimated_bill=request.form.get("temp"),\
                                  user_id = current_user.id) #associates data with current_user
            db.session.add(new_ACdatum) #adds data to db session
            db.session.commit() #commits data 
        return request.form #this is what will be returned to the page
    return render_template("aircalculator.html",user=current_user)

@views.route('fancalculator', methods = ['GET','POST'])
@login_required
def fancalculator():
    if request.method == 'POST':
        form = request.form
        '''
        new_fanData = FanData(#class variable list)
        #do fan calculations
        current_user.fanData = new_fanData
        db.session.commit()
        '''
        return form
    return render_template("fancalculator.html",user=current_user)

@views.route('next_question', methods = ['GET', 'POST'])
def next_question():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
