from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import ACdatum
from . import db
from .Backend_Scripts import AC_Calc
from .Backend_Scripts.AC_Calc import input_request as inp

views = Blueprint('views', __name__)

recent_bill_iter = []


@views.route('')
def default():
    return render_template("home.html", user=current_user)


@views.route('home')
def home():
    return redirect(url_for("views.default"))
    # redirects to default page for people who search url/home


@views.route('base')
@login_required
def webflow():
    return render_template("base2.html", user=current_user)


@views.route('aircalculator', methods=['GET', 'POST'])
@login_required
def aircalculator():
    global recent_bill_iter
    if request.method == 'POST':
        KwH, GOT = AC_Calc.KwH(inp('BTU_rating'), inp('EER'), inp('wattage'), [inp('size'), inp('type')])
        res_iter = AC_Calc.Price(KwH, inp('hours'), inp('temp'), inp('state'), inp('use-average'),
                                  inp('major-city'), inp('month'), inp('day-avg-temp'), inp('day-high-temp'),
                                  inp('save'))
        global recent_bill_iter
        recent_bill_iter = res_iter
        if request.form.get("save"):
            new_ACdatum = ACdatum(hours=res_iter[1],
                                  temp=res_iter[2],
                                  estimated_bill=res_ter[0],
                                  user_id=current_user.id)
            db.session.add(new_ACdatum)
            db.session.commit()
        return render_template("aircalculator.html", user=current_user)  # this is what will be returned to the page
    return render_template("aircalculator.html", user=current_user)


@views.route('next_question', methods=['GET', 'POST'])
def next_question():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
